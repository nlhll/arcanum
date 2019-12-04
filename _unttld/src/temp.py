from kaggle.api.kaggle_api_extended import KaggleApi
import random

# Reading credentials from kaggle.json is chosen
# as an authentication mechanism.
# Read more https://github.com/Kaggle/kaggle-api
try:
    api = KaggleApi()
    api.authenticate()
except OSError as o:
    print(o.args[0])


pg = random.randint(1, 500)
ix = random.randint(1, 20)

print(api.dataset_list(page=pg)[ix])
