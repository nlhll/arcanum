import json
import os
import pandas
import send2trash
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

        # initialize list of loads
        self.load_call = {
            '.csv': self.load_csv,
            # '.json': self.load_json
        }

        # initialize db folder, connection and db itself
        self.dataset_dir = dataset_dir
        self.db_dir = db_dir
        try:
            os.mkdir(self.db_dir)
        except OSError:
            pass
        self.conn = sqlite3.connect(db_dir + '\\' + db_name + '.db')

        # get all files path's
        files = []
        for (dirpath, dirnames, filenames) in os.walk(self.dataset_dir):
            files += [os.path.join(dirpath, file) for file in filenames]

        # prepare a dictionary with files' metadata
        self.files_to_load = []
        for file in files:
            file_name, file_ext = os.path.splitext(file)
            self.files_to_load.append(
                {
                    'file_path': file,
                    'file_name': file_name.split('\\')[-1],
                    'file_ext': file_ext
                }
            )

    def delete_db_dir(self):
        if self.conn:
            self.conn.close()
        send2trash.send2trash(self.db_dir)

    def load_csv(self, file):
        # .csv loader
        table_name = file['file_name']

        try:
            csv_conn = pandas.read_csv(file['file_path'])
            csv_conn.to_sql(table_name, self.conn, if_exists='append', index=False)
        except pandas:
            print('The file {} is corrupted. the loading is skipped.'.format(file['file_name']))
        else:
            print('The file {} has been loaded.'.format(file['file_name'] + file['file_ext']))

    def load_json(self, file):
        # .json loader
        table_name = file['file_name']
        df = pandas.read_json(open(file['file_path']))
        df.to_sql(table_name, self.conn, if_exists='append', index=False)

    def load_wrapper(self):
        # Wrapps loads from different files types
        for file in self.files_to_load:
            try:
                self.load_call[file['file_ext']](file)
            except KeyError:
                print('The file with {} extension was skipped'
                      .format(file['file_ext']))


if __name__ == '__main__':
    ld = SQLiteLoad()
    ld.load_wrapper()
