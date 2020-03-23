import click
from kaggleExtract import KaggleExtract
from sqliteLoad import SQLiteLoad
# TODO: argparse or click command-line args (full-functional console interface

dataset = input('Input dataset suffix '
                '(Dataset URL suffix in format <owner>/<dataset-name>): ')
if not dataset:
    file_type = input('Input primal files\' type: csv, json, sqlite. '
                      '(Note: there might be files '
                      'with other types in the dataset): ')
@click.group()
def cli():
    pass

@click.command()
@click.argument('dataset_dir', default='..\\dataset',
                help='A dataset path')
@click.argument('db_dir', default='..\\database',
                help='A database path')
@click.option('--dataset_name', default=None,
              help='A Dataset URL suffix in format <owner>/<dataset-name>')
@click.option('--file_type', default=None,
              help='An expected extension of dataset\'s files')
def execute_etl(dataset_dir, db_dir, dataset_name, file_type):
    extractor = KaggleExtract(dataset_dir=dataset_dir,
                              dataset_name=dataset_name, file_type=file_type)
    extractor.download_dataset()
    dataset_name = extractor.get_dataset_name()
    dataset_path = dataset_dir + '/' + dataset_name

    loader = SQLiteLoad(dataset_dir=dataset_path, db_dir=db_dir)
    loader.load_wrapper()


@click.command()
def delete_dataset_dir():
    extractor.delete_dataset_dir()
    loader.delete_db_dir()
