# Camera placer
Find the optimal cameras' placement inside a given polygon using simmulated annealing algorithm.

## Setting up environment
1. `sudo apt install virtualenv virtualenvwrapper`
1. add to ~/.bashrc: `export WORKON_HOME=~/projects/VIRTUALENVS`
1. restart console
1. inside virtualenv install packages:
`pip3 install -r pip.requirements`

#### Virtual env helpers
`mkvirtualenv <name> --python=/usr/bin/python3.5` - creates new env and enables it
  
`workon <name>` - enable existing env

`deactivate` - leave env

## Running
`workon cameras`
  
`python main.py`
    
`usr/bin/time python main.py -F config.json`    


## Testing
`python -m unittest discover`

## MacOS environment
1. `brew install python3`
1. `pyvenv cameras`
1. `source cameras/bin/activate`
