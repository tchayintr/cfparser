import os

import constants
from wordcut import Wordcut as wordcut      # 97ddca7

'''
    input: raw text
    output: segmented text with whitespaces ('segment' function)
'''



class Wordcut(wordcut):
    @classmethod
    def _model(cls, dictfile):
        '''Initialize tokenizer model from dictionary'''
        with open(dictfile) as dictionary:
            words = list(set([word.rstrip() for word in dictionary.readlines()]))
            words.sort()
            return cls(words)


    def segment(self, inp):
        '''Tokenize an input using defined arbitary model'''
        tokens = self.tokenize(inp)
        tokens = clean(tokens)
        return ' '.join(tokens)


    @classmethod
    def get_default_model(cls):
        '''Get default tokeniser model (bigthai)'''
        return wordcut.bigthai()


    @classmethod
    def default_segment(cls, inp):
        '''Segment an input with default model (bigthai)'''
        tokens = wordcut.bigthai().tokenize(inp)
        tokens = clean(tokens)
        return ' '.join(tokens)



def trim(tokens):
    '''Trim spaces in the list'''
    return [token.strip() for token in tokens]


def remove_empty(tokens):
    '''Remove an empty string in the list'''
    return list(filter(None, [token.strip() for token in tokens]))


def clean(tokens):
    '''Trim spaces and remove an empty element (empty string) in the list'''
    return remove_empty(trim(tokens))



if __name__ == '__main__':
    text = "ทดลองการตัดคำ"
    filedir = os.path.dirname(__file__)
    dictfile = os.path.join(filedir, constants.DEFAULT_DICT_PATH)

    model = Wordcut._model(dictfile)
    print(model.segment(text))

    default_model = Wordcut.get_default_model()
    print(default_model.tokenize(text))

    print(Wordcut.default_segment(text))
