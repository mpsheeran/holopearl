from holopearl.exception import HoloError
from config import BaseConfig


class InitialSetup:
    def __init__(self):
        pass

    @staticmethod
    def insert_token():
        import os
        token = os.getenv('HOLOPEARL_BOT_TOKEN')
        config_path = f"{BaseConfig.ROOT_DIR}/config.py"
        print(f"Token: {token}")
        if token:
            with open(config_path, 'r') as config_file:
                config_data = config_file.read()

            config_data = config_data.replace('PROD_TOKEN_GOES_HERE', token)

            with open(config_path, 'w') as config_file:
                config_file.write(config_data)

        else:
            raise HoloError("'HOLOPEARL_BOT_TOKEN' environment variable not set; exiting.")