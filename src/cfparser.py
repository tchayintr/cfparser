from arguments import parser_arguments
from core import Core
from trainers import parser_trainer
import util



class CFParser(Core):
    def __init__(self):
        super().__init__()


    def get_timer(self):
        timer = util.Time()
        return timer


    def get_args(self):
        parser = parser_arguments.ParserArgumentLoader()
        args = parser.parse_args()
        return args


    def get_trainer(self, args):
        trainer = parser_trainer.ParserTrainer(args)
        return trainer



if __name__ == '__main__':
    cfparser = CFParser()
    timer = cfparser.get_timer()
    timer.start()
    cfparser.run()
    timer.stop()
    print('### Elapsed time: {} seconds'.format(timer.elapsed))
