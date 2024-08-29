from pathlib import Path
import argparse
import zipfile

# file_path = "C:\Users\axell\Documents\dev\sCT_generation\data\raw_dat\Task1.zip"
# output_dir = "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data"
# python unzip_file.py -file_path "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data\Task1.zip" -output_dir "C:\Users\axell\Documents\dev\sCT_generation\dat"

def main(file_path: str, output_dir: str):

    FILE_PATH = Path(file_path)
    OUTPUT_DIR = Path(output_dir)

    with zipfile.ZipFile(FILE_PATH, 'r') as zip_ref:
        zip_ref.extractall(OUTPUT_DIR)

    return


if __name__ == "__main__" :

    parser = argparse.ArgumentParser(description = "Script to unzip file")

    parser.add_argument("-file_path", metavar = "string", required = True, help = "path toward the file to unzip")
    parser.add_argument("-output_dir",metavar = "string", required = True, help = "directory of the unzip file")

    args = parser.parse_args()
    
    main(file_path = args.file_path, output_dir = args.output_dir)
