#PYTHON VARS
PYCMD = python
PYTEST=$(PYCMD) -m unittest discover
B_NAME=antiserve

#COMMANDS

pytest:
	$(PYTEST) -s ./test/ -p "test_*.py"