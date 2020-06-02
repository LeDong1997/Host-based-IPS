# HostIDPS
Building Host based IDPS for Linux and Windows

# Windows

## Setup environment
This project using `Python 3.8.1` on Windows 10 64 bit
About IDE and Editor: Pycharm, Visual Studio Code, Sublime Text 3
### Create Virtual Environment
`$ cd HostIDPS`

`$ python -m venv venv`

Run project in virtual environment

`$ .\venv\Scripts\activate`

`$ python demo.py`

### On Visual Studio Code

`Error: Cannot be loaded because running scripts is disabled on this system.`

To fix the error, run the command below

`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`

Back to step create venv

## Install library for project
### # Install crypto library
`$ pip install pycryptodome`
### # Install API windows event log 
`$ pip install pywin32`

# Linux

## Install library for project
### # Install crypto library
`$ pip install pycrypto`