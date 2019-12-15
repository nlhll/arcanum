from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

print(api.dataset_list(search='sobhanmoosavi/us-accidents').)

#print(api.dataset_list_files('sobhanmoosavi/us-accidents').)
