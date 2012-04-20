#!/bin/bash

if [ -z "$VIRTUAL_ENV" ]; then
    echo 'Error: you should be in a virtualenv. Create it using:'
    echo '  mkvirtualenv --no-site-packages templater-env'
    echo 'You need to have virtualenv and virtualenvwrapper installed:'
    echo '  pip install virtualenv virtualenvwrapper'
    exit 1
fi

clear
$VIRTUAL_ENV/bin/python setup.py build install
$VIRTUAL_ENV/bin/python /usr/local/bin/nosetests -dv --with-yanc
