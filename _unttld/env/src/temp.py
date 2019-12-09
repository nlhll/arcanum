from kaggle.api.kaggle_api_extended import KaggleApi
import random

# Reading credentials from kaggle.json is chosen
# as an authentication mechanism.
# Read more on https://github.com/Kaggle/kaggle-api

class KaggleExport():

    MAX_SIZE = 512*1024*1024
    VALID_DATASET_TYPES = ['csv', 'json', 'sqlite']

    def __init__(self):
        try:
            api = KaggleApi()
            api.authenticate()
        except OSError as o:
            print(o.args[0])

    def set_dataset(self, dataset=None, file_type=None):
        if not dataset:
            self.page = random.randint(1, 2)
            self.index = random.randint(1, 19)

            if file_type:
                self.file_type = file_type
            else:
                self.file_type = VALID_DATASET_TYPES[random.randint(0, 2)]
        else:
            self.datset_suff = dataset


    #dataset_suff = str(api.dataset_list(file_type=self.file_type, page=self.page, max_size=MAX_SIZE)[self.index])

    #a = api.dataset_list_files(dataset_suff).files

    #dir_dataset = '..\src\datasets\\' + dataset_suff

    #api.dataset_download_files(dataset=dataset_suff, path=dir_dataset, unzip=True)
