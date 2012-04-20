clean:
	rm -rf *.pyc **/*.pyc reg_settings* .coverage MANIFEST build/ dist/ \
	       _templater.so readme.html

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

readme:
	rst2html README.rst > readme.html

.PHONY:	clean build install test sdist upload readme
