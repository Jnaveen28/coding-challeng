import pymysql
import sys
import shutil
import os

def move_files(source_folder, destination_folder):
    for file_name in os.listdir(source_folder):
        source = source_folder + file_name
        destination = destination_folder + file_name
        if os.path.isfile(source):
            shutil.move(source, destination)
            print('Moved:', file_name)

def load_to_mysql(path, table):
    try:
        con = pymysql.connect(host='localhost',
                                user='root',
                                password='test1234',
                                autocommit=True,
                                local_infile=1)
        cursor = con.cursor()
        for file in os.listdir(path):
            if table == 'yield':
                load_sql = f"LOAD DATA LOCAL INFILE '{path}{file}' INTO TABLE coding_exercise.{table}"
                cursor.execute(load_sql)
            elif table == 'weather':
                trunc_sql = f"TRUNCATE TABLE coding_exercise.{table}_stage"
                cursor.execute(trunc_sql)
                load_sql = f"LOAD DATA LOCAL INFILE '{path}{file}' INTO TABLE coding_exercise.{table}_stage SET location_id = '{file.split('.')[0]}'"
                cursor.execute(load_sql)
                stats_sql = f"""INSERT INTO coding_exercise.{table}_stats 
                select `year`, location_id, max(max_tmp) as max_tmp, min(min_tmp) as min_tmp, avg(precipitation) as avg_prep from (
                select *, year(`date`) as `year` from coding_exercise.{table}_stage 
                union
                select *, '' as date from coding_exercise.{table}_stats where location_id = '{file.split('.')[0]}') k group by location_id, `year`
                """
                cursor.execute(stats_sql)
                insert_sql = f"INSERT INTO coding_exercise.{table} SELECT * FROM coding_exercise.{table}_stage"
                cursor.execute(insert_sql)
        con.close()
    except Exception as e:
        print('Error: {}'.format(str(e)))
        sys.exit(1)

load_to_mysql('../../yld_data/', 'yield')
move_files('../../yld_data/', '../../data_backup/')

load_to_mysql('../../wx_data/', 'weather')
move_files('../../wx_data/', '../../data_backup/')