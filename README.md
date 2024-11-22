# F1-Predictions

My career as a Data Scientist started with motorsport: not so long ago I bough a racing simulator and that became my favorite hobby. I always like to push everything to the limit, so I asked myself, how can I do it here? How can I improve? That’s when all this “data world” came up. Turns out, a racing simulator not only simulates the real life in looks and physics, but also on data. In this case, telemetry. I found out I could analyze this data to improve my lap times, get my ideal fuel load, estimate the best lap time to pit, and so on. I loved that so much that I thought, how can I make this my career? That’s when I found out about Data Science.

So as my first Data Science project, I figured I could go back to where it all started and make it about motorsport, and of course it had to be Formula 1, right? I thought it would be fun to predict the winner of a Grand Prix, and see what variables are the most important ones for a weekend of success. With 3 races remaining of the 2024 season, I thought it would be also the perfect time to predict them. 

I will divide this project into 3 major steps: **Data Collection**, **Exploratory Data Analysis** (EDA) and **Machine Learning Modeling**.

## 1. Data Collection
Here I'll explain my data source and how I used it for gathering all the information I need.

My primary source will be [Ergast API](http://ergast.com/mrd/), which is an experimental web service which provides a historical record of motor racing data for non-commercial purposes. It will be deprecated soon, but since its successor it’s still in alpha phase, for this first version of the project, I’ll stick to Ergast. One feature this API has is that it lets you download the full MySQL database image, so you can run it locally, and thats the approach I took. 

First I'll start by querying the results table: I’ll fetch all foreign keys related to tables we'll need to get data from, plus the grid position. I'll join that with the race table to get other foreign keys plus the year, round, and date of the race. 

![first_table](Data-collection/Images/table_01.png)

That will be my base table, based on that, I’ll start adding more columns that will help me later, like driver’s age, experience, experience with current team, all time wins, all time wins with current team, points, and more. Then to make this simpler, I’ll filter the data from 2010 onwards, because that is the last major change in F1’s point system. In the future I may consider all the data from 1950 and try to convert it to the current point system. 

I ended up with a table with 21 columns (147 after I get dummies). For the complete step by step, refer to the [Data Collection Notebook](Data-collection/Data_Collection.ipynb). 

## 2. Exploratory Data Analysis

