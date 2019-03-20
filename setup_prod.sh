#!/bin/bash
scriptdir=$(dirname "$0")
if [[ -n $1 ]]
then
token=$1
else
if [[ $(grep -c PROD_TOKEN_GOES_HERE "$scriptdir/config/holoconfig.py") -eq 1 ]]
then
echo "Please input your bot token: "
read token
else
echo "Token already appears to be set. Exiting."; exit -1
fi
fi

#do the magic
sed -i "s/PROD_TOKEN_GOES_HERE/$token/g" "$scriptdir/config/holoconfig.py"