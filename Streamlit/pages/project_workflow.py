import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import random

df_eda = pd.read_csv('assets/EDA/df_eda.csv')
races_held_2010 = pd.read_csv('assets/EDA/df_races_2010.csv')

def grid_vs_finish():
    fig = px.box(df_eda, x='grid', y='position', 
                labels={'grid': 'Grid Position', 'position': 'Finish Position'})
    fig.update_layout(
        title="Grid Position vs Finish Position",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig)

def heatmap():
    heatmap_data = df_eda[['grid', 'position', 'driver_age', 'driver_experience', 'driver_constructor_experience', 
                   'driver_points', 'driver_standing', 'constructor_points', 'constructor_standing', 
                   'driver_wins', 'constructor_wins', 'circuit_danger']]
    
    correlation_matrix = heatmap_data.corr()
    fig = px.imshow(correlation_matrix,
                   color_continuous_scale='RdBu',
                   text_auto=".2f")
    fig.update_layout(
        title="Feature Correlation Heatmap",
        xaxis_showgrid=False,
        yaxis_showgrid=False
    )
    st.plotly_chart(fig)

def pole_to_win():
    pole_wins = df_eda[(df_eda['grid'] == 1) & (df_eda['position'] == 1)].shape[0]
    total_poles = df_eda[df_eda['grid'] == 1].shape[0]
    pole_win_rate = pole_wins / total_poles

    fig = px.bar(x=['Pole to Win Rate'], y=[pole_win_rate],
                labels={'y': 'Probability', 'x': ''},
                title='Overall Probability of Winning from Pole Position')
    fig.update_traces(width=0.3)
    fig.update_layout(
        yaxis_range=[0,1],
        showlegend=False
    )
    st.plotly_chart(fig)

def circuit_danger():
    circuit_data = df_eda.groupby('circuitRef', as_index=False)['circuit_danger'].mean()
    circuit_data = circuit_data.sort_values(by='circuit_danger', ascending=False)  # Sort descending

    colors = sns.color_palette("RdYlGn", len(circuit_data)).as_hex()
    
    fig = px.treemap(circuit_data, 
                    path=['circuitRef'], 
                    values='circuit_danger',
                    title='Circuit Danger Levels by Circuit',
                    color_discrete_sequence=colors)
    st.plotly_chart(fig)

def pole_to_win_circuit():
    total_races_by_circuit = df_eda.groupby('circuitRef').size()
    wins_from_pole_by_circuit = df_eda[(df_eda['grid'] == 1) & (df_eda['position'] == 1)].groupby('circuitRef').size()

    pole_to_win_ratio = (wins_from_pole_by_circuit / total_races_by_circuit).fillna(0)

    pole_to_win_ratio = pole_to_win_ratio[pole_to_win_ratio > 0].sort_values(ascending=False)

    sizes = pole_to_win_ratio.values 
    labels = pole_to_win_ratio.index

    colors = sns.color_palette("summer", len(labels)).as_hex()

    fig = px.treemap(pd.DataFrame({'circuitRef': labels, 'ratio': sizes}),
                    path=['circuitRef'],
                    values='ratio',
                    title='Pole to Win Ratio by Circuit',
                    color_discrete_sequence=colors)
    st.plotly_chart(fig)

