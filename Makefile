clean:
	rm -rf *.pyc reg_settings* build/ MANIFEST dist/

test:
	./run-tests.sh

upload:	clean test
	python setup.py sdist upload

.PHONY:	clean test upload
