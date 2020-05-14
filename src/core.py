import os

import constants



class Core(object):
    def get_args(self):
        # to be implemented in sub-class
        return None


    def get_trainer(self, args):
        # to be implemented in sub-class
        return None


    def run(self):
        ################################
        # Make necessary directories

        if not os.path.exists(constants.LOG_DIR):
            os.mkdir(constants.LOG_DIR)
        if not os.path.exists(constants.PARAM_DIR):
            os.mkdir(constants.PARAM_DIR)
        if not os.path.exists(constants.MODEL_DIR):
            os.mkdir(constants.MODEL_DIR)

        ################################
        # Get arguments and initialize trainer

        args = self.get_args()
        trainer = self.get_trainer(args)

        ################################
        # Prepare gpu

        use_gpu = 'gpu' in args and args.gpu >= 0
        if use_gpu:
            os.environ[constants.CUDA_DEVICE] = str(args.gpu)

        ################################
        # Load model if any otherwise init parameters

        if args.model_path:
            trainer.load_model()
        else:
            trainer.init_parameters()

        ################################
        # Load dataset

        if args.execute_mode == 'train':
            trainer.load_training_and_validation_data()
        elif args.execute_mode == 'eval':
            trainer.load_training_and_validation_data()
        elif args.execute_mode == 'script':
            trainer.setup_data_loader()
        elif args.execute_mode == 'interactive':
            trainer.setup_data_loader()

        ################################
        # Set up model

        if not trainer.core:
            trainer.init_model()
        else:
            trainer.update_model()

        ################################
        # Run

        if args.execute_mode == 'train':
            trainer.run_train_mode()
        elif args.execute_mode == 'eval':
            trainer.run_eval_mode()
        elif args.execute_mode == 'script':
            trainer.run_script_mode()
        elif args.execute_mode == 'interactive':
            trainer.run_interactive_mode()

        ################################
        # Terminate

        trainer.close()
