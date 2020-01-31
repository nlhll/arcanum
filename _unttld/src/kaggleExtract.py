from kaggle.api.kaggle_api_extended import KaggleApi
import random
import send2trash

# TODO: logging (console, file)
# TODO: add subdirectory per dataset extracted =========DONE
# TODO: docstrings =========DONE


class KaggleExtract:
    """Kaggle exporter class based on official Kaggle API."""
    MAX_DATASET_SIZE = 150*1024*1024
    VALID_FILE_TYPES = ['csv', 'json', 'sqlite']
    # DOWNLOAD_DIR = '../dataset'

    def __init__(self,
                 dataset_dir,
                 dataset_name=None,
                 file_type=None
                 ):
        """Constructor.

        Kaggle API Authentication.
        Datasets' name, properties, download directory initialiaztion.
        """
        # authentication
        self.authenticate()
        # attributes set
        self.dataset_dir = dataset_dir
        self.set_file_type(file_type)
        self.set_dataset_name(dataset_name)

    def authenticate(self):
        """
        Kaggle API authentication method.

        Reading credentials from kaggle.json is chosen
        as an authentication mechanism.
        Read more on https://github.com/Kaggle/kaggle-api
        """
        try:
            self.api = KaggleApi()
            self.api.authenticate()
        except OSError as o:
            print(o.args[0])

    def delete_dataset_dir(self):
        """Deletion of the download directory."""
        send2trash.send2trash(self.dataset_dir)

    def download_dataset(self):
        """Calls Kaggle API dataset_download_files method.

        Downloads dataset from kaggle's vault.
        """
        # print(api.dataset_list_files('sobhanmoosavi/us-accidents').files)

        self.api.dataset_download_files(
            dataset=self.dataset_name,
            path=self.dataset_dir + '/' + self.dataset_name,
            unzip=True)

    def get_dataset_name(self):
        return self.dataset_name

    def set_dataset_name(self, dataset_name):
        """Dataset's name setter.

        Calls dataset's existence validation.
        Sets a name if provided,
        otherwise chooses a dataset randomly,
        using randomly generated page and index.
        """
        if dataset_name:
            self.validate_dataset_exist(dataset_name)
            self.dataset_name = dataset_name
        else:
            page = random.randint(1, 2)
            index = random.randint(1, 19)

            self.dataset_name = str(self.api.
                                    dataset_list(file_type=self.file_type,
                                                 page=page,
                                                 max_size=self.MAX_DATASET_SIZE
                                                 )[index]
                                    )

    def set_file_type(self, file_type):
        """Dataset's file extension setter.

         Calls file's extension validation.
         Sets a priority file's extension
         as a dataset's search parameter if provided,
         otherwise chooses it randomly from the default list of extensions.
         """
        if file_type:
            self.validate_file_type(file_type)
            self.file_type = file_type
        else:
            self.file_type = self.VALID_FILE_TYPES[random.randint(0, 2)]

    def validate_file_type(self, file_type):
        """Validates file's extension."""
        if file_type not in self.VALID_FILE_TYPES:
            raise ValueError('Incorrect file extension has been entered.')

    def validate_dataset_exist(self, dataset_name):
        """Validates dataset's existence."""
        search_res = str(self.api.dataset_list(search=dataset_name))

        if search_res != '[' + dataset_name + ']':
            raise ValueError('Incorrect dataset name has been entered.')


if __name__ == '__main__':
    dataset = input('Input dataset name '
                    '(Dataset URL suffix in format <owner>/<dataset-name>): ')
    if not dataset:
        file_type = input('Input primal files\' type: csv, json, sqlite. '
                          '(Note: there might be files '
                          'with other types in the dataset): ')

    exp = KaggleExtract(dataset_name=dataset,
                        file_type=file_type,
                        dataset_dir='../dataset')
    exp.download_dataset()
