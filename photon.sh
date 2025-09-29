#!/bin/bash

sudo apt update

sudo apt install python3 python3-pip -y
sudo apt install python3-venv -y

python3 -m venv venv

source venv/bin/activate

sudo apt install python3-tk

pip3 install -r requirements.txt

python main.py

python src/entry_terminal_screen.py