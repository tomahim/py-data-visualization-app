import os
import pandas as pd
import zipfile

usa_states = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'
}


class DataReader:
    df = None

    _file_path = '../resources/gun-violence-data_01-2013_03-2018.csv'

    def __init__(self):
        self._init_data_frame()

    def _init_data_frame(self):
        current_folder = os.path.dirname(os.path.abspath(__file__))
        with zipfile.ZipFile(os.path.join(current_folder, self._file_path) + '.zip', "r") as zip_ref:
            zip_ref.extractall(os.path.join(current_folder, '..', 'resources'))
            absolute_file_path = os.path.join(current_folder, self._file_path)
            self.df = pd.read_csv(absolute_file_path)
            self.df['year'] = pd.DatetimeIndex(self.df['date']).year
            self.df['state_code'] = self._get_state_code_column()

    def _get_state_code_column(self):
        return self.df['state'] \
            .apply(lambda x: list(usa_states.keys())[
            list(usa_states.values()).index(x)] if x != 'District of Columbia' else 'MD')

    def get_nb_injured_and_killed_by_year(self):
        from_2014_to_2017 = self.df[(self.df.year >= 2014) & (self.df.year <= 2017)]
        return from_2014_to_2017.groupby("year")[["n_injured", "n_killed"]].sum()

    def get_nb_injured_and_killed_by_state(self):
        from_2014_to_2017 = self.df[(self.df.year >= 2014) & (self.df.year <= 2017)]
        data_frame = from_2014_to_2017.groupby("state_code")[["n_injured", "n_killed"]].sum()
        data_frame['total_injured_killed'] = data_frame['n_injured'] + data_frame['n_killed']
        return data_frame


if __name__ == '__main__':
    data_reader = DataReader()
    df = data_reader.get_nb_injured_and_killed_by_state()
    print(df)
