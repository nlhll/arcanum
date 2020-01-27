from kaggleExtract import KaggleExtract
from sqliteLoad import SQLiteLoad
# TODO: argparse or click command-line args (full-functional console interface

DOWNLOAD_DIR = '..\\dataset'
dataset = input('Input dataset suffix '
                '(Dataset URL suffix in format <owner>/<dataset-name>): ')
if not dataset:
    file_type = input('Input primal files\' type: csv, json, sqlite. '
                      '(Note: there might be files '
                      'with other types inthe dataset): ')


extractor = KaggleExtract()
extractor.download_dataset()
loader = SQLiteLoad()
loader.load_wrapper()

#extractor.delete_download_dir()
#loader.delete_db_dir()
