"""
Author Huy Phan
February 2024
Description: This program extracts data and change it into DoL and LoL 
to find out the home court advantage in NBA finals and regular season of 2021.
"""

import pandas as pd
import matplotlib.pyplot as plt

def todf(data, cols):
    """
    Converts data into a pandas DataFrame.

    Parameters:
    data (dict or list): The data to be converted. If a dictionary,
    keys are column names and values are lists of column values.
    If a list, it is assumed to be a list of lists where each inner list is a row of data.
    cols (list): The column names for the DataFrame. Only used if data is a list of lists.

    Returns:
    df (DataFrame): The resulting pandas DataFrame.
    """
    if isinstance(data, dict):
        df = pd.DataFrame(data)
    elif isinstance(data, list):
        df = pd.DataFrame(data, columns=cols)
    else:
        raise ValueError("Data must be a dictionary or a list of lists.")
    return df

def todol(filename,columns):
    """
    This function reads a CSV file and organizes the data into dictionaries
    based on home and away teams.

    Parameters:
        filename (str): The path to the CSV file.
        columns (list of str): The columns to extract data from.

    Returns:
        tuple: Two dictionaries containing the data for home and away teams.
    """
    data_home = {col: [] for col in columns}
    data_away = {col: [] for col in columns}

    with open(filename,encoding='utf-8') as user_input:
        header_list = user_input.readline().strip().split(',')
        indices = {col: header_list.index(col) for col in columns}
        for row in user_input:
            row = row.strip().split(',')
            if row[header_list.index('Home')] == '1':
                for element in columns:
                    data_home[element].append(row[indices[element]])
            else:
                for element in columns:
                    data_away[element].append(row[indices[element]])

    return data_home, data_away

def tolol(filename,columns):
    """
    This function reads a CSV file and
    organizes the data into lists of lists based on home and away teams.

    Parameters:
        filename (str): The path to the CSV file.
        columns (list of str): The columns to extract data from.

    Returns:
        tuple: Two lists of lists containing the data for home and away teams.
    """
    data_home = []
    data_away = []

    with open(filename,encoding='utf-8') as user_input:
        header_list = user_input.readline().strip().split(',')
        indices = [header_list.index(col) for col in columns]
        for row in user_input:
            row = row.strip().split(',')
            if row[header_list.index('Home')] == '1':
                data_home.append([row[index] for index in indices])
            else:
                data_away.append([row[index] for index in indices])

    return data_home, data_away

def clean_data(df):
    """
    Parameter: df
    Description:
    Cleans the given DataFrame by removing duplicates, handling missing values, 
    and ensuring correct data types.
    Return: A clean data frame
    """
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)  # Remove rows with missing values
    for col in ['Win', 'FGP', 'TRB', 'AST', 'TOV', 'PTS']:
        df[col] = pd.to_numeric(df[col], errors='coerce') #Replace non-numeric value with NaN
    df.dropna(inplace=True)  # Remove rows with conversion errors
    return df

