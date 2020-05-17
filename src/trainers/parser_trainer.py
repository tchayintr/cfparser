import nltk.parse
import sys

import constants
from data_loaders import parsing_data_loader
from trainers.trainer import Trainer



class ParserTrainerBase(Trainer):
    def __init__(self, args, logger=sys.stderr):
        super().__init__(args, logger)


    def show_data_info(self, data_type):
        if data_type == 'valid':
            data = self.valid
        else:
            data = self.train

        self.log('### {} info'.format(data_type))
        self.log('# length: {}'.format(len(data)))
        self.log()


    def show_training_data(self):
        train = self.train
        valid = self.valid

        train_size = len(train) if train else 0
        valid_size = len(valid) if valid else 0

        self.log('### Loaded data')
        self.log('# train: {} ...'.format(train_size))
        self.log('# valid: {} ...'.format(valid_size))
        self.log()

        self.report('[INFO] data length: train= {} valid={}'.format(train_size, valid_size))



class ParserTrainer(ParserTrainerBase):
    def __init__(self, args, logger=sys.stderr):
        super().__init__(args, logger)


    def init_model(self):
        super().init_model()


    def load_model(self):
        super().load_model()


    def update_model(self, parser=None):
        if self.args.execute_mode == 'eval':
            # TODO
            pass

        elif self.args.execute_mode == 'script':
            self.input_data = self.data_loader.parse_input(self.args.input_data)
            self.update_parser()


    def init_parameters(self):
        self.params = {
            'parsing_model': self.args.parsing_model,
            'segmentation_model': self.args.segmentation_model,
            'tagging_model': self.args.tagging_model,
        }

        self.log('Init parameters')
        self.log('### arguments')
        for k, v in self.args.__dict__.items():
            message = '{}={}'.format(k, v)
            self.log('# {}'.format(message))
            self.report('[INFO] arg: {}'.format(message))
        self.log('')


    def init_root(self):
        self.root = nltk.Nonterminal(constants.ROOT_NONTERMINAL)


    def update_parameters(self, key, value):
        self.params[key] = value


    def update_parser(self):
        self.init_root()
        self.update_grammars()

        if self.core.parser_model == 'viterbi':
            self.parser = nltk.parse.ViterbiParser(self.train)


    def update_grammars(self):
        input_data = self.input_data
        if self.args.task == constants.TASK_TAGPARSE or self.args.task == constants.TASK_TAG:
            segmented_data = input_data
        else:
            segmented_data = self.core.segmenter(input_data)
        tagged_data = self.core.tagger(segmented_data)

        sample_data = self.gen_sample_data(
            tagged_data,
            constants.UNUSED_NONTERMINAL,
        )

        sample_tree = self.data_loader.convert_to_tree(
            sample_data,
            self.args.brackets_format
        )

        self.core.trees.append(sample_tree)
        self.train = self.gen_grammars(self.core.trees, constants.PCFG_FORMAT)


    def setup_data_loader(self):
        self.data_loader = parsing_data_loader.ParsingDataLoader(
            lowercasing=self.args.lowercasing,
            normalize_digits=self.args.normalize_digits,
        )


    def gen_grammars(self, data, data_format):
        ''' Generate cfg/pcfg (data_format) from nltk.Tree datalist '''
        grammars = []

        for _data in data:
            for production in _data.productions():
                grammars.append(production)

        if data_format == constants.PCFG_FORMAT:
            grammars = nltk.induce_pcfg(self.root, grammars)

        return grammars


    def gen_sample_data(self, data, root):
        brackets_format_l = self.args.brackets_format[0]
        brackets_format_r = self.args.brackets_format[1]
        return constants.SAMPLE_FORMAT.format(brackets_format_l, root, data, brackets_format_r)


    def gen_sample_grammars(self, productions):
        samples = []
        for production in productions:
            lhs = production.lhs()
            rhs = production.rhs()
            samples.append(nltk.grammar.Production(lhs, rhs))
        return samples


    def setup_parser(self):
        self.init_root()
        self.trees = self.train
        if self.args.input_data_format == 'tree':
            self.train = self.gen_grammars(self.train, constants.PCFG_FORMAT)

        if self.args.parsing_model == 'viterbi':
            parser = nltk.parse.ViterbiParser(self.train)

        self.parser = parser


    def run_script_mode(self):
        input_data = self.input_data
        segmenter = self.segmenter
        tagger = self.tagger
        parser = self.parser

        if self.args.task == constants.TASK_SEG:
            segmented_data = segmenter(input_data)
            res = segmented_data

        elif self.args.task == constants.TASK_SEGTAG:
            segmented_data = segmenter(input_data)
            tagged_data = tagger(segmented_data)
            res = tagged_data

        elif self.args.task == constants.TASK_SEGTAGPARSE:
            segmented_data = segmenter(input_data)
            sample_data = segmented_data.split()
            for parsed_data in parser.parse(sample_data):
                parsed_tree = '{}▁{}'.format(
                    parsed_data.pformat(parens=self.args.brackets_format),
                    parsed_data.prob()
                )
            res = parsed_tree

        elif self.args.task == constants.TASK_TAG:
            tagged_data = tagger(input_data)
            res = tagged_data

        elif self.args.task == constants.TASK_TAGPARSE:
            sample_data = input_data.split()
            for parsed_data in parser.parse(sample_data):
                parsed_tree = '{}{}{}'.format(
                    parsed_data.pformat(parens=self.args.brackets_format),
                    constants.DELIMITER_PROB,
                    parsed_data.prob()
                )
            res = parsed_tree

        elif self.args.task == constants.TASK_PARSE:
            # Do not support
            pass

        self.log('{}{}{}'.format(input_data, constants.DELIMITER_PARSED_TREE, res))
        self.report('{}{}{}'.format(input_data, constants.DELIMITER_PARSED_TREE, res))

        return res


    def run_interactive_mode(self):
        pass
