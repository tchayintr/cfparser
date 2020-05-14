import argparse
from pathlib import Path
import sys



class ArgumentLoader(object):
    def __init__(self):
        # self.parser = argparse.ArgumentParser()
        pass


    def parse_args(self):
        all_args = self.get_full_parser().parse_args()
        min_args = self.get_minimum_parser(all_args).parse_args()
        return min_args


    def get_full_parser(self):
        parser = argparse.ArgumentParser()

        # mode options
        parser.add_argument('--execute_mode', '-x', choices=['train', 'eval', 'script', 'interactive'], help='Choose a mode from among \'train\', \'eval\', \'script\', and \'interactive\'')
        parser.add_argument('--task', '-t', help='Choose a task')
        parser.add_argument('--quiet', '-q', action='store_true', help='Do not output log file and serialized model file')

        # gpu options
        parser.add_argument('--gpu', '-g', type=int, default=-1, help='[UNSUPPORTED] GPU device ID (Use CPU if specify a negative value) (Default: -1)')

        # data paths and related options
        parser.add_argument('--model_path', '-m', default=None, help='File path to of trained model')
        parser.add_argument('--train_data', default=None, help='File path of training data')
        parser.add_argument('--valid_data', default=None, help='File path of validation data')
        parser.add_argument('--input_data', '-i', default=None, help='Input unparsed text')
        parser.add_argument('--output_data', '-o', default=None, help='File path to output parsed text')
        parser.add_argument('--input_data_format', choices=['tree', 'cfg', 'pcfg'], default='tree', help='Choose format of input (training and validation) data from among \'tree\', \'cfg\' and \'pcfg\' (Default: tree)')
        parser.add_argument('--output_data_format', default='txt', help='Choose format of output data from among \'txt\' and \'json\'')
        parser.add_argument('--brackets_format', choices=['()', '[]'], default='()', help='Specify brackets format for training/validation data from among \'()\' and \'[]\'(Default: ())')

        # options for data pre/post-processing
        parser.add_argument('--lowercase_alphabets', dest='lowercasing', action='store_true', help='Lowercase alphabets in input text')
        parser.add_argument('--normalize_digits', action='store_true', help='Normalize digits by the same symbol in input text')

        return parser


    def get_minimum_parser(self, args):
        parser = argparse.ArgumentParser()

        # basic options
        self.add_basic_options(parser, args)

        # dependent execute mode options
        if args.execute_mode == 'train':
            self.add_train_mode_options(parser, args)
        elif args.execute_mode == 'eval':
            self.add_eval_mode_options(parser, args)
        elif args.execute_mode == 'script':
            self.add_script_mode_options(parser, args)
        elif args.execute_mode == 'interactive':
            self.add_interactive_mode_options(parser, args)
        else:
            print('Error: invalid execute mode: {}'.format(args.execute_mode), file=sys.stderr)
            sys.exit()

        return parser


    def add_basic_options(self, parser, args):
        # mode options
        parser.add_argument('--execute_mode', '-x', type=str.lower, required=True, default=args.execute_mode)
        if args.execute_mode == 'script' or args.execute_mode == 'interactive':
            parser.add_argument('--task', type=str.lower, required=True, default=args.task)
        parser.add_argument('--quiet', '-q', action='store_true', default=args.quiet)

        # options for data pre/post-processing
        parser.add_argument('--lowercase_alphabets', dest='lowercasing', action='store_true', default=args.lowercasing)
        parser.add_argument('--normalize_digits', action='store_true', default=args.normalize_digits)

        # gpu options
        parser.add_argument('--gpu', '-g', type=int, default=args.gpu)


    def add_train_mode_options(self, parser, args):
        # data path and related options
        parser.add_argument('--model_path', type=Path, default=args.model_path)
        parser.add_argument('--train_data', required=True, type=Path, default=args.train_data)
        parser.add_argument('--valid_data', type=Path, default=args.valid_data)

        self.add_input_data_format_option(parser, args)
        self.add_brackets_format_option(parser, args)


    def add_eval_mode_options(self, parser, args):
        # data path and related options
        parser.add_argument('--model_path', required=True, type=Path, default=args.model_path)
        parser.add_argument('--train_data', type=Path, default=args.train_data)
        parser.add_argument('--valid_data', required=True, type=Path, default=args.valid_data)

        self.add_input_data_format_option(parser, args)
        self.add_brackets_format_option(parser, args)


    def add_script_mode_options(self, parser, args):
        # data path and related options
        parser.add_argument('--model_path', required=True, type=Path, default=args.model_path)
        parser.add_argument('--input_data', required=True, type=str, default=args.input_data)

        self.add_output_data_options(parser, args)
        self.add_brackets_format_option(parser, args)


    def add_interactive_mode_options(self, parser, args):
        # data path and related options
        parser.add_argument('--model_path', required=True, type=Path, default=args.model_path)

        self.add_output_data_options(parser, args)
        self.add_brackets_format_option(parser, args)


    def add_output_data_options(self, parser, args):
        parser.add_argument('--output_data', '-o', type=Path, default=args.output_data)

        self.add_output_data_format_option(parser, args)


    def add_input_data_format_option(self, parser, args):
        parser.add_argument('--input_data_format', type=str.lower, default=args.input_data_format)


    def add_output_data_format_option(self, parser, args):
        parser.add_argument('--output_data_format', type=str.lower, default=args.output_data_format)


    def add_brackets_format_option(self, parser, args):
        parser.add_argument('--brackets_format', type=str, default=args.brackets_format)



if __name__ == '__main__':
    ArgumentLoader().get_full_parser()
