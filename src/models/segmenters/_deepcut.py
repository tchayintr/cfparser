import os
import logging
import deepcut

import constants
import util

'''
    input: raw text
    output: segmented text with whitespaces
'''



class Deepcut(deepcut.DeepcutTokenizer):
    def __init__(self):
        '''suppress messages from tensorflow'''
        set_tf_loglevel(logging.FATAL)


    def segment(self, inp, custom_words=None):
        tokens = self.tokenize(inp, custom_dict=custom_words)
        tokens = util.clean(tokens)
        return ' '.join(tokens)


    @classmethod
    def default_segment(cls, inp):
        tokens = deepcut.tokenize(inp)
        tokens = util.clean(tokens)
        return ' '.join(tokens)


    @classmethod
    def get_default_model(cls):
        return deepcut



def set_tf_loglevel(level):
    '''Set loging level for TensorFlow'''
    if level >= logging.FATAL:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    if level >= logging.ERROR:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    if level >= logging.WARNING:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
    else:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
    logging.getLogger('tensorflow').setLevel(level)




if __name__ == '__main__':
    text = "ทดลองการตัดคำ"
    # set_tf_loglevel(logging.FATAL)

    default_model = Deepcut.get_default_model()
    print(default_model.tokenize(text))
    print(Deepcut.default_segment(text))
    print(Deepcut.segment(text, constants.DEFAULT_DICT_PATH))
