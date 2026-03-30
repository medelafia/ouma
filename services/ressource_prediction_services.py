from core.prometheus_module import fetch_metrics
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

    df = pd.DataFrame(metrics)
    



    return df.values()
