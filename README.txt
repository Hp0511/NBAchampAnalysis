Dataset we use in this project:
championsdata.csv and runnerupsdata.csv both contain data about in detail stats of NBA finals games. We use data such as: field goal percentage, total assists, turnovers, scores to explore the impact of home court advantage.

For regular season, we picked season 2021 to to compare the average points scored by home team and away team to explore the impact of home court advantage


Functions we use for parsing data

toDF(data, cols): This function converts data into a pandas DataFrame. The data can be a dictionary or a list of lists. If it’s a dictionary, the keys are treated as column names and the values as lists of column values. If it’s a list of lists, each inner list is treated as a row of data. The cols parameter, which is a list of column names, is only used if the data is a list of lists.
toDoL(filename, columns): This function reads a CSV file and organizes the data into dictionaries based on home and away teams. The filename parameter is the path to the CSV file and columns is a list of columns to extract data from. The function returns two dictionaries containing the data for home and away teams.
toLoL(filename, columns): Similar to toDoL, this function reads a CSV file and organizes the data into lists of lists based on home and away teams. The filename parameter is the path to the CSV file and columns is a list of columns to extract data from. The function returns two lists of lists containing the data for home and away teams.
read_csv(file_path): This function reads a CSV file into a pandas DataFrame. The file_path parameter is the path to the CSV file. The function returns a DataFrame containing the CSV data. If the file is not found or an unexpected error occurs, the function prints an error message.

Variables in 'champs.csv' and 'runnerups.csv'

Year: The year the series was played
Team: The name of the team.
Win: 1 = Win. 0 = Loss
Home: 1 = Home team. 0 = Away team.
Game: Game #
MP - Total minutes played. Equals 240 (48x5=240) if game did not go to overtime. MP>240 if game went to overtime.
FG - Field goals made
FGA - Field goal attempts
FGP* - Field Goal Percentage
TP - 3 Point Field Goals Made
TPA - Three point attempts
TPP - three point percentage
FT - Free throws made
FTA - Free throws attempted
FTP - Free throw percentage
ORB - Offensive rebounds
DRB - Defensive rebounds
TRB* - Total rebounds
AST* - Assists
STL - Steals
BLK - Blocks
TOV* - Turnovers
PF - Personal fouls
PTS* - points scored
