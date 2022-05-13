#!/bin/bash

docker run --memory="8m" --cpus="0.02" -it server server-alt.py >> serverOutput.txt &

# sleep 10

docker run --memory="10m" --cpus="1" -i partner1 partner.py >> partnerOutput.txt &
docker run --memory="10m" --cpus="1" -i partner2 partner.py >> partnerOutput.txt &

sleep 5

docker run -i client1 client.py >> clientOutput.txt &
