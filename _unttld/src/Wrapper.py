from KaggleExtract import KaggleExtract
from SQLiteLoad import SQLiteLoad

'''
dataset = input('Input dataset suffix '
                '(Dataset URL suffix in format <owner>/<dataset-name>): ')
if not dataset:
    file_type = input('Input primal files\' type: csv, json, sqlite. '
                      '(Note: there might be files '
                      'with other types inthe dataset): ')
'''
extractor = KaggleExtract()
extractor.download_dataset()
loader = SQLiteLoad()
loader.load_wrapper()
