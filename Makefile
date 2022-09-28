CUSTOM_COMPILE_COMMAND = 'make update-deps'

init:
	python -m venv .venv
	. .venv/bin/activate

install:
	pip install --upgrade -r requirements/main.txt

install-dev:
	pip install --upgrade -r requirements/dev.txt

update: update-deps init

update-deps:
	pip install --upgrade pip-tools pip setuptools
	CUSTOM_COMPILE_COMMAND=$(CUSTOM_COMPILE_COMMAND) pip-compile --upgrade --build-isolation --generate-hashes --output-file requirements/main.txt requirements/main.in
	CUSTOM_COMPILE_COMMAND=$(CUSTOM_COMPILE_COMMAND) pip-compile --upgrade --build-isolation --generate-hashes --output-file requirements/dev.txt requirements/dev.in

run-datasette:
	datasette serve \
		--metadata datasette/metadata.json \
		--static static:datasette/static/ \
		--template-dir=datasette/templates \
		datasette/data.db

run-scrape:
	python -m src

publish:
	datasette publish cloudrun \
		--extra-options="--setting default_cache_ttl 300 --setting sql_time_limit_ms 5000 --setting facet_time_limit_ms 2000" \
		--metadata datasette/metadata.json \
		--static static:datasette/static/ \
		--template-dir=datasette/templates \
		--service=tracking-luma-outages \
		datasette/data.db

install-precommit:
	pre-commit install

run-precommit:
	pre-commit run --all-files

.PHONY: update-deps init update
