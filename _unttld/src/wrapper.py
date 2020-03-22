from kaggleExtract import KaggleExtract
from sqliteLoad import SQLiteLoad
# TODO: argparse or click command-line args (full-functional console interface

DB_DIR = '..\\database'
DATASET_DIR = '..\\dataset'
file_type = None
dataset = input('Input dataset suffix '
                '(Dataset URL suffix in format <owner>/<dataset-name>): ')
if not dataset:
    file_type = input('Input primal files\' type: csv, json, sqlite. '
                      '(Note: there might be files '
                      'with other types in the dataset): ')


extractor = KaggleExtract(dataset_dir=DATASET_DIR, dataset_name=dataset,
                          file_type=file_type)
extractor.download_dataset()
dataset_name = extractor.get_dataset_name()
dataset_path = DATASET_DIR + '/' + dataset_name

loader = SQLiteLoad(dataset_dir=dataset_path, db_dir=DB_DIR)
loader.load_wrapper()

extractor.delete_dataset_dir()
loader.delete_db_dir()
