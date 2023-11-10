setup:
	python3 -m venv ~/.udacity-project-2
	#source ~/.udacity-project-2/bin/activate
	
install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv test_hello.py

lint:
	#hadolint Dockerfile #uncomment to explore linting Dockerfiles
	pylint --disable=R,C,W1203,W0702,C0301,R1710,W0703 app.py

all: install lint test