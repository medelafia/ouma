from core.prometheus_module import fetch_metrics , fetch_instances
import pandas as pd 




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
        return : ready data to predict next values
        args : None 

        {
            'instance 1' : [
                {   
                    timestamp : 1000000 , 
                    cpu_usage : 10 , 
                    ...
                }
            ] 
            
            
        }
    """
    metrics = fetch_metrics()
    data = { }
    
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
    



    dataframes = [ pd.DataFrame(data[elem]) for elem in data]
    for i in range(len(dataframes)): 
        print(dataframes[i].head())
        dataframes[i]['timestamp'] = pd.to_datetime(dataframes[i]['timestamp'] , unit='s')
        dataframes[i].set_index('timestamp', inplace=True)
        dataframes[i].sort_index(inplace=True)
        dataframes[i]['hour'] = dataframes[i].index.hour.astype(int)
        dataframes[i]['day'] = dataframes[i].index.day.astype(int)
        dataframes[i]['weekday'] = dataframes[i].index.weekday.astype(int)

        dataframes[i]['cpu_lag1'] = dataframes[i]['CPU usage [%]'].shift(1)
        dataframes[i]['cpu_lag5'] = dataframes[i]['CPU usage [%]'].shift(5)

        dataframes[i]['cpu_mean'] = dataframes[i]['CPU usage [%]'].rolling(5).mean()
        dataframes[i]['cpu_std'] = dataframes[i]['CPU usage [%]'].rolling(5).std()

        print(dataframes[i].head())
    

    return data
     






