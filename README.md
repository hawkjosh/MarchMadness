# My March Madness EDA Project

## Project Description

My first attempt at an exploratory data analysis using historical and current NCAA Division I Men's Basketball data to make predictions about this year's tournament outcome.

## Installing Required Packages

To install required packages, run `pip install -r "requirements.txt"`

## Possible next steps

- **Descriptive Analysis**: Start with a broad overview. Calculate basic statistics (mean, median, standard deviation, etc.) for each category and stat type. This will give you a sense of the data's central tendencies and variability. Visualize these stats through histograms, box plots, and density plots to understand the distribution of each statistic.

- **Correlation Analysis**: Investigate how different stats correlate with winning percentage and each other. This could help identify key factors contributing to a team's success. Heatmaps and scatter plots are great for visualizing these relationships.

- **Trend Analysis**: Analyze trends over the years. This could involve looking at how the importance of certain stats (like three-point shooting or turnovers) has evolved. Time series plots can be helpful here, showing how averages for significant stats have changed over time.

- **Comparative Analysis**: Compare stats between teams that have historically performed well in the tournament versus those that haven’t. This might reveal certain statistical benchmarks or thresholds that successful teams typically meet.

- **Cluster Analysis**: Use clustering techniques to group teams with similar statistical profiles. This could reveal archetypes of teams (e.g., defensive powerhouses, high-scoring teams) and how well each archetype tends to perform in the tournament.

- **Predictive Modeling**: More complex approach, building predictive models (like logistic regression for binary outcomes, or more sophisticated machine learning models) using historical data to predict tournament outcomes can be very insightful. Use your stats as features to predict outcomes such as game winners, tournament progression, or even identify potential upsets.

- **Incorporating KenPom Stats**: KenPom stats are highly regarded in college basketball analytics. Compare your findings with KenPom’s efficiency ratings, tempo, and other advanced metrics. This could validate your analysis or reveal new insights.

- **Visualization and Dashboarding**: Develop interactive dashboards using tools like Tableau, Power BI, or even Python libraries (Dash by Plotly, for instance) to make analysis accessible. This can help in exploring data dynamically, comparing teams, and identifying patterns more intuitively.

- **Narrative and Storytelling**: Use analysis to tell stories. This could involve identifying underdog teams with the potential to make deep runs, powerhouse teams that might be vulnerable, or key matchups to watch based on statistical matchups.
