VERSION=1.0

.PHONY: build


build: bootstrap
	docker build -t joatmon08/testapp:$(VERSION) .
	

push:
	docker push joatmon08/testapp:$(VERSION)
	docker tag joatmon08/testapp:$(VERSION) joatmon08/testapp:latest
	docker push joatmon08/testapp:latest
	

bootstrap: virtualenv
ifneq ($(wildcard requirements.txt),)
	venv/bin/pip install -r requirements.txt
endif

virtualenv:
	virtualenv -p python3 venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install --upgrade setuptools
