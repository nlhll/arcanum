import os
import pandas
import sqlite3

class SQLiteLoad:
    # Loader into SQLite db
    DB_DIR = '..\\database'
    DATASET_DIR = '..\\dataset'
    DB_NAME = 'db'
    # FILE_PATH = 'D:/work/arcanum/_unttld/dataset/ISO_TC 213.csv'

    def __init__(self,
                 dataset_dir=DATASET_DIR,
                 db_dir=DB_DIR,
                 db_name=DB_NAME):

        self.dataset_dir = dataset_dir

        self.db_dir = db_dir
        try:
            os.mkdir(self.db_dir)
        except OSError:
            pass

        self.conn = sqlite3.connect(db_dir + '\\' + db_name + '.db')

        self.files_to_load = []
        file_dir = next(os.walk(self.dataset_dir))[2]
        for file in file_dir:
            file_name, file_ext = os.path.splitext(file)
            self.files_to_load.append(
                {
                    'file_name': file_name,
                    'file_ext': file_ext
                }
            )

    def load_csv(self, file_name):
        table_name = file_name.split('\\')[-1]
        csv_conn = pandas.read_csv(self.dataset_dir + '\\' + file_name + '.csv')
        csv_conn.to_sql(table_name, self.conn, if_exists='append', index=False)

    def load_wrapper(self):
        for file in self.files_to_load:
            if 
            self.load_csv(file['file_name'])

ld = SQLiteLoad()
ld.load_wrapper()

