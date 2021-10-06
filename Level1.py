import os
import re
import pandas as pd



class Comb:
    def __init__(self, data_path, output_path):
        self.files = os.listdir(data_path)
        self.path = data_path
        output_columns = ['user_id', 'first_name', 'last_name', 'births', 'img_path']
        users_data = []
        for file in self.files:
            ext = re.search(r'([^.]*)$', file)[1].lower()
            user_id = re.search(r'^([^.]*)', file)[1].lower()
            if ext == 'csv':
                user_info = self.read_csv(file)
                user_info.insert(0, user_id)
                if f'{user_id}.png' in self.files:
                    user_info.append(f'{data_path}\\{user_id}.png')
                else:
                    user_info.append('no_picture')
                users_data.append(user_info)
        df = pd.DataFrame(users_data, columns=output_columns)
        df.set_index('user_id', inplace=True)
        df.to_csv(f'{output_path}\\output.csv')



    def read_csv(self, csv):
        df = pd.read_csv(f'{self.path}\\' + csv)
        info = df.values.tolist()[0]
        return info


if __name__ == '__main__':
    Comb(data_path='src_data', output_path='processed_data')
