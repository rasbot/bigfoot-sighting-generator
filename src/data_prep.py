import pandas as pd
import json
import numpy as np


def import_data(filepath):
    """
    Imports data from a json file.

            Parameters:
                    filepath (str): Filepath to the json file.

            Returns:
                    reports (dict): A dictionary of all web scraped reports.
    """
    reports = []
    with open(filepath, "r") as f:
        data = f.read()
        reports = json.loads(data)
    return reports


def create_df(reports):
    """
    Creates a dataframe from a dictionary.

            Parameters:
                    reports (dict): A dictionary of all web scraped reports.

            Returns:
                    reports_df (dataframe): A dataframe of sighting reports.
    """
    df = pd.DataFrame.from_dict(reports)
    features = ['YEAR', 'SEASON', 'MONTH', 'STATE', 'COUNTY', 'LOCATION DETAILS',
                'NEAREST TOWN', 'NEAREST ROAD', 'OBSERVED', 'ALSO NOTICED',
                'OTHER WITNESSES', 'OTHER STORIES', 'TIME AND CONDITIONS',
                'ENVIRONMENT', 'DATE']
    df = df.loc[features]
    reports_df = df.transpose()
    return reports_df


def get_bag_of_words(df, feature, folder):
    """
    Creates a bag of words for a feature column.

        Parameters:
                df (dataframe): A dataframe of the sightings data.
                feature (str): The name of the feature column to extract.
                folder (str): Folder to store the txt file.

        Returns:
                None.
    """
    sub_df = df.loc[df[feature].notnull()][feature]
    s = ""
    for i in sub_df:
        s = s + i
    text_file = open(f"{folder}/{feature}.txt", "w", encoding="utf-8")
    text_file.write(s)
    text_file.close()


def get_state_data(df, folder):
    """
    From the main dataframe, gets a list of unique states that have had sightings
    and creates a dictionary that has counties, nearest towns, and nearest roads
    associated with sightings from those states. Writes the dictionary to a json
    file called 'states.json'.

        Parameters:
                df (dataframe): The main sightings dataframe
                folder (str): The folder where the json file is stored.

        Returns:
                None.
    """
    unique_states = np.unique(np.array(df['STATE'].dropna()))
    idx = np.argwhere(unique_states == '(International)')
    unique_states = np.delete(unique_states, idx)

    counties_d, nearest_town_d, nearest_road_d = dict(), dict(), dict()
    for i in range(len(unique_states)):
        counties_d[unique_states[i]] = np.unique(
            df[df.STATE == unique_states[i]]['COUNTY'].dropna()).tolist()
        nearest_town_d[unique_states[i]] = np.unique(
            df[df.STATE == unique_states[i]]['NEAREST TOWN'].dropna()).tolist()
        nearest_road_d[unique_states[i]] = np.unique(
            df[df.STATE == unique_states[i]]['NEAREST ROAD'].dropna()).tolist()
    d = dict()
    for i in unique_states:
        d[i] = {"Counties": counties_d[i],
                "Nearest Town": nearest_town_d[i],
                "Nearest Road": nearest_road_d[i]}

    with open(f"{folder}/states.json", "w") as f:
        json.dump(d, f, indent=4, sort_keys=False)
