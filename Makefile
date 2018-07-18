venv: requirements.txt
	python3 -m virtualenv -p python3 venv
	venv/bin/pip install --upgrade -r requirements.txt

example: venv
	venv/bin/python print_lev_groups.py --files small-file.txt --ratio 60
