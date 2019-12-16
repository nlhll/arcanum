from kaggle.api.kaggle_api_extended import KaggleApi
# import os
import random


class KaggleExport:
    # Kaggle exporter class based on official Kaggle API
    MAX_DATASET_SIZE = 150*1024*1024
    VALID_DATASET_TYPES = ['csv', 'json', 'sqlite']
    DOWNLOAD_DIR = '..\\dataset'
    # os.path.abspath(os.curdir) + '\\datasets'

    def __init__(self,
                 max__dataset_size=MAX_DATASET_SIZE,
                 dataset_suff=None,
                 file_type=None,
                 download_dir=DOWNLOAD_DIR
                 ):
        # authentication
        self.authenticate()

        # attributes set
        self.download_dir = download_dir

        if dataset_suff:
            self.validate_dataset_exist(dataset_suff)
            self.dataset_suff = dataset_suff
        else:
            page = random.randint(1, 2)
            index = random.randint(1, 19)

            if file_type:
                self.validate_file_type(file_type)
                self.file_type = file_type
            else:
                self.file_type = self.VALID_DATASET_TYPES[random.randint(0, 2)]

            self.dataset_suff = str(self.api.
                                    dataset_list(file_type=self.file_type,
                                                 page=page,
                                                 max_size=self.MAX_DATASET_SIZE
                                                 )[index]
                                    )

    def authenticate(self):
        # Reading credentials from kaggle.json is chosen
        # as an authentication mechanism.
        # Read more on https://github.com/Kaggle/kaggle-api
        try:
            self.api = KaggleApi()
            self.api.authenticate()
        except OSError as o:
            print(o.args[0])

    def validate_file_type(self, file_type):
        if file_type not in self.VALID_DATASET_TYPES:
            raise ValueError('Incorrect file type has been entered.')

    def validate_dataset_exist(self, dataset_suff):
        search_res = str(self.api.dataset_list(search=dataset_suff))

        if search_res != '[' + dataset_suff + ']':
            raise ValueError('Incorrect dataset suffix has been entered.')

    def download_dataset(self):
        # Download dataset from kaggle's vault
        # print(api.dataset_list_files('sobhanmoosavi/us-accidents').files)
        self.api.dataset_download_files(
            dataset=self.dataset_suff,
            path=self.download_dir,
            unzip=True)


dataset = input('Input dataset suffix '
                '(Dataset URL suffix in format <owner>/<dataset-name>): ')
if not dataset:
    file_type = input('Input primal files\' type: csv, json, sqlite. '
                      '(Note: there might be files '
                      'with other types in the dataset): ')

exp = KaggleExport(dataset_suff=dataset, file_type=file_type)
exp.download_dataset()