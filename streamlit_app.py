import streamlit as st
import pandas as pd
from utils import predict_round

with st.sidebar:
    st.page_link('streamlit_app.py', label='Predictor', icon='🏎️')
    st.page_link('pages/project_workflow.py', label='Project Workflow', icon='🚀')

st.title(f'🏎️ F1 Predictions')

df = pd.read_csv('data/processed/rounds_2024.csv')

round = st.selectbox("Select a race from the 2024 season to make predictions!", 
                    options=df['round'],
                    format_func=lambda x: f"Round {x}: {df['name'].iloc[x - 1]}")

st.text(f"Results for {df['name'].iloc[round - 1]}")

prediction_df = predict_round(round)

prediction_df_reordered = prediction_df.set_index('position').reindex([2, 1, 3]).reset_index()

st.markdown("""
<style>
    .podium-container {
        display: flex;
        align-items: flex-end;
        justify-content: center; 
        gap: 5px;
    }
            
    .podium-step {
        width: 100%;
        border: 2px solid #444;
        margin: 0 2px;
    }
    
    .step-label {
        text-align: center;
        width: 100%;
        font-size: 0.9em;
    }
    
    .driver-name {
        top: 0;
        text-align: center;
        padding: 5px;
        font-weight: bold;
        font-size: 1.2em;
    }
    
    /* Individual step heights */
    .first-place { height: 150px; background: #FFD700; }
    .second-place { height: 100px; background: #C0C0C0; }
    .third-place { height: 50px; background: #CD7F32; }
            
    /* Individual spacer heights */
    .first-place-spacer { height: 0px; background: transparent !important; }
    .second-place-spacer { height: 50px; background: transparent !important; }
    .third-place-spacer { height: 100px; background: transparent !important; }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

def create_podium_column(column, title, drivers):
    with column:
        with st.container(border=True):
            st.subheader(title)
            
            st.markdown('<div class="podium-container">', unsafe_allow_html=True)
            
            cols = st.columns(3) #Steps
            positions = [
                ('2nd Place', 'second-place', 'second-place-spacer'),
                ('1st Place', 'first-place', 'first-place-spacer'),
                ('3rd Place', 'third-place', 'third-place-spacer')
            ]
            
            for idx, (col, (label, css_class, css_class_spacer)) in enumerate(zip(cols, positions)):
                with col:
                    st.markdown(
                        f'<div class="{css_class_spacer}"></div>'
                        f'<div class="driver-name">{drivers[idx]}</div>'
                        f'<div class="podium-step {css_class}"></div>'
                        f'<div class="step-label">{label}</div>',
                        unsafe_allow_html=True
                    )
            
            st.markdown('</div>', unsafe_allow_html=True)

create_podium_column(col1, "Model Predicted", prediction_df_reordered['predicted'])
create_podium_column(col2, "Actual Results", prediction_df_reordered['actual'])

predicted_driver = prediction_df['predicted'].iloc[0]
actual_winner = prediction_df['actual'].iloc[0]

if predicted_driver == actual_winner:
    st.success(f"Model predicted {predicted_driver} as winner correctly!", icon="✅")
else:
    podium_drivers = prediction_df['actual'].tolist()
    
    if predicted_driver in podium_drivers: # Finished in the podium
        actual_position = prediction_df.loc[prediction_df['actual'] == predicted_driver, 'position'].iloc[0]
        
        pos_text = "2nd" if actual_position == 2 else "3rd"
            
        st.warning(f"Model predicted {predicted_driver} as winner, but he finished {pos_text} instead.", icon="⚠️")
    else: 
        st.error(f"Model predicted {predicted_driver} as winner, but he didn't even finish in the podium.", icon="🚨")

st.page_link(page=df['url'].iloc[round - 1], label="Full race details", icon=":material/link:")