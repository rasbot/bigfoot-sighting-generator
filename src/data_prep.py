import pandas as pd
import json


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
