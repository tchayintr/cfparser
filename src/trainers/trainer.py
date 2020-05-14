from datetime import datetime
import pickle
import sys

from cfcore import CFCore
import constants
import models.segmenters._wordcut
import models.taggers._artagger



class Trainer(object):
    def __init__(self, args, logger=sys.stderr):
        err_msgs = []
        if args.execute_mode == 'train':
            if not args.train_data:
                msg = 'Error: the following argument is required for {} mode: {}'.format(args.execute_mode, '--train_data')
                err_msgs.append(msg)

        elif args.execute_mode == 'eval':
            if not args.model_path:
                msg = 'Error: the following argument is required for {} mode: {}'.format(args.execute_mode, '--model_path/-m')
                err_msgs.append(msg)

            if not args.valid_data:
                msg = 'Error: the following argument is required for {} mode: {}'.format(args.execute_mode, '--valid_data')
                err_msgs.append(msg)

        elif args.execute_mode == 'script':
            if not args.model_path:
                msg = 'Error: the following argument is required for {} mode: {}'.format(args.execute_mode, '--model_path/-m')
                err_msgs.append(msg)

        elif args.execute_mode == 'interactive':
            if not args.model_path:
                msg = 'Error: the following argument is required for {} mode: {}'.format(args.execute_mode, '--model_path/-m')
                err_msgs.append(msg)

        else:
            msg = 'Error: invalid execute mode: {}'.format(args.execute_mode)
            err_msgs.append(msg)

        if err_msgs:
            for msg in err_msgs:
                print(msg, file=sys.stderr)
            sys.exit()

        self.args = args
        self.start_time = datetime.now().strftime('%Y%m%d_%H%M')
        self.logger = logger    # outout execute log to console
        self.reporter = None    # output execute log to file
        self.train = None
        self.valid = None
        self.trees = None
        self.input_data = None
        self.params = None
        self.dic = None
        self.data_loader = None
        self.core = None        # core model bundler (segmenter, tagger, parser)
        self.segmenter = None
        self.tagger = None
        self.parser = None
        self.evaluator = None
        self.root = None

        self.log('Start time: {}'.format(self.start_time))
        if not self.args.quiet:
            self.reporter = open('{}/{}.log'.format(constants.LOG_DIR, self.start_time), mode='a')


    def report(self, message):
        if not self.args.quiet:
            print(message, file=self.reporter)


    def log(self, message=''):
        print(message, file=self.logger)


    def close(self):
        if not self.args.quiet:
            self.reporter.close()


    def load_external_dictionary(self):
        # to be implemented in sub-class
        pass


    def init_model(self):
        self.log('Initialize model from parameters')
        self.setup_core()


    def reinit_model(self):
        self.log('Re-initialize model components')
        self.setup_core(train=False)


    def load_model(self):
        model_path = self.args.model_path
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        self.log('# Load model: {}\n'.format(model_path))

        self.segmenter = model.segmenter
        self.tagger = model.tagger
        self.parser = model.parser
        self.trees = model.trees
        self.reinit_model()


    def show_parameters(self):
        self.log('### arguments')
        for k, v in self.args.__dict__.items():
            if k in self.params and v == self.params[k]:
                message = '{}={}'.format(k, self.params[k])

            elif k in self.params:
                if v != self.hparams[k] and (str(v) == str(self.hparams[k])):
                    message = '{}={}'.format(k, self.hparams[k])
                elif v != self.params[k]:
                    message = '{}={} (input option value {} was discarded)'.format(k, v, self.hparams[k])
                    self.params[k] = v

            else:
                message = '{}={}'.format(k, v)

            self.log('# {}'.format(message))
            self.report('[INFO] arg: {}'.format(message))


    def update_model(self, parser=None):
        # to be implemented in sub-class
        pass


    def init_parameters(self):
        # to be implemented in sub-class
        self.params = {}


    def update_parameters(self, key, value):
        # to be implemented in sub-class
        pass


    def load_parameters(self, params_path):
        # to be implemented in sub-class
        pass


    def load_training_and_validation_data(self):
        self.load_data('train')
        if self.args.valid_data:
            self.load_data_('valid')
        self.show_training_data()


    def load_data(self, data_type):
        if data_type == 'train':
            self.setup_data_loader()
            data_path = self.args.train_data
            data = self.data_loader.load_gold_data(
                data_path,
                self.args.input_data_format,
                self.args.brackets_format,
            )
            self.train = data

        elif data_type == 'valid':
            data_path = self.args.valid_data
            data = self.data_loader.load_gold_data(
                data_path,
                self.args.input_data_format,
                self.args.brackets_format,
            )
            self.valid = data

        else:
            print('Error: incorrect data type: {}'.format(data_type), file=sys.stderr)
            sys.exit()

        self.log('Load {} data: {}'.format(data_type, data_path))
        self.show_data_info(data_type)


    def show_data_info(self):
        # to be implemented in sub-class
        pass


    def show_model_info(self):
        self.log('### CFCore model: {}'.format(self.core))
        self.log('# segmenter: {}'.format(self.segmenter))
        self.log('# tagger: {}'.format(self.tagger))
        self.log('# parser: {}'.format(self.parser))
        self.log('# trees: {}'.format(len(self.trees)))
        self.log('')


    def show_training_data(self):
        # to be implemented in sub-class
        pass


    def setup_data_loader(self):
        # to be implemented in sub-class
        pass


    def setup_segmenter(self):
        if self.args.segmentation_model == 'deepcut':
            segmenter = None

        elif self.args.segmentation_model == 'wordcut':
            if self.args.external_dic_path:
                edic_path = self.args.external_dic_path
            else:
                edic_path = constants.DEFAULT_DICT_PATH
            segmenter = models.segmenters._wordcut.Wordcut._model(edic_path).segment

        self.segmenter = segmenter


    def setup_tagger(self):
        if self.args.tagging_model == 'artagger':
            tagger = models.taggers._artagger.ARTagger.tag

        self.tagger = tagger


    def setup_parser(self):
        # to be implemented in sub-class
        pass


    def setup_core(self, train=True):
        if train:
            self.setup_segmenter()
            self.setup_tagger()
            self.setup_parser()

        self.core = CFCore(
            segmenter=self.segmenter,
            tagger=self.tagger,
            parser=self.parser,
            segmenter_model=self.args.segmentation_model,
            tagger_model=self.args.tagging_model,
            parser_model=self.args.parsing_model,
            trees=self.trees,
        )
        self.show_model_info()


    def run_train_mode(self):
        if not self.args.quiet:
            param_path = '{}/{}.hyp'.format(constants.PARAM_DIR, self.start_time)
            with open(param_path, 'w') as f:
                for key, val in self.params.items():
                    print('{}={}'.format(key, val), file=f)
                self.log('Save parameters: {}'.format(param_path))

            model_path = '{}/{}.model'.format(constants.MODEL_DIR, self.start_time)
            with open(model_path, 'wb') as f:
                pickle.dump(self.core, f)
            self.log('save the model: {}'.format(model_path))
            self.report('[INFO] save the model: {}'.format(model_path))

        time = datetime.now().strftime('%Y%m%d_%H%M')
        self.report('[INFO] complete: {}\n'.format(time))
        self.log('Finish: {}\n'.format(time))


    def run_eval_mode(self):
        # TODO
        pass


    def run_script_mode(self):
        # to be implemented in sub-class
        pass


    def run_interactive_mode(self):
        # to be implemented in sub-class
        pass
