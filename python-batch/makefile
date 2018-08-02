VERSION=2.0

.PHONY: build

integration: build
	sh -c '. venv/bin/activate; docker-compose up -d; pytest .; docker-compose down'

build: bootstrap
	docker build -t joatmon08/batcher:$(VERSION) .

push:
	docker push joatmon08/batcher:$(VERSION)

bootstrap: virtualenv
ifneq ($(wildcard requirements.txt),)
	venv/bin/pip install -r requirements.txt
endif

virtualenv:
	virtualenv -p python3 venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install --upgrade setuptools
