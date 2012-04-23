#!/bin/bash

if [ -z "$VIRTUAL_ENV" ]; then
    echo 'Error: you should be in a virtualenv. Create it using:'
    echo '  mkvirtualenv --no-site-packages templater-env'
    echo 'You need to have virtualenv and virtualenvwrapper installed:'
    echo '  pip install virtualenv virtualenvwrapper'
    exit 1
fi

clear
make clean build
cp $(find build/ -name _templater.so) .
$VIRTUAL_ENV/bin/python `which nosetests` -dv \
    --with-coverage --cover-package templater --with-yanc
