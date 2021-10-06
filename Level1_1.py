import os
import re
import pandas as pd
from minio import Minio
from io import BytesIO


class Comb:
    def __init__(self, data_path, output_path):

        client = Minio('127.0.0.1:9000',
                            access_key='minio-access-key',
                            secret_key='minio-secret-key',
                            secure=False)
        files = client.list_objects('datalake', prefix=data_path, recursive=True)
        output_columns = ['user_id', 'first_name', 'last_name', 'births', 'img_path']
        users_data = []
        file_list = []
        for file in files:
            file_list.append(file.object_name)
        for file in file_list:
            obj = client.get_object('datalake', file)
            ext = re.search(r'([^.]*)$', file)[1].lower()
            user_id = re.search(r'\w/([^.]*)', file)[1].lower()
            if ext == 'csv':
                user_info = self.read_csv(obj)
                user_info.insert(0, user_id)
                if f'src_data/{user_id}.png' in file_list:
                    user_info.append(f'{file}.png')
                else:
                    user_info.append('no_picture')
                users_data.append(user_info)
        df = pd.DataFrame(users_data, columns=output_columns)
        df.set_index('user_id', inplace=True)
        result = df.to_csv().encode('utf-8')
        client.put_object('datalake',
                          f'{output_path}/output.csv',
                          data=BytesIO(result),
                          length=len(result),
                          content_type='application/csv')

    def read_csv(self, csv):
        df = pd.read_csv(csv)
        info = df.values.tolist()[0]
        return info


if __name__ == '__main__':
    Comb(data_path='src_data', output_path='processed_data')
