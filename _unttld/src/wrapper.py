import click
from kaggleExtract import KaggleExtract
from sqliteLoad import SQLiteLoad
# TODO: argparse or click command-line args (full-functional console interface
#  ========DONE


@click.command()
@click.option('--dataset_dir', default='..\\dataset',
              help='A dataset path')
@click.option('--db_dir', default='..\\database',
              help='A database path')
@click.option('--dataset_name', default=None,
              help='A Dataset URL suffix in format <owner>/<dataset-name>')
@click.option('--file_type', default=None,
              help='An expected extension of dataset\'s files (csv, json, sqlite)')
@click.option('--del_after', default=1,
              help='A flag whether dataset and db folder have t be deleted after')
def execute_etl(dataset_dir, db_dir, dataset_name, file_type, del_after):
    extractor = KaggleExtract(dataset_dir=dataset_dir,
                              dataset_name=dataset_name, file_type=file_type)
    extractor.download_dataset()

    dataset_name = extractor.get_dataset_name()
    dataset_path = dataset_dir + '/' + dataset_name

    loader = SQLiteLoad(dataset_dir=dataset_path, db_dir=db_dir)
    loader.load_wrapper()

    if del_after == 1:
        extractor.delete_dataset_dir()
        loader.delete_db_dir()


if __name__ == '__main__':
    execute_etl()


