venv: requirements.txt
	virtualenv -p python3 venv
	venv/bin/pip install --upgrade -r requirements.txt

test: venv
	venv/bin/python tests/*.py

