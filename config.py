
class BaseConfig:
    import os
    DISCORD_BOT_KEY = None
    LOG_LEVEL = 'INFO'
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root


class DevelopmentConfig(BaseConfig):
    LOG_LEVEL = 'DEBUG'
    DISCORD_BOT_KEY = 'DEV_TOKEN_GOES_HERE'


class ProductionConfig(BaseConfig):
    LOG_LEVEL = 'INFO'
    DISCORD_BOT_KEY = 'PROD_TOKEN_GOES_HERE'

