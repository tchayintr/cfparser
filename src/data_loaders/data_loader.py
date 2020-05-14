import pickle
import re

import constants



class DataLoader(object):
    def __init__(self):
        self.lowercasing = False
        self.normalize_digits = False


    def gen_grammars(self, data, data_format):
        # to be implemented in sub-class
        pass


    def load_gold_data(self, path, data_format, brackets_format='()'):
        # to be implemented in sub-class
        pass


    def preprocess_token(self, token):
        if self.lowercasing:
            token = str(token).lower()
        if self.normalize_digits:
            token = re.sub(r'[0-9๐-๙]+', constants.NUM_SYMBOL, token)

        return token


    def parse_input(self, line):
        # to be implemented in sub-class
        pass


    def parse_commandline_input(self, line):
        # to be implemented in sub-class
        pass


    def normalize_line(self, line):
        return line.strip()



def load_external_dictionary(path):
    dic = []

    with open(path) as f:
        for line in f:
            dic.append(line)

    return dic


def load_pickle_data(filename_wo_ext):
    dump_path = filename_wo_ext + '.pickle'

    with open(dump_path, mode='rb') as f:
        obj = pickle.load(f)

    return obj


def dump_pickle_data(filename_wo_ext, data):
    dump_path = filename_wo_ext + '.pickle'

    with open(dump_path, mode='wb') as f:
        obj = (data)
        pickle.dump(obj, f)
