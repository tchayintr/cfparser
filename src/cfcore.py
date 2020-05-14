class CFCore(object):
    def __init__(
        self,
        segmenter=None,
        tagger=None,
        parser=None,
        segmenter_model=None,
        tagger_model=None,
        parser_model=None,
        trees=None
    ):
        self.segmenter = segmenter
        self.tagger = tagger
        self.parser = parser
        self.segmenter_model = segmenter_model
        self.tagger_model = tagger_model
        self.parser_model = parser_model
        self.trees = trees
