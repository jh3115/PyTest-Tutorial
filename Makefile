test-pretty:
	python -m pytest --verbose

test:
	python -m pytest --verbose -p "no:sugar"

test-cov:
	python -m pytest --verbose --cov=. --cov-report html