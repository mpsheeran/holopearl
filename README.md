# HOLOPEARL

a Discord bot by @misterHaderach

#### Requirements

- Python3.7+
- pip
- a [Discord bot token](https://discordapp.com/developers/docs/topics/oauth2#bots)
- Docker (Optional) 

#### Local Setup

These instructions assume mac/linux. Windows users, you're on your own. Sorry.

1) `git clone <<this repository>>`

2) `cd <<repository root>>`

3) `virtualenv -p python3 env`

4) `source env/bin/activate`

5) `pip3 install -r pip-requirements.txt`

 
#### Usage

From the repository root:

1) `source env/bin/activate`

2) `export HOLOPEARL_BOT_TOKEN="<<TOKEN GOES HERE>>"`

3) `python3 . prod`  


#### Docker Setup & Usage

These instructions assume you already have Docker configured and running on your local machine.

1) `git clone <<this repository>>`

2) `cd <<repository root>>`

3) `docker build .`

4) `docker run -d -e HOLOPEARL_BOT_TOKEN="<<TOKEN_GOES_HERE>>" <<container ID>>"`


#### Capabilities

- TBD

#### FAQs

- TBD - ask me some questions! 