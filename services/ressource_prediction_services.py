from core.prometheus_module import fetch_metrics , fetch_nodes
import pandas as pd 

def prepare_data_input() : 
    """
        func_name : prepare_data_input
        description : Load data from prometheus , create record for making ML model prediction ,
        scale data using the scaler used in the training process , create new features such as lag1 , cpu_std ...  
        return : ready data to predict next values
        args : None 
    """
    metrics = fetch_metrics()
    nodes = fetch_nodes() 
    dfs = []

    for node in nodes : 
        
        df = pd.DataFrame(metrics)

    
    



    return df.values()
