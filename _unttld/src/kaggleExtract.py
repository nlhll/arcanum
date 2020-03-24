from kaggle.api.kaggle_api_extended import KaggleApi
import logging
from loggingConfig import LoggingConfig
import random
import send2trash

# TODO: logging (console, file) =========DONE
# TODO: add subdirectory per dataset extracted =========DONE
# TODO: docstrings =========DONE


class KaggleExtract:
    """Kaggle exporter class based on official Kaggle API."""
    MAX_DATASET_SIZE = 150*1024*1024
    VALID_FILE_TYPES = ['csv', 'json', 'sqlite']

    LoggingConfig(__name__)
    LOGGER = logging.getLogger(__name__)

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
        self.set_dataset_name(dataset_name, file_type)

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
            self.LOGGER.error(o.args[0])

    def delete_dataset_dir(self):
        """Deletion of the download directory."""
        send2trash.send2trash(self.dataset_dir)

    def download_dataset(self):
        """Calls Kaggle API dataset_download_files method.

        Downloads dataset from kaggle's vault.
        """
        # print(api.dataset_list_files('sobhanmoosavi/us-accidents').files)
        self.LOGGER.info('A download of [' + self.dataset_name +
                         '] dataset has started.')
        try:
            self.api.dataset_download_files(
                dataset=self.dataset_name,
                path=self.dataset_dir + '/' + self.dataset_name,
                unzip=True)
            self.LOGGER.info('The [' + self.dataset_name +
                             '] dataset has been downloaded.')
        except Exception:
            self.LOGGER.error('The download of [' + self.dataset_name +
                              '] dataset has failed')

    def get_dataset_name(self):
        return self.dataset_name

    def set_dataset_name(self, dataset_name, file_type):
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
            true_file_type = self.form_file_type(file_type)

            self.dataset_name = str(self.api.
                                    dataset_list(file_type=true_file_type,
                                                 page=page,
                                                 max_size=self.MAX_DATASET_SIZE
                                                 )[index]
                                    )

    def form_file_type(self, file_type):
        """Dataset's file extension setter.

         Calls file's extension validation.
         Sets a priority file's extension
         as a dataset's search parameter if provided,
         otherwise chooses it randomly from the default list of extensions.
         """
        if file_type:
            self.validate_file_type(file_type)
            true_file_type = file_type
        else:
            true_file_type = self.VALID_FILE_TYPES[random.randint(0, 2)]
        return true_file_type

    def validate_file_type(self, file_type):
        """Validates file's extension."""
        if file_type not in self.VALID_FILE_TYPES:
            self.LOGGER.error('Incorrect file extension has been entered.')
            raise ValueError

    def validate_dataset_exist(self, dataset_name):
        """Validates dataset's existence."""
        try:
            search_res = str(self.api.dataset_list(search=dataset_name))
            try:
                if search_res != '[' + dataset_name + ']':
                    raise ValueError
            except ValueError:
                self.LOGGER.error('Incorrect dataset name has been entered.')
        except Exception:
            self.LOGGER.warning('Something went wrong in retrieving '
                                'Kaggle API dataset list')


if __name__ == '__main__':
    dataset = input('Input dataset name '
                    '(Dataset URL suffix in format <owner>/<dataset-name>): ')
    file_type = None
    if not dataset:
        file_type = input('Input primal files\' type: csv, json, sqlite. '
                          '(Note: there might be files '
                          'with other types in the dataset): ')

    exp = KaggleExtract(dataset_name=dataset,
                        file_type=file_type,
                        dataset_dir='../dataset')
    exp.download_dataset()
