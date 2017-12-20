# cameras

install virtualenv:
sudo apt install virtualenv virtualenvwrapper

add to ~/.bashrc:
export WORKON_HOME=~/projects/VIRTUALENVS
source /usr/local/bin/virtualenvwrapper.sh

restart console and:
mkvirtualenv <name> - creates new env and enables it 
workon <name> - enable existing env
deactivate - leave env

inside virtualenv install packages:
pip3 install -r pip.requirements
