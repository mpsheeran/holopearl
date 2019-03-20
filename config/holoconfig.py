class Config:
    DISCORD_BOT_KEY = None
    LOG_LEVEL = 'INFO'


class DevelopmentConfig(Config):
    LOG_LEVEL = 'DEBUG'
    DISCORD_BOT_KEY = 'DEV_TOKEN_GOES_HERE'


class ProductionConfig(Config):
    LOG_LEVEL = 'INFO'
    DISCORD_BOT_KEY = 'PROD_TOKEN_GOES_HERE'

