#
# Lovingly adapted from Michal Young’s example
#

PY = python3.4      
PYVENV = pyvenv-3.4   
PORT = 5601     

install:	CONFIG.py
	rm -rf env  # In case it is already there
	$(PYVENV) env
	(. env/bin/activate ; pip3 install -r requirements.txt)

test:	env CONFIG.py
	(. env/bin/activate; $(PY) flask_main.py)

run:	env CONFIG.py
	(. env/bin/activate; gunicorn -b 0.0.0.0:$(PORT) dispatch_backend:app) &

env:
	build

CONFIG.py:  CONFIG.base.py
	cp CONFIG.base.py CONFIG.py
