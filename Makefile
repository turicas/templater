clean:
	rm -rf *.pyc reg_settings* build/

test:
	./run-tests.sh

upload:	clean
	python setup.py sdist upload

.PHONY:	clean test
