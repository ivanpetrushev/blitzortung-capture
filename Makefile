web-start:
	cd webserver; php -S localhost:8012
capture-start:
	python capture.py
detect-clusters:
	python plot-multiple-dbscan.py