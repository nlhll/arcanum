# import json
import os
import pandas
import send2trash
import sqlite3

# TODO: logging (console, file)
# TODO: decouple logic from Extract (dataset dir, etc.)
# TODO: json loader
# TODO: docstrings
# TODO: remove db connection from __init__


class SQLiteLoad:
    # Loader into SQLite db
    DB_DIR = '..\\database'
    DATASET_DIR = '..\\dataset'
    DB_NAME = 'db'

    # FILE_PATH = 'D:/work/arcanum/_unttld/dataset/ISO_TC 213.csv'

    def __init__(self,
                 dataset_dir,
                 db_dir,
                 db_name=DB_NAME):
        """Constructor.

        Dataset and db directories initializtion.
        List of files to load setting.
        """
        # initialize list of loads
        self.load_call = {
            '.csv': self.load_csv,
            '.json': self.load_json,
            '.sqlite': self.load_sqlite
        }

        # initialize db folder, connection and db itself
        self.dataset_dir = dataset_dir
        self.db_dir = db_dir
        try:
            os.mkdir(self.db_dir)
        except OSError:
            pass

        # get all files path's
        files = []
        # TODO: rewrite with pathlib (should become simpler)
        for (dirpath, dirnames, filenames) in os.walk(self.dataset_dir):
            files += [os.path.join(dirpath, file) for file in filenames]

        # prepare a dictionary with files' metadata
        self.files_to_load = []
        for file in files:
            file_name, file_type = os.path.splitext(file)
            self.files_to_load.append(
                {
                    'file_path': file,
                    'file_name': file_name.split('\\')[-1],
                    'file_type': file_type
                }
            )

    def delete_db_dir(self):
        """Deletion of the db directory."""
        if self.db_conn:
            self.db_conn.close()
        send2trash.send2trash(self.db_dir)

    def load_csv(self, file):
        """ .csv loader"""
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
                  .format(file['file_name'] + file['file_type']))
            print('========================================'
                  '========================================')

    def load_json(self, file):
        """ .json loader"""
        pass

    def load_sqlite(self, file):
        """ .sqlite loader"""
        db_conn = sqlite3.connect(self.db_dir + '\\' + self.db_name + '.db')
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
                    table.to_sql(table_name, db_conn,
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
                  .format(file['file_name'] + file['file_type']))
            print('========================================'
                  '========================================')

        cursor.close()
        conn.close()

    def load_wrapper(self):
        """Wrapps loads from different files types"""
        for file in self.files_to_load:
            try:
                print('The file\'s {} loading has started.'
                      .format(file['file_name'] + file['file_type']))
                print('========================================'
                      '========================================')
                self.load_call[file['file_type']](file)
            except KeyError:
                print('The file with {} extension has been skipped'
                      .format(file['file_type']))
                print('========================================'
                      '========================================')

        # TODO: remove after refactoring
        self.db_conn.close()


if __name__ == '__main__':
    ld = SQLiteLoad()
    ld.load_wrapper()
