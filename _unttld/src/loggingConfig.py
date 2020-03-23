import logging.config
import logging
import json
from pathlib import Path


class LoggingConfig:
    """Custom logging config class"""
    LOG_CONFIG_PATH = 'logConfig.json'
    VALID_HANDLER_CLASS = ['StreamHandler', 'FileHandler']

    def __init__(self, logger_name, handler_class='StreamHandler',
                 level='INFO'):
        """Constructor.

        Config Log config
        """
        # set a handler's config
        self.set_handler(handler_class, logger_name)
        # set a logger's config
        self.set_logger(logger_name, level)

        self.set_dictconfig()

    def set_dictconfig(self):
        """Set the updated log config file"""
        path = Path(self.LOG_CONFIG_PATH)
        if path.is_file():
            with open(path, 'r') as f:
                dict_log_config = json.load(f)
        else:
            raise FileExistsError('The log config file doesn\'t exist')

        # add the handler and the logger
        dict_log_config["handlers"].update(self.handler["value"])
        dict_log_config["loggers"].update(self.logger["value"])
        # set config
        logging.config.dictConfig(dict_log_config)

        if path.is_file():
            with open(path, 'w') as f:
                json.dump(dict_log_config, f)
        else:
            raise FileExistsError('The log config file doesn\'t exist')

    def set_handler(self, handler_class, handler_prefix):
        """Set a handler's config (name, class, etc) with class validation"""
        self.validate_handler_class(handler_class)

        handler_name = handler_prefix + handler_class
        self.handler = {"key": handler_name, "value": {handler_name: {}}}
        self.handler["value"][handler_name]["class"] = \
            'logging.' + handler_class
        self.handler["value"][handler_name]["formatter"] = 'formatter'
        if handler_class == self.VALID_HANDLER_CLASS[1]:
            self.handler["value"][handler_name]["filename"] = \
                handler_prefix + '.log'

    def set_logger(self, logger_name, level):
        """Set a logger's config (name, level, etc) with class validation"""
        self.logger = {"key": logger_name, "value": {logger_name: {}}}
        self.logger["value"][logger_name]["handlers"] = [self.handler["key"]]
        self.logger["value"][logger_name]["level"] = level

    def validate_handler_class(self, handler_class):
        """Validator.

        Validate if the handler's class is valid
        (either 'StreamHandler'or 'FileHandler')
        """
        if handler_class not in self.VALID_HANDLER_CLASS:
            logger = logging.getLogger()
            logger.error('Incorrect handler class name has been entered.')
            raise ValueError
