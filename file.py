import os
import argparse
from PIL import Image
import math
import operator
from functools import reduce


def get_file_histograms(directory):
    hl = []
    for filename in os.listdir(directory):
        h = Image.open(directory + filename).histogram()
        hl.append({'file_name': filename, 'histogram': h})
    return hl


def rms(h1, h2):
    """root mean square function"""
    return math.sqrt(reduce(operator.add, map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))


def find_duplicates(histogram_list):
    res_list = []
    for i in histogram_list:
        for j in histogram_list:
            if i != j and {i['file_name'], j['file_name']} not in res_list:
                if rms(i['histogram'], j['histogram']) == 0.0:
                    res_list.append({i['file_name'], j['file_name']})
    return res_list


def print_duplicates(duplicates_list):
    for i in duplicates_list:
        print([j for j in i])


def main_func(directory):
    if os.path.isdir(directory):
        histogram_list = get_file_histograms(directory)
        duplicates_list = find_duplicates(histogram_list)
        print_duplicates(duplicates_list)
    else:
        raise NotADirectoryError(directory)


parser = argparse.ArgumentParser()
parser.add_argument('--path', nargs=1, type=main_func, help='folder with images')
args = parser.parse_args()
