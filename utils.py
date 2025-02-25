import joblib
import pandas as pd

def load_model_and_scaler():
    model = joblib.load("data/models/model.pkl")
    scaler = joblib.load("data/models/scaler.pkl")
    return model, scaler

def predict_round(round_number):

    trained_model, scaler = load_model_and_scaler()

    df = pd.read_csv('data/processed/df_2024.csv')

    numerical_columns = [
        'grid', 'driver_age', 'driver_experience', 'driver_constructor_experience',
        'driver_points', 'driver_standing', 'constructor_points', 
        'constructor_standing', 'driver_wins', 'constructor_wins', 'circuit_danger', 
        'year', 'round'
    ]

    if round_number not in df['round'].unique():
        return pd.DataFrame(columns=['position', 'predicted', 'actual'])
    
    df_current_round = df[df['round'] == round_number].copy()
    
    # Scale and transform
    df_current_round[numerical_columns] = scaler.transform(df_current_round[numerical_columns])    
    one_hot_columns = [col for col in df_current_round.columns if df_current_round[col].dtype == 'bool']
    df_current_round[one_hot_columns] = df_current_round[one_hot_columns].astype(int)
    
    # Prepare features and make predictions
    X_test_current_round = df_current_round.drop(columns=['position'])

    predictions_df = pd.DataFrame({'predicted_position': trained_model.predict(X_test_current_round)}) # Make predictions
    predictions_df.index = df_current_round.index # Ensure the indices align for merging
    df_current_round = pd.concat([df_current_round, predictions_df], axis=1) # Merge predictions back into the original DataFrame
    
    # Helper function to extract driver name from one-hot encoded columns
    def get_driver_name(row):
        for col in one_hot_columns:
            if row[col] == 1:
                # Format the column name to get driver surname
                return col.replace("driver_", "").replace("_", " ").title().split()[-1]
        return None
    
    # Get predicted top 3 drivers
    predicted_top3 = df_current_round.sort_values(by='predicted_position').head(3)
    
    # Get actual top 3 drivers (positions 1.0, 2.0, 3.0)
    actual_top3 = df_current_round[df_current_round['position'].isin([1.0, 2.0, 3.0])].sort_values(by='position')
    
    # Build results dataframe
    results = []
    for position in [1, 2, 3]:
        # Get predicted driver
        pred_driver = None
        if len(predicted_top3) >= position:
            pred_row = predicted_top3.iloc[position-1]
            pred_driver = get_driver_name(pred_row)
        
        # Get actual driver
        actual_driver = None
        actual_row = actual_top3[actual_top3['position'] == float(position)]
        if not actual_row.empty:
            actual_driver = get_driver_name(actual_row.iloc[0])
        
        results.append({
            'position': position,
            'predicted': pred_driver,
            'actual': actual_driver
        })
    
    return pd.DataFrame(results)

