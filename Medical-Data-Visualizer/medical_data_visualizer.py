import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
weight = df['weight']
height = df['height'] / 100
bmi = (weight / (height * height))
df['overweight'] = bmi > 25

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['overweight'] = df['overweight'].astype('int')
df['cholesterol'] = (df['cholesterol'] != 1).astype('int')
df['gluc'] = (df['gluc'] != 1).astype('int')


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat1 = df[[
        'cholesterol', 'gluc', 'smoke', 'alco', 'active', 
        'cardio','overweight'
    ]]
    df_cat = df_cat1.melt(id_vars=['cardio'],
                          value_vars=[
                              'cholesterol', 'gluc', 'smoke', 
                              'alco', 'active', 'overweight'
                          ])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'
                             ]).size().to_frame(name='total').reset_index()

    # Draw the catplot with 'sns.catplot()'
    grid = sns.catplot(x="variable",
                    y="total",
                    hue="value",
                    data=df_cat,
                    col='cardio',
                    kind="bar")

    fig = grid.fig 
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data

    df_heat = df[
    (df['ap_lo'] <= df['ap_hi']) &
    (df['height'] >= df['height'].quantile(0.025)) &
    (df['height'] <= df['height'].quantile(0.975)) &
    (df['weight'] >= df['weight'].quantile(0.025)) &
    (df['weight'] <= df['weight'].quantile(0.975)) 
  ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr)

    # Set up the matplotlib figure    
    fig, ax = plt.subplots(figsize=(7, 7))

    # Draw the heatmap with 'sns.heatmap()'
    ax = sns.heatmap(corr, mask=mask, vmin=-0.1, vmax=.3,              annot=True, cbar_kws={'shrink':.40}, fmt='.1f',               square=True, center=0, linewidths='0.4')

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
