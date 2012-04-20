clean:
	rm -rf *.pyc **/*.pyc reg_settings* MANIFEST build/ dist/

build:
	python setup.py build

install:
	python setup.py install

test:	clean
	./run-tests.sh
	make clean

upload:	clean test
	python setup.py sdist upload

.PHONY:	clean build install test upload
