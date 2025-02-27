# F1-Predictions

[![Open App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://f1-predictions-juanisimieli.streamlit.app/)

### Motivation

My career as a Data Scientist started with motorsport: not so long ago I bought a racing simulator and that became my favorite hobby. I always like to push everything to the limit, so I asked myself, how can I do it here? How can I improve? That’s when all this “data world” came up. Turns out, a racing simulator not only simulates the real life in looks and physics, but also on data. In this case, telemetry. I found out I could analyze this data to improve my lap times, get my ideal fuel load, estimate the best lap time to pit, and so on. I loved that so much that I thought, how can I make this my career? That’s when I found out about Data Science.

So as my first Data Science project, I figured I could go back to where it all started and make it about motorsport, and of course it had to be Formula 1, right? I thought it would be fun to predict the winner of a Grand Prix, and see what variables are the most important ones for a weekend of success. I will predict the whole 2024 season and compare it to the actual results.

### Getting started
The model can be used through a web application created with **Streamlit**. You can use this platform to select the desired round from the 2024 calendar and make predictions. To access the Streamlit app, please click [here](https://f1-predictions-juanisimieli.streamlit.app/). 

You can also download the project from GitHub:

``` 
# Clone the repository:
git clone https://github.com/JuaniSimieli/F1-Predictions.git

# Install dependencies:
pip install -r requirements.txt

# To run Streamlit locally on your PC:
streamlit run ./streamlit_app.py
```

### About the model and data
The data used for this was queried from [Ergast](https://ergast.com/mrd/). You can download the latest [here](https://ergast.com/mrd/db/). Note that the project was made with data up until the end of the 2024 season. To run the [Data Collection Notebook](https://github.com/JuaniSimieli/F1-Predictions/blob/main/notebooks/01_data_collection.ipynb), you'll need to download the database image from Ergast and set up a file called `sql_credentials.env` and fill it with the information below (updating it to your credentials).

```
# sql_credentials.env 
DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost
DB_NAME=f1_db
```

For the full workflow, refer to the [notebooks](https://github.com/JuaniSimieli/F1-Predictions/tree/main/notebooks) or the full explanation on Stremalit under the **🚀 Project Workflow** page.
