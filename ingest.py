import os
import logging
import psycopg2
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import models
from database import engine

models.Base.metadata.create_all(bind=engine)


def load_file_data():
    try:
        logging.basicConfig(
            level=logging.DEBUG,
            format='[%(asctime)s] [%(levelname)s] - %(message)s',
            filename='info.log'
        )

        start_time = datetime.now()

        folder = 'data/wx_data'
        file_list = os.listdir(folder)

        load_dotenv()
        db_params = {
            'dbname': os.getenv("DB_NAME"),
            'user': os.getenv("USERNAME"),
            'password': os.getenv("PASSWORD"),
            'host': os.getenv("DB_HOST"),
            'port': os.getenv("DB_PORT")
        }

        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        insert_into_weather = "INSERT INTO weather (date, maximum_temp, minimum_temp," \
                              " precipitation, station) VALUES (%s, %s, %s, %s, %s)"

        for file_name in file_list:
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder, file_name)
                all_records = []
                station_name = Path(file_path).stem

                with open(file_path, 'r') as f:
                    for line in f:
                        data = line.strip().split('\t')
                        if '-9999' in data:
                            continue
                        else:
                            temp_line = []
                            for idx, cell in enumerate(data):
                                if idx == 0:
                                    temp_line.append(datetime.strptime(str(cell), '%Y%m%d').date())
                                else:
                                    temp_line.append(int(cell.strip()))
                            temp_line.append(station_name)
                            all_records.append(temp_line)
                for record in all_records:
                    cursor.execute(insert_into_weather, record)
                end_time = datetime.now()
                logging.info(f'Start time {start_time}, End time {end_time}, Inserted Records {len(all_records)}')
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(str(e))
        logging.error(str(e))


def calculate_stats_data():
    try:
        load_dotenv()
        db_params = {
            'dbname': os.getenv("DB_NAME"),
            'user': os.getenv("USERNAME"),
            'password': os.getenv("PASSWORD"),
            'host': os.getenv("DB_HOST"),
            'port': os.getenv("DB_PORT")
        }
        insert_into_stats_query = '''
            INSERT INTO analysis (avg_max_temperature, avg_min_temperature, total_precipitation, station, year)
            SELECT
                AVG(maximum_temp / 10) AS avg_max_temperature,
                AVG(minimum_temp / 10) AS avg_min_temperature,
                SUM(precipitation / 100.0) AS total_precipitation,
                station,
                date_part('year', date) as year
            FROM
                weather
            WHERE
                maximum_temp IS NOT NULL
                AND minimum_temp IS NOT NULL
                AND precipitation IS NOT NULL
            GROUP BY
                year, station;
             '''

        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        cursor.execute(insert_into_stats_query)
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(str(e))


load_file_data()
calculate_stats_data()
