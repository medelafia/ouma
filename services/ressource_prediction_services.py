from services.prometheus_service import fetch_metrics , fetch_instances
import pandas as pd 
import tensorflow as tf
import pickle 
from services.influx_service import save_prediction 
from schemas.schemas import MetricsPrediction
from datetime import timedelta
import xgboost
import sklearn
import numpy as np
from utils.instance_factory import get_instance_by_host_and_port
from services.alerting_services import send_alert
from services.anomaly_service import create_and_save_anomaly ,  save_anomaly
import datetime
from services.metadata_services import load_metadata
anomalies = { 
    "memory" :  {
        "count" : 0 ,  
        "anomaly" : None 
    },
    "cpu" : {
        "count" : 0 ,  
        "anomaly" : None 
    }
}
thresholds = {
}


def load_pkl(name) :
    model = pickle.load(open(f"others/{name}.pkl", 'rb'))
    return model

memory_model = load_pkl("memory_model")
cpu_model = load_pkl("cpu_model")
prediction_interval = load_metadata().PREDICTION_INTERVAL


def check_timestamp_existance(list_obj , timestamp  ) : 
    for record in list_obj : 
        if record['timestamp'] == timestamp :
            return True 
    return False 


def get_threshold(df , key , metric) : 
    global thresholds
    if key not in thresholds : 
        thresholds[key] = { "cpu" : None , "memory" : None }
    if thresholds[key][metric] is None :
        col = "CPU usage " if metric == 'cpu' else "Memory usage " 
        thresholds[key][metric] = df[col].mean() + 2 * df[col].std()
    
    return thresholds[key][metric]


def prepare_data_input(metrics) : 
    """
        func_name : prepare_data_input
        description : Load data from prometheus , create record for making ML model prediction ,
        scale data using the scaler used in the training process , create new features such as lag1 , cpu_std ...  
        args : None 
        return : a list of dataframes ready to be an input of model to predict next values
    """
    data = { }
    
    ## loop through the metrics and append each metric to predefined dictionnary 
    for metric in metrics : 
        if metric['value']['status'] == 'success' : 
            for i in range(len(metric['value']['data']['result'])) :
                metrics_result = metric['value']['data']['result'][i]
                #instance_id = get_instance_by_host_and_port(metrics_result['metric']['instance'].split(':')[0] , int(metrics_result['metric']['instance'].split(':')[1]))
                instance_id = get_instance_by_host_and_port(metrics_result['metric']['instance'].split(':')[0] , int(metrics_result['metric']['instance'].split(':')[1])).instance_id
                if instance_id not in data :
                    data[instance_id] = []
                
                
                for value in metrics_result['values']  : 
                    metric_name = metric['name'] 
                    timestamp = value[0]
                    metric_value = value[1]
                    if not check_timestamp_existance(data[instance_id] , timestamp) : 
                        data[instance_id].append({'timestamp' : timestamp , metric_name : metric_value})
                    else :

                        for j in range(len(data[instance_id])) :
                            if timestamp == data[instance_id][j]['timestamp'] :  
                                data[instance_id][j][metric_name] = metric_value
    

    """
    here i tried to create dataframes based on dict created after the previous part ,
    and in the same time i tried to preprocess the data following the same stepss in
    the model training process, and adding some additionnal features such as cpu_lag5...
    """

    dataframes = { key : pd.DataFrame(data[key]) for key in data }
    #values = {}
    for key in dataframes: 
        dataframes[key]['timestamp'] = pd.to_datetime(dataframes[key]['timestamp'] , unit='s')
        dataframes[key].set_index('timestamp', inplace=True)
        dataframes[key].sort_index(inplace=True)
        
        for col in dataframes[key].columns : 
            dataframes[key][col] = pd.to_numeric(dataframes[key][col] , errors='coerce')
 
        dataframes[key]['CPU capacity provisioned MHZ']= 2400 * dataframes[key]['CPU cores']

        dataframes[key]['hour'] = dataframes[key].index.hour.astype(int)
        dataframes[key]['day'] = dataframes[key].index.day.astype(int)
        dataframes[key]['weekday'] = dataframes[key].index.weekday.astype(int)

        dataframes[key]['cpu_lag1'] = dataframes[key]['CPU usage '].shift(1)
        dataframes[key]['cpu_lag5'] = dataframes[key]['CPU usage '].shift(3)
        dataframes[key]['memory_lag1'] = dataframes[key]['Memory usage '].shift(1)
        dataframes[key]['memory_lag5'] = dataframes[key]['Memory usage '].shift(3)

        dataframes[key]['cpu_mean'] = dataframes[key]['CPU usage '].rolling(3).mean()
        dataframes[key]['cpu_std'] = dataframes[key]['CPU usage '].rolling(3).std()
        dataframes[key]['memory_mean'] = dataframes[key]['Memory usage '].rolling(3).mean()
        dataframes[key]['memory_std'] = dataframes[key]['Memory usage '].rolling(3).std()
        ### deleteing the first 5 data records , because they will contain noisy rows 

        dataframes[key] = dataframes[key].replace([np.inf, -np.inf], np.nan)
        dataframes[key] = dataframes[key].fillna(method='bfill')
        dataframes[key] = dataframes[key].dropna()



        dataframes[key] = dataframes[key].tail(10)

        print(dataframes[key].tail())

        #values[i] = scaler.transform(dataframes[key])
        #values[key] = dataframes[key][['CPU cores','CPU capacity provisioned MHZ',	'CPU usage ','Memory capacity provisioned KB',	'Memory usage ','Disk size GB','hour','day','weekday','cpu_lag1','cpu_lag5','memory_lag1','memory_lag5','cpu_mean','cpu_std','memory_mean','memory_std']].values 
        #values[key] = input_scaler.transform(values[key])
        
        feature_columns = [
            'CPU cores', 'hour', 'day', 'weekday', 'cpu_lag1', 'cpu_lag5',
            'memory_lag1', 'memory_lag5', 'cpu_mean', 'cpu_std', 'memory_mean',
            'memory_std', 'CPU capacity provisioned MHZ', 'CPU usage ',
            'Memory capacity provisioned KB', 'Memory usage ', 'Disk size GB'
        ]
        dataframes[key][feature_columns].tail(1).to_csv(f'others/{key}.csv', mode='a', index=True, header=False)
        dataframes[key] = dataframes[key][feature_columns]
        
    return dataframes 


