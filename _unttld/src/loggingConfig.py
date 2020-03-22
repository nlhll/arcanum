import logging.config
import json
from pathlib import Path


class LoggingConfig:
    """Custom logging config class"""
    LOG_CONFIG_PATH = 'logConfig.json'
    # VALID_HANDLER_CLASS = ['StreamHandler', 'FileHandler']

    def __init__(self, logger_name, handler_name='handler',
                 handler_class=None, level='INFO'):

        """Constructor.

        Config Log config
        """
        # set a logger name
        self.logger_name = logger_name
        # set a handler name
        self.handler_name = handler_name
        # set a handler's class
        # self.set_handler_class(handler_class)
        # set level
        self.level = level

        self.set_dictConfig()

    def set_handler_class(self, handler_class):
        """Set a handler's class with validation"""
        self.validate_handler_class(handler_class)
        self.handler_class = handler_class

    def validate_handler_class(self, handler_class):
        """Validator.

        Validate if the handler's class is valid
        (either 'StreamHandler'or 'FileHandler')
        """
        if handler_class not in self.VALID_HANDLER_CLASS:
            raise ValueError('Incorrect handler class name has been entered.')

    def set_dictConfig(self):
        # set the updated log config file
        path = Path(self.LOG_CONFIG_PATH)
        if path.is_file():
            with open(path, 'r') as f:
                dict_log_config = json.load(f)
        else:
            raise FileExistsError('The log config file doesn\'t exist')
        logger_value = \
            {
                "handlers": [self.handler_name],
                "level": self.level
            }
        dict_log_config["loggers"][self.logger_name] = logger_value
        # set config
        logging.config.dictConfig(dict_log_config)

        if path.is_file():
            with open(path, 'w') as f:
                json.dump(dict_log_config, f)
        else:
            raise FileExistsError('The log config file doesn\'t exist')
