# import json
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
            '.sqlite': self.load_sqlite
        }

        # initialize db folder, connection and db itself
        self.dataset_dir = dataset_dir
        self.db_dir = db_dir
        try:
            os.mkdir(self.db_dir)
        except OSError:
            pass
        self.db_conn = sqlite3.connect(db_dir + '\\' + db_name + '.db')

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
        if self.db_conn:
            self.db_conn.close()
        send2trash.send2trash(self.db_dir)

    def load_csv(self, file):
        # .csv loader
        table_name = file['file_name']

        try:
            csv_conn = pandas.read_csv(file['file_path'])
            csv_conn.to_sql(table_name, self.db_conn,
                            if_exists='replace', index=False)
        except pandas:
            print('The file {} is corrupted. the loading has been skipped.'
                  .format(file['file_name']))
            print('========================================'
                  '========================================')
        else:
            print('The file {} has been loaded.'
                  .format(file['file_name'] + file['file_ext']))
            print('========================================'
                  '========================================')

    def load_json(self, file):
        # .json loader
        pass

    def load_sqlite(self, file):
        # .sqlite loader
        conn = sqlite3.connect(file['file_path'])
        cursor = conn.cursor()
        table_name = file['file_name']

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        tables_meta = cursor.fetchall()
        try:
            for tab_meta in tables_meta:
                try:
                    table_name = tab_meta[0]
                    table = pandas.read_sql_query("SELECT * from %s"
                                                  % table_name, conn)
                    table.to_sql(table_name, self.db_conn,
                                 if_exists='replace', index=False)
                except pandas:
                    print('The table {} is corrupted. '
                          'The loading has been skipped.'.format(table_name))
                    print('========================================'
                          '========================================')
                else:
                    print('The table {} has been loaded.'.format(table_name))
                    print('========================================'
                          '========================================')
        except all():
            print('The file {} hasn\'t been loaded succesfully'
                  .format(file['file_name']))
            print('========================================'
                  '========================================')
        else:
            print('The file {} has been loaded.'
                  .format(file['file_name'] + file['file_ext']))
            print('========================================'
                  '========================================')

        cursor.close()
        conn.close()

    def load_wrapper(self):
        # Wrapps loads from different files types
        for file in self.files_to_load:
            try:
                print('The file\'s {} loading has started.'
                      .format(file['file_name'] + file['file_ext']))
                print('========================================'
                      '========================================')
                self.load_call[file['file_ext']](file)
            except KeyError:
                print('The file with {} extension has been skipped'
                      .format(file['file_ext']))
                print('========================================'
                      '========================================')

        self.db_conn.close()


if __name__ == '__main__':
    ld = SQLiteLoad()
    ld.load_wrapper()
