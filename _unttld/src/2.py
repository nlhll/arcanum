def validate_file_extension(files):
    for f in files:
        if str(f).split('.')[-1] not in VALID_DATASET_TYPES:
            return False
    return True