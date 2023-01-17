# HOLOPEARL

a Discord bot by @misterHaderach

#### Requirements

- Python3.9+
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

- !qrcode
    - creates a QR code based on your input text

- !download
    - uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) to download a video file. This currently downloads to the `/holodata` directory wherever Holopearl is running. For docker, this is a volume you can map to the Docker host by adding `-v holodata:/$DIRECTORY` to the `run` command.
- !challenge
    - challenge Holopearl to a duel
- !suggestion
    - Holopearl will keep track of suggestions you have!
    - note: there is no way to access these suggestions currently.
- !hello
    - say hi to Holopearl.

#### FAQs

- TBD - ask me some questions! 