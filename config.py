
class BaseConfig:
    import os
    LOG_LEVEL = 'INFO'
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root


class DevelopmentConfig(BaseConfig):
    LOG_LEVEL = 'DEBUG'
    LOG_ROOT = True
    COMMAND_PREFIX = '$'


class ProductionConfig(BaseConfig):
    LOG_LEVEL = 'INFO'
    COMMAND_PREFIX = '!'