def predict_next_and_save(metrics) : 
    global model 
    dfs = prepare_data_input(metrics)
    results = {}
    for key in dfs :
        print(dfs[key].tail(1))
        predicted_datetime = dfs[key].tail(1).index[0] + timedelta(minutes=prediction_interval)
        predicted_memory ,predicted_cpu = memory_model.predict(dfs[key].tail(1))[0] , cpu_model.predict(dfs[key].tail(1))[0]
        
        print("INFO:next predicted datetime :" ,predicted_datetime)

        print("INFO:insert value ",save_prediction(MetricsPrediction(timestamp=predicted_datetime , instance_id=key , cpu_usage=predicted_cpu ,memory_usage=predicted_memory) ) )
        threshold_cpu = get_threshold(dfs[key] , key, 'cpu')
        threshold_memory = get_threshold(dfs[key] , key , 'memory')

        if predicted_cpu > threshold_cpu : 
            if anomalies['cpu']['count'] == 0 : 
                anomaly = create_and_save_anomaly(key)
                anomalies['cpu']['anomaly'] = anomaly
                send_alert("High cpu usage after 5 min" ,"LOW" , anomaly.anomaly_id)
            elif anomalies['cpu']['count'] <= 2 : 
                send_alert(f"CPU still high (x{anomalies['cpu']['count']})" ,"MEDIUM" ,anomalies['cpu']['anomaly'].anomaly_id)
            else :
                send_alert(f"CRITICAL: CPU high repeatedly (x{anomalies['cpu']['count']})" ,"HIGH" , anomalies['cpu']['anomaly'].anomaly_id)
            anomalies['cpu']['count'] += 1  
            combined_datetime = datetime.datetime.combine(anomalies['cpu']['anomaly'].detection_date , anomalies['cpu']['anomaly'].detection_time) 
            anomalies['cpu']['anomaly'].duration = (datetime.datetime.now() - combined_datetime).total_seconds()
            anomalies['cpu']['anomaly'] = save_anomaly(anomalies['cpu']['anomaly'])
        else : 
            anomalies['cpu']['count'] = 0 
            anomalies['cpu']['anomaly'] = None
        
        if predicted_memory > threshold_memory : 

            if anomalies['memory']['count'] == 0 : 
                anomaly = create_and_save_anomaly(key)
                anomalies['memory']['anomaly'] = anomaly
                send_alert("High memory usage after 5 min" ,"LOW" , anomaly.anomaly_id)
            elif anomalies['memory']['count'] <= 2 : 
                send_alert(f"MEMORY still high (x{anomalies['memory']['count']})" ,"MEDIUM", anomalies['memory']['anomaly'].anomaly_id)
            else :
                send_alert(f"CRITICAL: MEMORY high repeatedly (x{anomalies['memory']['count']})" ,"HIGH" , anomalies['memory']['anomaly'].anomaly_id)
            anomalies['memory']['count'] += 1  
        else : 
            anomalies['memory']['count'] = 0 
            anomalies['memory']['anomaly'] = None

        results[key] = [[predicted_cpu , predicted_memory]]
    return results

def is_prediction_service_ready(metrics) :
    return len(metrics[0]['value']['data']['result'][0]['values']) >= 2