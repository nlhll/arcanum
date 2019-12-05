from kaggle.api.kaggle_api_extended import KaggleApi
import random

# Reading credentials from kaggle.json is chosen
# as an authentication mechanism.
# Read more on https://github.com/Kaggle/kaggle-api
try:
    api = KaggleApi()
    api.authenticate()
except OSError as o:
    print(o.args[0])

MAX_SIZE = 512*1024*1024
VALID_DATASET_TYPES = ['csv', 'json', 'sqlite']

'''
def valid_files(files, valid_types):
    for file in files, type in valid_types:
        if type 
'''
pg = random.randint(1, 2)
ix = random.randint(1, 19)
file_type = VALID_DATASET_TYPES[random.randint(0, 2)]

dataset_suff = str(api.dataset_list(file_type=file_type, page=pg, max_size=MAX_SIZE)[ix])
print(dataset_suff)

print(api.dataset_list_files(dataset_suff))
#api.dataset_download_files(dataset=dataset_suff, path=r'..\src\test', unzip=True)
