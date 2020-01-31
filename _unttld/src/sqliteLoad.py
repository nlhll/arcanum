import json
import pandas
from pathlib import Path
import send2trash
import sqlite3

# TODO: logging (console, file)
# TODO: decouple logic from Extract (dataset dir, etc.) =========DONE
# TODO: json loader =========DONE
# TODO: docstrings =========DONE
# TODO: remove db connection from __init__ =========DONE


class SQLiteLoad:
    # Loader into SQLite db
    # DB_DIR = '..\\database'
    # DATASET_DIR = '..\\dataset'
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
            '.csv':     self.load_csv,
            '.json':    self.load_json,
            '.sqlite':  self.load_sqlite
        }

        # initialize db folder, connection and db itself
        self.db_name = db_name
        self.db_dir = db_dir
        Path(self.db_dir).mkdir(exist_ok=True)

        self.dataset_dir = dataset_dir
        # get all files path's
        # TODO: rewrite with pathlib (should become simpler) =========DONE
        files = [str(f) for f in Path(self.dataset_dir).rglob('*')
                 if f.is_file()]

        # prepare a dictionary with files' metadata
        self.files_to_load = []
        for file in files:
            self.files_to_load.append(
                {
                    'path': file,
                    'name': Path(file).stem,
                    'type': Path(file).suffix
                }
            )

    def delete_db_dir(self):
        """Deletion of the db directory."""
        send2trash.send2trash(self.db_dir)

    def load_csv(self, file):
        """ .csv loader"""
        db_conn = sqlite3.connect(self.db_dir + '\\' + self.db_name + '.db')
        table_name = file['name']

        try:
            csv_conn = pandas.read_csv(file['path'])
            csv_conn.to_sql(table_name, db_conn,
                            if_exists='replace', index=False)
        except pandas:
            print('The file {} is corrupted. the loading has been skipped.'
                  .format(file['name']))
            print('========================================'
                  '========================================')
        else:
            print('The file {} has been loaded.'
                  .format(file['name'] + file['type']))
            print('========================================'
                  '========================================')

        db_conn.commit()
        db_conn.close()

    def load_json(self, file):
        """ .json loader"""
        # get file name w/o extension
        table_name = '[' + file['name'] + ']'

        # create a table
        db_conn = sqlite3.connect(self.db_dir + '\\' + self.db_name + '.db')
        cur = db_conn.cursor()
        cur.execute('DROP TABLE IF EXISTS ' + table_name)
        cur.execute('CREATE TABLE ' + table_name + ' (data TEXT)')

        try:
            # deserialize json file
            with open(file['path'], 'r') as jread:
                json_data = json.load(jread)

            cur.execute('INSERT INTO ' + table_name + ' VALUES(?)',
                        [str(json_data)])

        except all():
            print('The file {} hasn\'t been loaded succesfully.'
                  .format(file['name']))
            print('========================================'
                  '========================================')
        else:
            print('The file {} has been loaded succesfully.'
                  .format(file['name'] + file['type']))
            print('========================================'
                  '========================================')

        db_conn.commit()
        db_conn.close()

    def load_sqlite(self, file):
        """ .sqlite loader"""
        db_conn = sqlite3.connect(self.db_dir + '\\' + self.db_name + '.db')
        conn = sqlite3.connect(file['path'])
        cursor = conn.cursor()
        table_name = file['name']

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        tables_meta = cursor.fetchall()
        try:
            for tab_meta in tables_meta:
                try:
                    table_name = tab_meta[0]
                    table = pandas.read_sql_query("SELECT * FROM [%s]"
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
                  .format(file['name']))
            print('========================================'
                  '========================================')
        else:
            print('The file {} has been loaded.'
                  .format(file['name'] + file['type']))
            print('========================================'
                  '========================================')

        cursor.close()
        conn.close()
        db_conn.commit()
        db_conn.close()

    def load_wrapper(self):
        """Wrapps loads from different files types"""
        for file in self.files_to_load:
            try:
                print('The file\'s {} loading has started.'
                      .format(file['name'] + file['type']))
                print('========================================'
                      '========================================')
                self.load_call[file['type']](file)
            except KeyError:
                print('The file with {} extension has been skipped'
                      .format(file['type']))
                print('========================================'
                      '========================================')


if __name__ == '__main__':
    # DB_DIR = '..\\database'
    # DATASET_DIR = '..\\dataset'
    ld = SQLiteLoad(db_dir='..\\database', dataset_dir='..\\dataset')
    ld.load_wrapper()
