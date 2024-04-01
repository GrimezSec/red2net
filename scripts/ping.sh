#!/bin/bash

read -t ip_address

for ((i=1; i<=5; i++))
do
    ping -c 1 $ip_address

    sleep 1
done
