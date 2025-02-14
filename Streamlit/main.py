import streamlit as st
import pandas as pd
from utils import predict_round

with st.sidebar:
    st.page_link('main.py', label='Predictor', icon='🏎️')
    st.page_link('pages/project_workflow.py', label='Project Workflow', icon='🚀')

st.title(f'🏎️ F1 Predictions')

df = pd.read_csv('assets/rounds_2024.csv')

round = st.selectbox("Select a race from the 2024 season to make predictions!", 
                    options=df['round'],
                    format_func=lambda x: f"Round {x}: {df['name'].iloc[x - 1]}")

st.text(f"Results for {df['name'].iloc[round - 1]}")

prediction_df = predict_round(round)

st.dataframe(prediction_df, hide_index=True)

predicted_driver = prediction_df['predicted'].iloc[0]
actual_winner = prediction_df['actual'].iloc[0]

if predicted_driver == actual_winner:
    st.text(f"🟢 Model predicted {predicted_driver} as winner correctly!")
else:
    podium_drivers = prediction_df['actual'].tolist()
    
    if predicted_driver in podium_drivers: # Finished in the podium
        actual_position = prediction_df.loc[prediction_df['actual'] == predicted_driver, 'position'].iloc[0]
        
        pos_text = "2nd" if actual_position == 2 else "3rd"
            
        st.text(f"🟡 Model predicted {predicted_driver} as winner, but he finished {pos_text} instead.")
    else: 
        st.text(f"🔴 Model predicted {predicted_driver} as winner, but he didn't even finish in the podium.")

st.page_link(page=df['url'].iloc[round - 1], label="Full race details", icon=":material/link:")