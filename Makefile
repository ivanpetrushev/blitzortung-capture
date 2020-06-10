web-start:
	cd webserver; php -S localhost:8012
capture-start:
	while true; do python3.6 capture.py; sleep 1; done
detect-clusters:
	python3.6 plot-multiple-dbscan.py