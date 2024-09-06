import os
import requests
from pathlib import Path
import tqdm
import argparse


# data_file_name = "task1.zip"
# url = "https://zenodo.org/records/7260705/files/Task1.zip?download=1"
# data_output_dir = "C:\Users\\axell\Documents\dev\sCT_generation\data\\raw_data"
# python .\data_downloading.py -url "https://zenodo.org/records/7260705/files/Task1.zip?download=1" -data_file_name "task1.zip" -data_output_dir "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data"


def main(url: str,
         data_file_name: str,
         data_output_dir: str):

    DATA_OUTPUT_DIR = Path(data_output_dir)

    # Create data directory
    try:
        DATA_OUTPUT_DIR.mkdir()
    except:
        print(f"{DATA_OUTPUT_DIR} already exist ...")


    with open(DATA_OUTPUT_DIR/data_file_name, "wb") as f:
        with requests.get(url, stream = True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get("content-lenght", 0))

            tqdm_params = {
                    'desc': data_file_name,
                    'total': total_size,
                    'miniters': 1,
                    'unit': 'B',
                    'unit_scale': True,
                    'unit_divisor': 1024,
                    } 
            with tqdm.tqdm(**tqdm_params) as pb:
                for chunk in r.iter_content(chunk_size=8192):
                    pb.update(len(chunk))
                    f.write(chunk)
    return


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "script for downloding your dataset")
    parser.add_argument("-data_file_name", metavar="string", required = True, help = "Name of the downloaded dataset")
    parser.add_argument("-url", metavar="string", required = True, help = "Link toward the dataset to download")
    parser.add_argument("-data_output_dir", metavar="string", required = True, help = "Path of the directory that will contain the dowloaded dataset")

    args = parser.parse_args()

    main(url = args.url, data_file_name = args.data_file_name, data_output_dir = args.data_output_dir)

