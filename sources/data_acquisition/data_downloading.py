import os
import requests
from pathlib import Path
import tqdm
import argparse


# filename = "task1.zip"
# url = "https://zenodo.org/records/7260705/files/Task1.zip?download=1"
# data_dir = "C:\Users\\axell\Documents\dev\sCT_generation\data\\raw_data"
# python .\data_downloading.py -filename "task1.zip" -url "https://zenodo.org/records/7260705/files/Task1.zip?download=1" -data_dir "C:\Users\axell\Documents\dev\sCT_generation\data\raw_data"


def main(filename: str, url: str, data_dir: str):

    DATA_DIR = Path(data_dir)

    # Create data directory
    try:
        DATA_DIR.mkdir()
    except:
        print(f"{DATA_DIR} already exist ...")


    with open(DATA_DIR/filename, "wb") as f:
        with requests.get(url, stream = True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get("content-lenght", 0))

            tqdm_params = {
                    'desc': filename,
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
    parser.add_argument("-filename", metavar="string", required = True, help = "Name of the downloaded dataset")
    parser.add_argument("-url", metavar="string", required = True, help = "Link toward the dataset to download")
    parser.add_argument("-data_dir", metavar="string", required = True, help = "Path of the directory that will contain the dowloaded dataset")

    args = parser.parse_args()

    main(filename = args.filename, url = args.url, data_dir = args.data_dir)

