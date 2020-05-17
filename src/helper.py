'''Helper functions for cfparser-app'''
import nltk
import pickle

import constants



def load_model(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def gen_parser(grammars, parsing_model):
    if parsing_model == constants.APP_DEFAULT_VITERBI_MODEL:
        parser = nltk.parse.ViterbiParser(grammars)

    return parser


def gen_sample_data_tree(data, unused_root, sample_format, brackets_format):
    brackets_format_l = brackets_format[0]
    brackets_format_r = brackets_format[1]
    _ = sample_format.format(brackets_format_l, unused_root, data, brackets_format_r)

    return nltk.Tree.fromstring(_, brackets=brackets_format)


def gen_sample_data_grammars(data, root, grammar_format):
    ''' Generate cfg/pcfg (grammar_format) from nltk.Tree datalist '''
    grammars = []

    for _data in data:
        for production in _data.productions():
            grammars.append(production)

    if grammar_format == constants.APP_DEFAULT_PCFG_FORMAT:
        grammars = nltk.induce_pcfg(root, grammars)

    return grammars


def str2nonterminal(s):
    return nltk.Nonterminal(s)
