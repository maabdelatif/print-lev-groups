venv:	requirements.txt
	virtualenv -p python3 venv
	venv/bin/pip3 install --upgrade -r requirements.txt

lint:
	venv/bin/pylint *.py

example:
	venv/bin/python3 print_lev_groups.py --files first-names.txt --ratio 90

clean:
	rm -rf venv

test: venv
	venv/bin/python tests/*.py

