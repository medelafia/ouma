from core.prometheus_module import fetch_metrics , fetch_instances
import pandas as pd 

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
                
                current = {}
                for value in metrics_result['values']  : 
                    metric_name = metric['name'] 
                    timestamp = value[0]
                    metric_value = value[1]
                    if len(data[metrics_result['metric']['instance']]) == 0 : 
                        data[metrics_result['metric']['instance']].append({'timestamp' : timestamp , metric_name : metric_value})
                    else :
                        for j in range(len(data[metrics_result['metric']['instance']])) :
                            if timestamp == data[metrics_result['metric']['instance']][j]['timestamp'] :  
                                data[metrics_result['metric']['instance']][j][metric_name] = metric_value
    
    return data






