import pandas as pd
from sqlalchemy import create_engine
from flask import Flask
from flask_restful import Api, Resource, reqparse
import psycopg2
import json
from Level1 import Comb

app = Flask(__name__)
api = Api(app)


class Json(Resource):
    def get(self, min_age, max_age):
        parser = reqparse.RequestParser()
        parser.add_argument('is_image_exists')
        params = parser.parse_args()
        image_par = params['is_image_exists'].lower()
        if image_par != None and image_par not in ['true', 'false']:
            return 'is_image_exists should be true or false', 400
        elif image_par == None:
            return 'please specify is_image_exist. It should be true or false', 400
        conn = psycopg2.connect(dbname='postgres',
                                user='postgres',
                                password='postgres',
                                host='localhost', port=5432)
        cursor = conn.cursor()
        cursor.execute("""select *, extract(year from age(now()::timestamp, to_timestamp(births/1000)))
                                  , case when img_path!= 'no_picture' then 'True' else 'False' end img from users""")
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        results = {i[1]: {'first_name': i[2],
                          'last_name': i[3],
                          'birth': i[4],
                          'picture': i[5],
                          'age': i[6]} for i in records if min_age <= i[6] <= max_age and i[7].lower() == image_par}
        return json.dumps(results), 200

    def post(self):
        Comb(data_path='src_data', output_path='processed_data')
        engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
        df = pd.read_csv('processed_data\\output.csv')
        df.to_sql('users', engine, if_exists='replace')
        return 'Data was updated', 201


api.add_resource(Json,
                 "/data/<int:min_age>/<int:max_age>",
                 "/data")
if __name__ == '__main__':
    app.run(debug=True)
