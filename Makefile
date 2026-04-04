run-server:
	python app/main.py

run-tests:
	pytest

run-integration-tests:
	pytest -m integration