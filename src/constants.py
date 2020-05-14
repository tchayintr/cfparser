global __version
__version__ = 'v0.2.0b'

# common

GPU_DEVICE = 'GPU'
CUDA_DEVICE = 'CUDA_VISIBLE_DEVICES'

# task

TASK_SEG = 'seg'
TASK_TAG = 'tag'
TASK_PARSE = 'parse'
TASK_SEGTAG = 'segtag'
TASK_TAGPARSE = 'tagparse'
TASK_SEGTAGPARSE = 'segtagparse'

# for analyzer

LOG_DIR = 'log'
MODEL_DIR = 'models/main'
PARAM_DIR = 'models/parameter'

# model

### segmenters

DEFAULT_DICT_PATH = 'data/dict/bigthai.dict'

### taggers


### parsers

ROOT_NONTERMINAL = 'S'
UNUSED_NONTERMINAL = 'UNUSED'

# for character

NUM_SYMBOL = '<num>'
NEWLINE_SYMBOL = '\n'

# for data i/o

TREE_FORMAT = 'tree'
CFG_FORMAT = 'cfg'
PCFG_FORMAT = 'pcfg'

JSON_FORMAT = 'json'
TXT_FORMAT = 'txt'
ATTR_INFO_DELIM = ','
PREFIX_FIELD_NAME = '_'
FIRST_ELEM = 0
LAST_ELEM = -1

CFG_FILE_FORMAT = '.cfg'
PCFG_FILE_FORMAT = '.pcfg'
TXT_FORMAT_EXTENSION = '.txt'
JSON_FORMAT_EXTENSION = '.json'

JSON_SOURCE_KEY = 'source'
JSON_TARGET_KEY = 'target'
