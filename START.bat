@echo off
color b
title Checking Requirements...
python get-pip.py

pip install -r REQUIREMENTS.txt

title requirements installed, running code...
python main.py
timeout 1
title Done, closing in 15 seconds...
timeout 15
exit