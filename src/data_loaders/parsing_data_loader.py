import nltk
import sys

import constants
from data_loaders.data_loader import DataLoader



class ParsingDataLoader(DataLoader):
    def __init__(
        self,
        lowercasing=False,
        normalize_digits=False,

    ):
        self.lowercasing = lowercasing
        self.normalize_digits = normalize_digits


    def load_gold_data(self, path, data_format, brackets_format='()'):
        if data_format == constants.TREE_FORMAT:
            data = self.load_gold_data_TREE(path, brackets_format)

        elif data_format == constants.CFG_FORMAT:
            if not is_compatible_file(path, constants.CFG_FILE_FORMAT):
                print('Error: invalid CFG extension format (*.cfg): {}'.format(path), file=sys.stderr)
                sys.exit()
            data = self.load_gold_data_CFG

        elif data_format == constants.PCFG_FORMAT:
            if not is_compatible_file(path, constants.PCFG_FILE_FORMAT):
                print('Error: invalid PCFG extension format (*.pcfg): {}'.format(path), file=sys.stderr)
                sys.exit()
            data = self.load_gold_data_PCFG

        return data


    def load_gold_data_TREE(self, path, brackets_format):
        ''' Load labelled brackets (String) into nltk.tree.Tree '''
        trees = []

        with open(path) as f:
            for lnum, line in enumerate(f):
                line = self.normalize_line(line)
                tree = ParsingDataLoader.convert_to_tree(line, brackets_format)
                trees.append(tree)

        return trees


    def load_gold_data_CFG(self, path):
        return nltk.data.load(path, format=constants.CFG_FORMAT)


    def load_gold_data_PCFG(self, path):
        return nltk.data.load(path, format=constants.PCFG_FORMAT)


    def parse_input(self, line):
        return line


    def parse_commandline_input(self, line):
        pass


    @classmethod
    def convert_to_tree(cls, data, brackets_format):
        ''' Parse a string into NLTK Tree '''
        assert isinstance(data, str)
        return nltk.Tree.fromstring(data, brackets=brackets_format)


    @classmethod
    def convert_to_cfg(cls, data):
        ''' Parse a string into NLTK CFG '''
        assert isinstance(data, str)
        return nltk.CFG.fromstring(data)


    @classmethod
    def convert_to_pcfg(cls, data):
        ''' Parse a string into NLTK PCFG '''
        assert isinstance(data, str)
        return nltk.PCFG.fromstring(data)



def is_compatible_file(path, compatible_format):
    return path.suffix == compatible_format
