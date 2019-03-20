import sys
from holopearl.holopearl import HoloPearl

env = sys.argv[1] if len(sys.argv) > 1 else 'dev'
app = HoloPearl(environment=env)
app.run()