def read_csv(file_path):
    """
    Reads a CSV file into a pandas DataFrame.
    
    Parameters:
        file_path (str): The path to the CSV file.
        
    Returns:
        DataFrame: The DataFrame containing the CSV data.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")
    return

def ensure_numeric(df, cols):
    """
    Ensures specified columns in a DataFrame are treated as numeric.
    """
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def plot_home_away_win_rates(df_home, df_away, title):
    """
    Plots win rates for home and away games.
    """
    # Ensure 'Win' column is numeric
    df_home = ensure_numeric(df_home, ['Win'])
    df_away = ensure_numeric(df_away, ['Win'])

    home_win_rate = df_home['Win'].mean()
    away_win_rate = df_away['Win'].mean()

    plt.figure(figsize=(7, 5))
    plt.bar(['Home', 'Away'], [home_win_rate, away_win_rate], color=['blue', 'orange'])
    plt.title(title)
    plt.ylabel('Win Rate')
    plt.show()

def plot_2021_season_overview(df_season):
    """
    Plots an overview of the 2021 season showing the number of wins for home and away teams.

    Parameters:
        df_season (DataFrame): DataFrame containing 2021 season data.
    """
    df_season['HomeWin'] = df_season['home_score'] > df_season['away_score']
    home_wins = df_season['HomeWin'].sum()
    away_wins = len(df_season) - home_wins  # Assuming no ties

    plt.figure(figsize=(7, 5))
    plt.bar(['Home Wins', 'Away Wins'], [home_wins, away_wins], color=['green', 'red'])
    plt.title('2021 Season Home vs Away Wins')
    plt.ylabel('Number of Wins')
    plt.show()

def plot_performance_metrics_difference(df_home, df_away, title):
    """
    Plots differences in performance metrics (FGP, TRB, AST, TOV, PTS) between home and away games.
    
    Parameters:
        df_home (DataFrame): DataFrame containing home games data.
        df_away (DataFrame): DataFrame containing away games data.
        title (str): Title for the plot.
    """
    metrics = ['FGP', 'TRB', 'AST', 'TOV', 'PTS']
    # Ensure metrics are numeric
    df_home = ensure_numeric(df_home, metrics)
    df_away = ensure_numeric(df_away, metrics)

    # Calculate average metrics for home and away
    home_means = df_home[metrics].mean()
    away_means = df_away[metrics].mean()

    # Calculate differences (home - away)
    differences = home_means - away_means

    # Plotting
    plt.figure(figsize=(10, 6))
    differences.plot(kind='bar',\
    color=['skyblue', 'lightgreen', 'lightcoral', 'lightpink', 'wheat'])
    plt.title(title)
    plt.ylabel('Difference (Home - Away)')
    plt.axhline(0, color='grey', linewidth=0.8)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def main():
    """
    Main function to process data for champion and runner-up teams.

    This function reads data from CSV files, organizes it into DataFrames,
    and prints the resulting DataFrames.

    Returns:
    Data for champion and runner-up for home and away teams 
    """
    columns = ['Year', 'Team', 'Win', 'FGP', 'TRB', 'AST', 'TOV', 'PTS']
    champhome, champaway = todol("championsdata.csv", columns)
    runneruphome, runnerupaway = tolol("runnerupsdata.csv", columns)

    dfchamphome = todf(champhome, columns)
    dfchampaway = todf(champaway, columns)
    dfrunneruphome = todf(runneruphome, columns)
    dfrunnerupaway = todf(runnerupaway, columns)
    dfseason_2021 = read_csv("season_2021_basic.csv")

    # Clean the data
    dfchamphome = clean_data(dfchamphome)
    dfchampaway = clean_data(dfchampaway)
    dfrunneruphome = clean_data(dfrunneruphome)
    dfrunnerupaway = clean_data(dfrunnerupaway)

    print("Champion Home Teams:")
    print(dfchamphome)
    print("\nChampion Away Teams:")
    print(dfchampaway)
    print("\nRunner-Up Home Teams:")
    print(dfrunneruphome)
    print("\nRunner-Up Away Teams:")
    print(dfrunnerupaway)
    print("\n2021 Season Overview:")
    print(dfseason_2021)

    # Plotting functions
    plot_home_away_win_rates(dfchamphome, dfchampaway,\
    'Champion Teams Home vs Away Win Rates')
    plot_home_away_win_rates(dfrunneruphome, dfrunnerupaway,\
    'Runner-Up Teams Home vs Away Win Rates')
    plot_2021_season_overview(dfseason_2021)

    # Plotting functions for performance metrics differences
    plot_performance_metrics_difference(dfchamphome, dfchampaway,\
    'Champion Team Performance Metrics Difference: Home vs Away')
    plot_performance_metrics_difference(dfrunneruphome, dfrunnerupaway,\
    'Runner-Up Team Performance Metrics Difference: Home vs Away')

if __name__ == "__main__":
    main()
    