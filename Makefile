init:
	mkdir -p data/input
	mkdir -p data/output

install:
	pip3 install -r requirements.txt

run: init install
	python3 extract_grades.py

.PHONY: init install run