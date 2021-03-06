"""
This module downloads chirps raster files for a
seleced range of years

Author  : Celray James CHAWANDA
Email   : celray.chawanda@outlook.com
Licence : MIT 2020 (c) Open Water Network
"""
# imports
from datetime import datetime, timedelta
import os
import wget
from multiprocessing import Pool


# functions


def file_name(path_, extension=True):
    if extension:
        fn = os.path.basename(path_)
    else:
        fn = os.path.basename(path_).split(".")[0]
    return(fn)


def download_file(url, save_path):
    fname = file_name(url)
    save_dir = os.path.dirname(save_path)
    save_fname = "{0}/{1}".format(save_dir, fname)

    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    wget.download(url, save_fname)


# provide the number of years here
years = range(1984, 2020)
workers = 32

if __name__ == '__main__':
    one_day = timedelta(days=1)
    current_date = datetime(1984, 1, 1)

    url_string = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/{year}/chirps-v2.0.{year}.{mm}.{dd}.tif.gz"
    urls = []
    save_dir = ["downloaded/"]

    while current_date.year in years:
        url = url_string.format(
            year=current_date.year,
            mm="0{0}".format(
                current_date.month) if current_date.month < 10 else current_date.month,
            dd="0{0}".format(current_date.day) if current_date.day < 10 else current_date.day)
        urls.append((url, save_dir[0]))
        current_date += one_day
        print(current_date)

    pool = Pool(workers)
    pool.starmap(download_file, urls)
    pool.terminate()
