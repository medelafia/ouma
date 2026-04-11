from services.prometheus_service import fetch_metrics , fetch_instances
import pandas as pd 
import tensorflow as tf
import pickle 
from services.influx_service import save_prediction 
from schemas.schemas import MetricsPrediction
from datetime import timedelta
import sklearn
import numpy as np

def check_timestamp_existance(list_obj , timestamp  ) : 
    for record in list_obj : 
        if record['timestamp'] == timestamp :
            return True 
    return False 


def prepare_data_input() : 
    """
        func_name : prepare_data_input
        description : Load data from prometheus , create record for making ML model prediction ,
        scale data using the scaler used in the training process , create new features such as lag1 , cpu_std ...  
        args : None 
        return : a list of dataframes ready to be an input of model to predict next values
    """
    metrics = fetch_metrics()
    data = { }
    
    ## loop through the metrics and append each metric to predefined dictionnary 
    for metric in metrics : 
        if metric['value']['status'] == 'success' : 
            for i in range(len(metric['value']['data']['result'])) :
                metrics_result = metric['value']['data']['result'][i]
                if metrics_result['metric']['instance'] not in data :
                    data[metrics_result['metric']['instance']] = []
                
                
                for value in metrics_result['values']  : 
                    metric_name = metric['name'] 
                    timestamp = value[0]
                    metric_value = value[1]
                    if not check_timestamp_existance(data[metrics_result['metric']['instance']] , timestamp) : 
                        data[metrics_result['metric']['instance']].append({'timestamp' : timestamp , metric_name : metric_value})
                    else :

                        for j in range(len(data[metrics_result['metric']['instance']])) :
                            if timestamp == data[metrics_result['metric']['instance']][j]['timestamp'] :  
                                data[metrics_result['metric']['instance']][j][metric_name] = metric_value
    

    """
    here i tried to create dataframes based on dict created after the previous part ,
    and in the same time i tried to preprocess the data following the same stepss in
    the model training process, and adding some additionnal features such as cpu_lag5...
    """
    scaler = load_min_max_scaler('input')
    dataframes = { key : pd.DataFrame(data[key]) for key in data }
    values = []
    i = 0 
    for key in dataframes: 
        dataframes[key]['timestamp'] = pd.to_datetime(dataframes[key]['timestamp'] , unit='s')
        dataframes[key].set_index('timestamp', inplace=True)
        dataframes[key].sort_index(inplace=True)
        
        for col in dataframes[key].columns : 
            dataframes[key][col] = pd.to_numeric(dataframes[key][col] , errors='coerce')
 
        dataframes[key]['CPU capacity provisioned [MHZ]']= 2400 * dataframes[key]['CPU cores']

        dataframes[key]['hour'] = dataframes[key].index.hour.astype(int)
        dataframes[key]['day'] = dataframes[key].index.day.astype(int)
        dataframes[key]['weekday'] = dataframes[key].index.weekday.astype(int)

        dataframes[key]['cpu_lag1'] = dataframes[key]['CPU usage [%]'].shift(1)
        dataframes[key]['cpu_lag5'] = dataframes[key]['CPU usage [%]'].shift(5)

        dataframes[key]['cpu_mean'] = dataframes[key]['CPU usage [%]'].rolling(5).mean()
        dataframes[key]['cpu_std'] = dataframes[key]['CPU usage [%]'].rolling(5).std()
        ### deleteing the first 5 data records , because they will contain noisy rows 

        
        dataframes[key] = dataframes[key].replace([np.inf, -np.inf], np.nan)
        dataframes[key] = dataframes[key].fillna(method='bfill')
        dataframes[key] = dataframes[key].dropna()

        dataframes[key] = dataframes[key].tail(24)

        #values[i] = scaler.transform(dataframes[key])
        values.append(dataframes[key][['CPU cores','CPU capacity provisioned [MHZ]',	'CPU usage [%]','Memory capacity provisioned [KB]',	'Memory usage [%]', 'Disk read throughput [KB/s]','Disk write throughput [KB/s]','Disk size [GB]','Network received throughput [KB/s]','hour','day','weekday','cpu_lag1','cpu_lag5','cpu_mean','cpu_std']].values)
        print(values[i])
        values[i] = scaler.transform(values[i])
        i += 1 

    return dataframes , values 


def load_min_max_scaler(type) :
    return pickle.load(open(f"others/scaler_lstm_ressource_prediction_{'data' if type == 'input' else 'labels'}.pkl" , 'rb')) 

def load_lstm_model() :
    model = tf.keras.models.load_model("others/model.h5")

    return model

def predict_next_and_save() : 
    dfs , input_values_sequence_dict = prepare_data_input()
    model = load_lstm_model() 
    output_scaler = load_min_max_scaler(type="output")
    results = {}
    for key in range(len(input_values_sequence_dict)) :
        print(input_values_sequence_dict[key])
        predictions = model.predict(input_values_sequence_dict[key])
        predictions = output_scaler.inverse_transform(predictions) 
        print(predictions)
        predicted_datetime = dfs[key].iloc[-1].index + timedelta(minutes=5)
        save_prediction(key, MetricsPrediction(predicted_datetime , key , predictions[0][0] , predictions[0][0]) ) 

        results[key] = predictions
    return results



def is_prediction_service_ready() :
    return len(fetch_metrics()[0]['value']['data']['result'][0]['values']) > 29