def pole_to_win_danger_circuit():
    circuit_danger = df_eda.groupby('circuitRef')['circuit_danger'].mean()

    chart_height = max(600, len(circuit_danger) * 20)
    
    total_races_by_circuit = df_eda.groupby('circuitRef').size()
    wins_from_pole_by_circuit = df_eda[(df_eda['grid'] == 1) & (df_eda['position'] == 1)].groupby('circuitRef').size()
    pole_to_win_ratio = (wins_from_pole_by_circuit / total_races_by_circuit).fillna(0) * 100
    
    circuit_data = pd.DataFrame({
        'circuit_danger': circuit_danger,
        'pole_to_win_ratio': pole_to_win_ratio
    }).reset_index().sort_values(by='circuit_danger', ascending=False)
    
    melted_df = circuit_data.melt(id_vars='circuitRef', 
                                value_vars=['circuit_danger', 'pole_to_win_ratio'])
    
    fig = px.bar(melted_df, 
                y='circuitRef', 
                x='value', 
                color='variable',
                barmode='group',
                orientation='h',
                height=chart_height,
                title='Pole to Win Ratio and Circuit Danger by Circuit')
    
    fig.update_layout(
        yaxis_title='Circuit',
        xaxis_title='Value',
        legend_title='Metric',
        yaxis=dict(
            autorange="reversed",  # Keep ascending order
            tickmode='linear',  # Force all labels
            showticklabels=True
        ),
        margin=dict(l=150)
    )
    st.plotly_chart(fig)

def circuit_map():
    colors = ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(len(races_held_2010))]

    fig = px.scatter_mapbox(races_held_2010,
                            lat="lat",
                            lon="lng",
                            hover_name="name",
                            zoom=0.8,
                            height=600)
    
    fig.update_layout(
        mapbox_style="carto-darkmatter",
        margin={"r":0,"t":0,"l":0,"b":0},
        title="Circuit Locations (2010 Onward)"
    )
    
    fig.update_traces(
        marker=dict(
            size=14,
            opacity=0.8,
            color=colors
        )
    )
    
    st.plotly_chart(fig)

def race_count_chart():
    sorted_df = races_held_2010.sort_values(by='race_count', ascending=True)

    chart_height = max(600, len(sorted_df) * 20)
    
    fig = px.bar(sorted_df,
                 x='race_count',
                 y='circuitRef',
                 orientation='h',
                 height=chart_height,
                 labels={'race_count': 'Number of Races', 'circuitRef': 'Circuit Name'},
                 color_discrete_sequence=['skyblue'])
    
    fig.update_layout(
        title='Number of Races Held by Circuit (2010 Onward)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        yaxis=dict(
            autorange="reversed",  # Keep ascending order
            tickmode='linear',  # Force all labels
            showticklabels=True
        ),
        margin=dict(l=150)
    )
    
    st.plotly_chart(fig)

with st.sidebar:
    st.page_link('main.py', label='Predictor', icon='🏎️')
    st.page_link('pages/project_workflow.py', label='Project Workflow', icon='🚀')

tab1, tab2, tab3 = st.tabs(["Data Collection", "EDA", "ML Modeling"])

