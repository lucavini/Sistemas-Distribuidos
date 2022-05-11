#!/bin/bash

docker run --network=my_socket_ipc_network --name ipc_server_dns_name server &

sleep 2

docker run --network=my_socket_ipc_network partner1 &
docker run --network=my_socket_ipc_network partner2 &

sleep 2

docker run --network=my_socket_ipc_network client1 &
docker run --network=my_socket_ipc_network client2 &

