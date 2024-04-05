#!/bin/bash

if [[ "$@" =~ "-a" ]]; then
    echo "red2net test successful!"
else
    echo "Failed!"
fi