with tab1:
    st.title("🔍 Data Collection")

    st.subheader("Step 1")
    st.text("Here I'll query for all rows in results table, I'll fetch all foreign keys related to tables we'll need to get data from, plus the grid position. I'll join that with the race table to get other foreign keys plus the year, round, and date of the race.")
    with st.expander("See Code"):
        code = '''
            SELECT r.resultId, r.raceId, r.driverId, r.constructorId, 
                r.grid, r.position, races.year, races.round, races.circuitId, races.date
            FROM results r
            JOIN races 
            ON r.raceId = races.raceId
            '''
        st.code(code, language='sql')
    with st.expander("See output"):
        df = pd.read_csv('assets/Data-collection/step_01.csv')
        st.dataframe(data=df, height=200)

    st.subheader('Step 2')
    st.text("Here I'll calculate the driver age at the time of the race, for that I'll get the driver's DOB and compare that to each entry's date to get the drivers age at that time.")
    with st.expander("See Code"):
        code = '''
            driver_age_query = """
                SELECT d.driverId, d.dob
                FROM drivers d
                """
            drivers_df = pd.read_sql(driver_age_query, con=engine)

            results_df = results_df.merge(drivers_df, on="driverId", how="left")
            results_df['driver_age'] = results_df.apply(
                lambda row: row['date'].year - row['dob'].year - 
                    ((row['date'].month, row['date'].day) < (row['dob'].month, row['dob'].day)),
                axis=1
            )
            '''
        st.code(code, language='python')
    with st.expander("See output"):
        df = pd.read_csv('assets/Data-collection/step_02.csv')
        st.dataframe(data=df, height=200)

    st.subheader('Step 3')
    st.markdown("Here I'll calculate the driver's experience (Number of GPs entered). For that I'll start by sorting the current `results_df` by `date` and `resultId`. Then I'll create a cumulative count of appearance for each driver.")
    with st.expander("See Code"):
        code = '''
            results_df = results_df.sort_values(by=['date', 'resultId']).reset_index(drop=True)

            results_df['driver_experience'] = results_df.groupby('driverId').cumcount()
            '''
        st.code(code, language='python')
    with st.expander("See output"):
        df = pd.read_csv('assets/Data-collection/step_03.csv')
        st.dataframe(data=df, height=200)
    
        st.subheader('Step 3')
    
    st.subheader('Step 4')
    st.markdown("Similar to last step, I'll calculate the driver's experience with it's current team. For that I'll create a cumulative count of appearances for each `driverId` and `constructorId` combination")
    with st.expander("See Code"):
        code = '''
            results_df['driver_constructor_experience'] = results_df.groupby(['driverId', 'constructorId']).cumcount()
            '''
        st.code(code, language='python')
    with st.expander("See output"):
        df = pd.read_csv('assets/Data-collection/step_04.csv')
        st.dataframe(data=df, height=200)

    st.subheader('Step 5')
    st.markdown("Now I want to calculate both the driver's all time wins and the driver's all time wins with that specific constructor. Using a temporary `win_indicator`, and similary to last steps, using a cumulative count, then dropping the temporary column as it's no longer needed.")
    with st.expander("See Code"):
        code = '''
            results_df['win_indicator'] = results_df['position'] == 1.0

            results_df['driver_wins'] = results_df.groupby('driverId')['win_indicator'].cumsum()
            results_df['constructor_wins'] = results_df.groupby(['driverId', 'constructorId'])['win_indicator'].cumsum()

            results_df.drop(columns=['win_indicator'], inplace=True)
            '''
        st.code(code, language='python')
    with st.expander("See output"):
        df = pd.read_csv('assets/Data-collection/step_05.csv')
        st.dataframe(data=df, height=200)

    st.subheader('Step 6')
    st.markdown("For this step I need to make a new query: I need `driver_points` and `driver_standings` after each race, that I'll then merge to `results_df`")
    with st.expander("See Code"):
        code = '''
            driver_standings_query = """
                SELECT ds.raceId, ds.driverId, ds.points AS driver_points, ds.position AS driver_standing
                FROM driverStandings ds
            """
            driver_standings_df = pd.read_sql(driver_standings_query, con=engine)
            results_df = results_df.merge(driver_standings_df, on=["raceId", "driverId"], how="left")
            '''
        st.code(code, language='python')
    with st.expander("See output"):
        df = pd.read_csv('assets/Data-collection/step_06.csv')
        st.dataframe(data=df, height=200)

    st.subheader('Step 7')
    st.markdown("Same as last step, but this time for constructor standings data.")
    with st.expander("See Code"):
        code = '''
            constructor_standings_query = """
                SELECT cs.raceId, cs.constructorId, cs.points AS constructor_points, cs.position AS constructor_standing
                FROM constructorStandings cs
            """
            constructor_standings_df = pd.read_sql(constructor_standings_query, con=engine)
            results_df = results_df.merge(constructor_standings_df, on=["raceId", "constructorId"], how="left")
            '''
        st.code(code, language='python')
    with st.expander("See output"):
        df = pd.read_csv('assets/Data-collection/step_07.csv')
        st.dataframe(data=df, height=200)

    st.divider()
    st.warning('Warning (explanation below)', icon="⚠️")
    with st.expander("See explanation"):
        st.markdown("""
                    Now we have a problem here:
                    As we can see the standings and data we got are for ***after*** each race, and since we want to predict a race result (finishing position), we need to have the standings from ***before*** the race. 
                    This means we will have to do some logic:
                    1. For the first race ever (1950 round 1), `driver_wins`, `constructor_wins`, `driver_points`, `driver_standing`, `constructor_points` and `constructor_standing` will be set to zero.
                    2. For the first race of every season, `driver_points`, `driver_standing`, `constructor_points` and `constructor_standing` will be 0, but `driver_wins` and `constructor_wins` will be carried over from the past race.
                    3. All data we have now on an entry, will be moved 1 race ahead. I.e. 2022 round 4 has the data for *after* that race, that data will be the *starting* data for the next race. So 2022 round 4 data will now be 2022 round 5 data.
                    4. Keeping the last step logic, if a season like 2022 has 22 rounds, we will end up with a round 23. So we need to check if the data we're handling is from the last round of the season, therefore we won't append that new entry to the new DataFrame. 
                    """)
    st.divider()

    st.subheader('Step 8')
    st.markdown("Shift data. As this is a more complicated step, I'll go step by step in the code block")
    with st.expander("See Code"):
        code = '''
            # 1. Sort the DataFrame chronologically
            results_df = results_df.sort_values(by=['year', 'round', 'driverId', 'constructorId'])

            # 2. Shift driver/constructor wins across all races (carry over between seasons)
            results_df['driver_wins_shifted'] = results_df.groupby('driverId')['driver_wins'].shift(1).fillna(0)
            results_df['constructor_wins_shifted'] = results_df.groupby('constructorId')['constructor_wins'].shift(1).fillna(0)

            # 3. Shift points/standings within each season (reset to 0 at the start of a season)
            # For drivers
            results_df['driver_points_shifted'] = (
                results_df.groupby(['driverId', 'year'])['driver_points']
                .shift(1)
                .fillna(0)
            )
            results_df['driver_standing_shifted'] = (
                results_df.groupby(['driverId', 'year'])['driver_standing']
                .shift(1)
                .fillna(0)
            )

            # For constructors
            results_df['constructor_points_shifted'] = (
                results_df.groupby(['constructorId', 'year'])['constructor_points']
                .shift(1)
                .fillna(0)
            )
            results_df['constructor_standing_shifted'] = (
                results_df.groupby(['constructorId', 'year'])['constructor_standing']
                .shift(1)
                .fillna(0)
            )
            '''
        st.code(code, language='python')
    with st.expander("See output"):
        df = pd.read_csv('assets/Data-collection/step_08.csv')
        st.dataframe(data=df, height=200)

    st.subheader('Step 9')
    st.markdown("Rename shifted columns and drop unnecesary ones")
    with st.expander("See Code"):
        code = '''
            results_df = results_df.drop(columns=['driver_wins', 'constructor_wins', 'driver_points', 'driver_standing', 'constructor_points', 'constructor_standing'])
            results_df = results_df.rename(columns={'driver_wins_shifted': 'driver_wins', 
                                                    'constructor_wins_shifted': 'constructor_wins', 
                                                    'driver_points_shifted': 'driver_points', 
                                                    'driver_standing_shifted': 'driver_standing', 
                                                    'constructor_points_shifted': 'constructor_points', 
                                                    'constructor_standing_shifted': 'constructor_standing'})

            merged_df = results_df.copy() # Defragmentate
            '''
        st.code(code, language='python')
    with st.expander("See output"):
        df = pd.read_csv('assets/Data-collection/step_09.csv')
        st.dataframe(data=df, height=200)

    st.subheader('Step 10')
    st.markdown("Filter `merged_df` to keep only rows where `year` is 2010 or later. Why I'm doing this? Because 2010 is the last time F1 made a big change in the points award system. So for simplicity, instead of converting all the previous races for the current point system, I'll work with all the entries from 2010 or later.")
    with st.expander("See Code"):
        code = '''
            merged_df = merged_df[merged_df['year'] >= 2010].reset_index(drop=True)
            '''
        st.code(code, language='python')
    with st.expander("See output"):
        df = pd.read_csv('assets/Data-collection/step_10.csv')
        st.dataframe(data=df, height=200)

    st.subheader('Step 11')
    st.markdown("Calculate Circuit Danger Metric. What is this? One of the tables is *status* which displays the status for each *results* entry. And since each of those entries corresponds to one *race*, we can calculate how many incidents there were on each circuit, and the total of races on that circuit. So `circuit_danger` will result of dividing the total of incidents on a circuit by the total races on that circuit, from 2010 or later.")
    with st.expander("See Code"):
        code = '''
            SELECT 
                c.circuitId,
                c.name,
                COUNT(*) AS count,
                total_races.total,
                COUNT(*) * 1.0 / total_races.total AS circuit_danger
            FROM 
                races r
            JOIN 
                results res ON r.raceId = res.raceId
            JOIN 
                circuits c ON r.circuitId = c.circuitId
            JOIN 
                (SELECT circuitId, COUNT(*) AS total 
                FROM races 
                WHERE year >= 2010 
                GROUP BY circuitId) AS total_races
                ON r.circuitId = total_races.circuitId
            WHERE 
                res.statusId IN (3, 4) 
                AND r.year >= 2010
            GROUP BY 
                c.circuitId, c.name, total_races.total
            ORDER BY 
                circuit_danger DESC;
            '''
        st.code(code, language='sql')
    with st.expander("See output"):
        df = pd.read_csv('assets/Data-collection/step_11.csv')
        st.dataframe(data=df, height=200)

    st.subheader('Step 12')
    st.markdown("Here I'll merge `circuit_danger` to the `merged_df`. The rest of the values will be used for EDA.")
    with st.expander("See Code"):
        code = '''
            circuit_danger_df = circuit_df[['circuitId', 'circuit_danger']]

            merged_df = merged_df.merge(circuit_danger_df, on='circuitId', how='left')
            '''
        st.code(code, language='python')
    with st.expander("See output"):
        df = pd.read_csv('assets/Data-collection/step_12.csv')
        st.dataframe(data=df, height=200)

    st.subheader('Step 13')
    st.markdown("Drop Nulls.")

    st.subheader('Step 14')
    st.markdown("Drop unnecesary columns: `date`, `dob`, `resultId` and `raceId`")

    st.subheader('Step 15')
    st.markdown("Change IDs from `driverId`, `circuitId` and `constructorId` to their descriptive names and apply one-hot-encoding")
    with st.expander("See Code"):
        code = '''
            driver_id_query = """
                SELECT driverId, driverRef
                FROM drivers
            """
            drivers_name = pd.read_sql(driver_id_query, con=engine)

            merged_df = merged_df.merge(drivers_name[['driverId', 'driverRef']], on='driverId', how='left')
            merged_df = merged_df.drop(columns=['driverId'])
            merged_df = merged_df.rename(columns={'driverRef': 'driver'})
            '''
        st.code(code, language='python')

        code = '''
            circuit_id_query = """
                SELECT circuitId, circuitRef
                FROM circuits
            """
            circuits_name = pd.read_sql(circuit_id_query, con=engine)

            merged_df = merged_df.merge(circuits_name[['circuitId', 'circuitRef']], on='circuitId', how='left')
            merged_df = merged_df.drop(columns=['circuitId'])
            merged_df = merged_df.rename(columns={'circuitRef': 'circuit'})
            '''
        st.code(code, language='python')

        code = '''
            constructor_id_query = """
                SELECT constructorId, constructorRef
                FROM constructors
            """
            constructors_name = pd.read_sql(constructor_id_query, con=engine)

            merged_df = merged_df.merge(constructors_name[['constructorId', 'constructorRef']], on='constructorId', how='left')
            merged_df = merged_df.drop(columns=['constructorId'])
            merged_df = merged_df.rename(columns={'constructorRef': 'constructor'})
            '''
        st.code(code, language='python')

        code = '''
            merged_df = pd.get_dummies(merged_df, columns=['driver', 'circuit', 'constructor'])
            '''
        st.code(code, language='python')
    with st.expander("See output"):
        df = pd.read_csv('assets/Data-collection/step_15.csv')
        st.dataframe(data=df, height=200)

    st.subheader('Step 16')
    st.markdown("""
            drop one-hot-encoding columns with the least amount of values:
            - `driver` < 25: To drop drivers that participated in less than a full season
            - `constructor` < 50: To drop teams that participated in less than a full season
            - `circuit` < 3: To drop circuits that hosted less than 3 races
        """)
    with st.expander("See Code"):
        code = '''
            for col in merged_df.columns:
                if 'driver' in col and merged_df[col].sum() < 25:
                    merged_df.drop(col, axis = 1, inplace = True)
        
                elif 'constructor' in col and merged_df[col].sum() < 50:
                    merged_df.drop(col, axis = 1, inplace = True)

                elif 'circuit' in col and merged_df[col].sum() < 3:
                    merged_df.drop(col, axis = 1, inplace = True)
    
                else:
                    pass
            '''
        st.code(code, language='python')
    with st.expander("See output"):
        df = pd.read_csv('assets/Data-collection/step_16.csv')
        st.dataframe(data=df, height=200)

