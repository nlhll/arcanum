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

MAX_SIZE = 524288

pg = random.randint(1, 500)
ix = random.randint(1, 20)

dataset_suff = str(api.dataset_list(page=pg, max_size=MAX_SIZE)[ix])

api.dataset_download_files(dataset=dataset_suff, path=r'..\src\test', unzip=True)
print(dataset_suff)
