from pathlib import Path
import argparse
import zipfile

# zipped_file_path = "C:\Users\axell\Documents\dev\sCT_generation\data\raw_dat\Task1.zip"
# unzipped_file_dir = "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data"
# python unzip_file.py -zipped_file_path "C:\:Users\axell\Documents\dev\sCT_generation\data\raw_data\Task1.zip" -unzipped_file_dir "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data"

def main(zipped_file_path: str, unzipped_file_dir: str):

    ZIPPED_FILE_PATH = Path(zipped_file_path)
    UNZIPPED_FILE_DIR = Path(unzipped_file_dir)

    with zipfile.ZipFile(ZIPPED_FILE_PATH, 'r') as zip_ref:
        zip_ref.extractall(UNZIPPED_FILE_DIR)

    return


if __name__ == "__main__" :

    parser = argparse.ArgumentParser(description = "Script to unzip file")

    parser.add_argument("-zipped_file_path", metavar = "string", required = True, help = "path toward the file to unzip")
    parser.add_argument("-unzipped_file_dir",metavar = "string", required = True, help = "directory of the unzip file")

    args = parser.parse_args()
    
    main(zipped_file_path = args.zipped_file_path, unzipped_file_dir = args.unzipped_file_dir)
