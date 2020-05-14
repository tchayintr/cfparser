import sys

from data_loaders import segmentation_data_loader
from trainers.trainer import Trainer



class SegmenterTrainer(Trainer):
    def __init__(self, args, logger=sys.stderr):
        self.args = args
        self.logger = logger


    def load_external_dictionary(self):
        if self.args.external_dic_path:
            edic_path = self.args.external_dic_path
            self.dic = segmentation_data_loader.load_external_dictionary(edic_path)
            self.log('Load external dictionary: {}'.format(edic_path))
            self.log('')
