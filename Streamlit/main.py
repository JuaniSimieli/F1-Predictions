import streamlit as st
import pandas as pd
from utils import predict_round

st.title("F1 Predictions")

df = pd.read_csv('Streamlit/assets/df_2024.csv')
rounds2024 = df['round'].unique()

round = st.selectbox("Select a race from the 2024 season to make predictions!", rounds2024)

st.text(f"Results for round {round}")

prediction_df = predict_round(round)

st.dataframe(prediction_df)

predicted_driver = prediction_df['predicted'].iloc[0]
actual_winner = prediction_df['actual'].iloc[0]

if predicted_driver == actual_winner:
    st.text(f"Model predicted {predicted_driver} as winner correctly!")
else:
    podium_drivers = prediction_df['actual'].tolist()
    
    if predicted_driver in podium_drivers: # Finished in the podium
        actual_position = prediction_df.loc[prediction_df['actual'] == predicted_driver, 'position'].iloc[0]
        
        pos_text = "2nd" if actual_position == 2 else "3rd"
            
        st.text(f"Model predicted {predicted_driver} as winner, but he finished {pos_text} instead.")
    else: 
        st.text(f"Model predicted {predicted_driver} as winner, but he didn't even finish in the podium.")