clean:
	rm -rf *.pyc reg_settings* build/

test:
	./run-tests.sh

.PHONY:	clean test
