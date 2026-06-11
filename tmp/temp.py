#import tensorflow

"""
def create_sequences(X, seq_len=40):
    Xs = []
    for i in range(len(X) - seq_len):
        Xs.append(X[i:i+seq_len])
    return np.array(Xs)

input_scaler = load_pkl("input_scaler")
output_scaler = load_pkl("output_scaler")
cnn_lstm_model = load_model('others/cnn_lstm.keras')

def prepare_data_input_cnn_lstm(dataframes) : 
    prepared_data = {}
    for key in dataframes: 
        dataframes[key]['timestamp'] = pd.to_datetime(dataframes[key]['timestamp'] , unit='s')
        dataframes[key].set_index('timestamp', inplace=True)
        dataframes[key].sort_index(inplace=True)

        dataframes[key] = dataframes[key][[
            'CPU usage ',
            'Memory usage ',
            'Disk write throughput KB/s',
            'Network received throughput KB/s'
        ]]

        print(dataframes[key])
        dataframes[key].columns = ['cpu', 'memory', 'disk', 'network']

        for col in dataframes[key].columns : 
            dataframes[key][col] = pd.to_numeric(dataframes[key][col] , errors='coerce')
        
        dataframes[key] = np.log1p(dataframes[key])

        for i in range(1, 6):
            dataframes[key][f'cpu_lag{i}'] = dataframes[key]['cpu'].shift(i)
            dataframes[key][f'memory_lag{i}'] = dataframes[key]['memory'].shift(i)
            
        dataframes[key]['cpu_rolling_mean'] = dataframes[key]['cpu'].rolling(5).mean()
        dataframes[key]['cpu_rolling_std'] = dataframes[key]['cpu'].rolling(5).std()
        dataframes[key]['memory_rolling_mean'] = dataframes[key]['memory'].rolling(5).mean()
        dataframes[key]['memory_rolling_std'] = dataframes[key]['memory'].rolling(5).std()

        dataframes[key] = dataframes[key].dropna()
        X = input_scaler.transform(dataframes[key].values)
        X_seq  = create_sequences(X)
        prepared_data[key] = X_seq

    return dataframes , prepared_data  


def predict_next_and_save_by_cnn_lstm(structured_data) : 
    dfs , values = prepare_data_input_cnn_lstm(structured_data)
    print(values)
    for key in dfs :
        try : 
            predicted_datetime = dfs[key].tail(1).index[0] + timedelta(minutes=prediction_interval)
            predictions = cnn_lstm_model.predict(values[key])[0]
            
            print("Beta Model prediction :", output_scaler.inverse_transform(predictions))

            #threshold_cpu = get_threshold(dfs[key] , key, 'cpu')
            #threshold_memory = get_threshold(dfs[key] , key , 'memory')
            #metricsPrediction = MetricsPrediction(timestamp=predicted_datetime , instance_id=key , cpu_usage=predicted_cpu ,memory_usage=predicted_memory)
            
            #handle_prediction(metricsPrediction , threshold_cpu , threshold_memory)
        except Exception as ex:
            print("ERROR :" , ex)

            
def is_cnn_lstm_prediction_engine_ready(metrics: dict[str, pd.DataFrame]) -> bool :  
    return bool(metrics) and all(df.shape[0] >= 46 for df in metrics.values())
"""