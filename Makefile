init-venv:
    sudo apt-get install python3-venv && python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt
web-start:
	cd webserver; php -S localhost:8012
capture-start:
	python capture.py
detect-clusters:
	python plot-multiple-dbscan.py