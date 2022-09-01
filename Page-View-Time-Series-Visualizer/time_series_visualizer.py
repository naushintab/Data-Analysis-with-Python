import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv(
     "fcc-forum-pageviews.csv",
     parse_dates=["date"],
     usecols=["date", "value"]
).set_index('date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    x = df.index
    y = df['value']
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y, color='red')
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year']=df_bar.index.year
    df_bar['month']=df_bar.index.month_name()
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=months, ordered=True)
    df_bar['month'].sort_values()
    df_bar = df_bar.groupby(['year', 'month']).mean().dropna().reset_index()
    
    # Draw bar plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax = sns.barplot(x="year", y="value", hue="month", data=df_bar,
                hue_order=months, ci="sd", palette='muted')
    ax.set(xlabel="Years", ylabel="Average Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box['monthnumber'] = df.index.month
    df_box = df_box.sort_values('monthnumber')

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    sns.boxplot(x='year', y='value', data=df_box, ax=ax[0])
    ax[0].set(xlabel="Year", ylabel="Page Views", title="Year-wise Box Plot (Trend)")
    sns.boxplot(y="value", x="month", data=df_box, ax=ax[1])
    ax[1].set(xlabel="Month", ylabel="Page Views", title="Month-wise Box Plot (Seasonality)")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
