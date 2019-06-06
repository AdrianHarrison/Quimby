#PYTHON VARS
PYCMD = python
PYTEST=$(PYCMD) -m unittest discover

#COMMANDS

pytest:
	$(PYTEST) -s ./test/ -p "test_*.py"
