init:
	pip install -r requirements.txt

clean:
	find tests/bin/pickle/ -name '*.pickle' | xargs rm

test:
	nosetests tests