with tab2:
    st.title("📊 EDA")

    intro = """
    For this step, I’d like to start explaining all the columns that will be mentioned:
    - `grid`: Starting position
    - `position`: Finishing position (this one is the one that I want to predict)
    - `driver_age`: Driver age at the time of the race
    - `driver_constructor_experience`: Driver experience with current team until that race
    - `driver_points`: Driver’s points before the start of the race
    - `driver_standing`: Driver’s standing in the championship before the start of the race
    - `constructor_points`: Driver’s current team points before the start of the race
    - `constructor_standing`: Driver’s current team standing in the championship before the start of the race
    - `driver_wins`: Driver’s total wins in F1 at the time of the race
    - `constructor_wins`: Driver’s current team total wins in F1 at the time of the race
    - `circuit_danger`: How prone are accidents in that circuit. Comes from dividing amount of total crashes in that circuit divided by the amount of races that circuit held.
  
    I want to start by creating a heat map between all this variables to see how correlated they are.
    """

    st.markdown(intro)
    heatmap()
    st.text("This gives us a good idea of how the different variables affect each other. Since I’ll be trying to predict position, we can see the one that has the most impact is grid. So let’s compare them in a Box Plot. Note that grid 0 is used for a pit lane start.")
    grid_vs_finish()
    st.text("So the chances of getting a win from pole (grid==1) are really high. In fact, here’s a chart of the overall probability of winning from pole position.")
    pole_to_win()
    st.text("More than 50% chance of winning a race if the starting position is the pole.")
    st.text("Are circuits related to this? Formula 1 hosted GPs in many different circuits over the years, which they also changed the layouts of. Here’s a map of all the circuits that hosted races since 2010.")
    circuit_map()
    st.text("It’s important to say that some circuits hosted only 1 race, like Mugello, where others like Silverstone hosted 16. Here’s a chart that shows the number of races held by each circuit.")
    race_count_chart()
    st.text("All of them are different. Some are permanent racing venues, while others are street circuits. Both are really different, but sometimes people may say that in some circuits like Monaco, pole position is the key to a win, mainly because of how narrow and difficult it is to overtake. Let’s see how different the pole-to-win ratio is varied by circuit, where the bigger squares represent the higher chance of converting a pole into a win.")
    pole_to_win_circuit()
    st.text("Does this have anything to do with accidents? Let’s see how they compare based on how prone accidents are to each circuit.")
    circuit_danger()
    st.text("We can see some similarities in the last 2 graphics. Is it possible that how prone a circuit is to accidents leads to a higher chance of converting a pole into a win?")
    pole_to_win_danger_circuit()
    st.text("We can see there is no correlation between the two variables.")

with tab3:
    st.title("🤖 ML Modeling")