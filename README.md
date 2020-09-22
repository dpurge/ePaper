# ePaper

## Setup

```powershell
python -m venv .venv
.venv\Scripts\activate.ps1

python -m pip install --upgrade pip

pip install -r requirements.txt

deactivate
```

Activate shell environment: `.venv\Scripts\activate.ps1`

Deactivate shell environment: `deactivate`

To update `requirements.txt`: `pip freeze > requirements.txt`

## API

Run the server:

D:\pgm\php\php.exe -S localhost

## DISPLAY

pip install esptool
pip install adafruit-ampy
pip install freetype-py

https://github.com/peterhinch/micropython-font-to-py

esptool --port COM3 flash_id
esptool --chip esp32 --port COM3 erase_flash
esptool --chip esp32 --port COM3 write_flash -z 0x1000 esp32-20181108-v1.9.4-683-gd94aa577a.bin

ampy --port COM3 --baud 115200 mkdir /lib
ampy --port COM3 --baud 115200 put lib/jdp_epaper.py /lib/jdp_epaper.py
ampy --port COM3 --baud 115200 put lib/jdp_network.py /lib/jdp_network.py
ampy --port COM3 --baud 115200 put lib/jdp_flashcards.py /lib/jdp_flashcards.py
ampy --port COM3 --baud 115200 put lib/font_pol_64.py /lib/font_pol_64.py
ampy --port COM3 --baud 115200 put config.json
ampy --port COM3 --baud 115200 put main.py
ampy --port COM3 --baud 115200 ls

Commands:
  get    Retrieve a file from the board.
  ls     List contents of a directory on the board.
  mkdir  Create a directory on the board.
  put    Put a file or folder and its contents on the...
  reset  Perform soft reset/reboot of the board.
  rm     Remove a file from the board.
  rmdir  Forcefully remove a folder and all its...
  run    Run a script and print its output.

ampy --port COM3 --baud 115200 ls
ampy --port COM3 --baud 115200 get /boot.py > boot.py
ampy --port COM3 --baud 115200 put main.py
ampy --port COM3 --baud 115200 rm /project.pymakr
ampy --port COM3 --baud 115200 run main.py
ampy --port COM3 --baud 115200 run test.py

import os
os.listdir()

with open('webrepl_cfg.py', 'r') as f: f.read()
with open('hello.txt', 'w') as f: f.write('Hello World')

import machine
print(dir(machine))
help('modules')
