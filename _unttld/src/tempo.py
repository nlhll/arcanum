import os
import pathlib

DATASET_DIR = '..\\dataset'

files_to_load = list()
for (dirpath, dirnames, filenames) in os.walk(DATASET_DIR):
    files_to_load += [os.path.join(dirpath, file) for file in filenames]

print(type(files_to_load))
a = []
for file in files_to_load:
    file_name, file_ext = os.path.splitext(file)
    a.append(
        {
            'file_path': file,
            'file_name': file_name.split('\\')[-1],
            'file_ext': file_ext
        }
    )
