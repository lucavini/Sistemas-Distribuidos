#!/bin/bash

T=0
QTD=20
while [ $T -le $QTD ]; do
    echo "Criando Containers"
    python3 client.py
    let T=T+1
done
