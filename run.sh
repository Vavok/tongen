#!/bin/bash
screen -X -S tongen quit
sleep 2
screen -dmS tongen bash -c 'python3.8 tongen.py'
