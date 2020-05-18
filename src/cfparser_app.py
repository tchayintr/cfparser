import copy
from datetime import datetime
import flask
from flask import Flask
from flask_cors import CORS, cross_origin
import os

import constants
import helper



cfparser = Flask(__name__)
cfparser.config['JSON_AS_ASCII'] = False
CORS(cfparser)



@cfparser.route('/')
def index():
    return flask.render_template('index.html')


@cfparser.errorhandler(404)
def not_found(error):
    return flask.render_template('404.html'), 404


@cfparser.errorhandler(500)
def internal_error(error):
    return 'error500'


@cfparser.route('/api')
def api():
    return flask.render_template('api.html')


@cfparser.route('/models')
def models():
    return flask.render_template('models.html')


@cfparser.route('/publications')
def publications():
    return flask.render_template('publications.html')


@cfparser.route('/tutorials')
def tutorials():
    return flask.render_template('tutorials.html')


@cfparser.route('/api/seg/<input_data>')
@cross_origin()
def seg(input_data):
    assert app

    res = app.core.segmenter(input_data)
    ret = {
        constants.APP_DEFAULT_JSONIFY_KEY_RESULT: res
    }

    return flask.jsonify(ret)


@cfparser.route('/api/segtag/<input_data>')
@cross_origin()
def segtag(input_data):
    assert app
    _ = app.core.segmenter(input_data)

    res = app.core.tagger(_, constants.APP_DEFAULT_BRACKETS_FORMAT)
    ret = {
        constants.APP_DEFAULT_JSONIFY_KEY_RESULT: res
    }

    return flask.jsonify(ret)


@cfparser.route('/api/segtagparse/<input_data>')
@cross_origin()
def segtagparse(input_data):
    assert app
    sample_data = app.gen_sample_data(input_data)

    res = app.parse(input_data, sample_data)
    ret = {
        constants.APP_DEFAULT_JSONIFY_KEY_RESULT: res
    }

    return flask.jsonify(ret)


@cfparser.route('/api/tag/<input_data>')
@cross_origin()
def tag(input_data):
    assert app

    res = app.core.tagger(input_data, constants.APP_DEFAULT_BRACKETS_FORMAT)
    ret = {
        constants.APP_DEFAULT_JSONIFY_KEY_RESULT: res
    }

    return flask.jsonify(ret)


@cfparser.route('/api/tagparse/<input_data>')
@cross_origin()
def tagparse(input_data):
    _ = app.core.tagger(input_data, constants.APP_DEFAULT_BRACKETS_FORMAT)
    sample_data = app.gen_sample_data(_, segment=False)

    res = app.parse(input_data, sample_data, segment=False)
    ret = {
        constants.APP_DEFAULT_JSONIFY_KEY_RESULT: res
    }

    return flask.jsonify(ret)



class App(object):
    def __init__(self):
        '''Refers to CFCore class structures from CFCore.py'''
        self.core = None
        if not os.path.exists(constants.APP_DEFAULT_LOG_DIR):
            os.mkdir(constants.APP_DEFAULT_LOG_DIR)


    def report(self, message):
        if not self.args.quiet:
            print(message, file=self.reporter)


    def load_model(self, path=constants.APP_DEFAULT_MODEL_PATH):
        model_path = path
        core = helper.load_model(model_path)
        self.core = core


    def gen_sample_data(
        self,
        data,
        root=constants.APP_DEFAULT_ROOT_NONTERMINAL,
        unused_nonterminal=constants.APP_DEFAULT_UNUSED_NONTERMINAL,
        sample_format=constants.APP_DEFAULT_SAMPLE_FORMAT,
        brackets_format=constants.APP_DEFAULT_BRACKETS_FORMAT,
        grammar_format=constants.APP_DEFAULT_PCFG_FORMAT,
        segment=True
    ):
        root = helper.str2nonterminal(root)
        sample_tree = self.gen_sample_data_tree(data, unused_nonterminal, sample_format, brackets_format, segment)
        sample_grammars = self.gen_sample_data_grammars(sample_tree, root, grammar_format)
        sample_data = sample_grammars

        return sample_data


    def gen_parser(self, grammars):
        core = self.core
        parsing_model = core.parser_model
        parser = helper.gen_parser(grammars, parsing_model)

        return parser


    def gen_sample_data_tree(self, data, unused_root, sample_format, brackets_format, segment):
        core = self.core
        if segment:
            _segmented_data = core.segmenter(data)
        else:
            _segmented_data = data
        _tagged_data = core.tagger(_segmented_data, brackets_format)
        sample_tree = helper.gen_sample_data_tree(_tagged_data, unused_root, sample_format, brackets_format)

        return sample_tree


    def gen_sample_data_grammars(self, sample, root, grammar_format):
        trees = copy.deepcopy(self.core.trees)
        trees.append(sample)
        sample_grammars = helper.gen_sample_data_grammars(trees, root, grammar_format)

        return sample_grammars


    def parse(
        self,
        data,
        sample_data,
        brackets_format=constants.APP_DEFAULT_BRACKETS_FORMAT,
        segment=True
    ):

        core = self.core
        parser = self.gen_parser(sample_data)
        parsed_tree = None

        if segment:
            _ = core.segmenter(data)
        else:
            _ = data
        _ = _.split()
        for parsed_data in parser.parse(_):
            parsed_tree = '{}{}{}'.format(
                parsed_data.pformat(parens=brackets_format),
                constants.APP_DEFAULT_DELIMITER_PROB,
                parsed_data.prob()
            )

        if parsed_tree:
            parse_time = datetime.now().strftime('%Y%m%d_%H%M')
            reporter = open('{}/{}.log'.format(constants.APP_DEFAULT_LOG_DIR, parse_time), mode='w')
            print('{}{}{}'.format(
                data,
                constants.APP_DEFAULT_DELIMITER_PARSED_TREE,
                parsed_tree,
            ), file=reporter)
            reporter.close()

        return parsed_tree



if __name__ == '__main__':
    app = App()
    app.load_model(constants.APP_DEFAULT_MODEL_PATH)
    # cfparser.run(debug=True, threaded=True)
