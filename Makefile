PYTHON ?= python
PYTHONPATH = backend/python

c-build:
	python backend/c/build.py

run-api:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run-tests:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m pytest -q tests

.PHONY: c-build run-api run-tests
