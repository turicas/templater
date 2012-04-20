clean:
	rm -rf *.pyc **/*.pyc reg_settings* MANIFEST build/ dist/

build:
	python setup.py build

install:
	python setup.py install

test:	clean
	./run-tests.sh
	make clean

sdist:	clean test
	python setup.py sdist

upload:	clean test
	python setup.py sdist upload
	make clean

.PHONY:	clean build install test upload sdist
