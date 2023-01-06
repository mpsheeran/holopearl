import sys
from holopearl.helpers import InitialSetup

# TODO: check to see if we have setup before?
isFreshInstall = True
if isFreshInstall:
    InitialSetup.insert_token()


def run():
    from holopearl.holopearl import HoloPearl
    env = sys.argv[1] if len(sys.argv) > 1 else 'dev'
    app = HoloPearl(bot_environment=env)
    app.run()


run()
