.PHONY: install test demo

install:
	python -m pip install -e .

test:
	python -m pytest -q

demo:
	python -m devflow /estado --target .
