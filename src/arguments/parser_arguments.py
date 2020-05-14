from pathlib import Path

from arguments.arguments import ArgumentLoader



class ParserArgumentLoader(ArgumentLoader):
    def parse_args(self):
        return super().parse_args()


    def get_full_parser(self):
        parser = super().get_full_parser()

        ### data paths and related options
        parser.add_argument('--external_dic_path', default=None, help='File path of external word dictionary listing known words')

        ### options for word segmentation model and parameters
        parser.add_argument('--segmentation_model', choices=['wordcut'], default='wordcut', help='Word segmentation model (Default: wordcut)')

        ### options for POS tagger model and parameters
        parser.add_argument('--tagging_model', choices=['artagger'], default='artagger', help='Part-of-speech tagging model (Default: artagger)')

        ### options for parser model and parameters
        parser.add_argument('--parsing_model', choices=['viterbi'], default='viterbi', help='Parsing model (Default: viterbi)')

        return parser


    def get_minimum_parser(self, args):
        parser = super().get_minimum_parser(args)

        # specific options for segmentation/tagging
        parser.add_argument('--external_dic_path', type=Path, default=args.external_dic_path)

        # segmentation model option
        self.add_segmentation_model_options(parser, args)

        # tagger model options
        self.add_tagging_model_options(parser, args)

        # parsing model options
        self.add_parsing_model_options(parser, args)

        return parser


    def add_segmentation_model_options(self, parser, args):
        parser.add_argument('--segmentation_model', type=str.lower, default=args.segmentation_model)


    def add_tagging_model_options(self, parser, args):
        parser.add_argument('--tagging_model', type=str.lower, default=args.tagging_model)


    def add_parsing_model_options(self, parser, args):
        parser.add_argument('--parsing_model', type=str.lower, default=args.parsing_model)
