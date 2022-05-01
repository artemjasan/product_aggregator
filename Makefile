# Just build the application image
build:
	docker-compose build

# Create the containers without starting them.
# Can be run before migration on the first application start.
create:
	docker-compose up --no-start

# Start the containers
up:
	docker-compose up

# Shorthand to build and run the application without migration
build-up: build up

# Migrate the database
migrate:
	docker-compose run --rm web python aggregator_project/manage.py migrate
	docker-compose stop

# Create migrations
makemigrations:
	docker-compose run --rm web python aggregator_project/manage.py makemigrations
	docker-compose stop

# Run the testing
.PHONY: test
test:
	docker-compose run --rm web pytest
	docker-compose stop

# Run checks
.PHONY: checks
checks:
	docker-compose run --rm --no-deps web ./checks.sh

# Run pre-commit locally on all files
.PHONY: pre-commit
pre-commit:
	docker-compose run --rm --no-deps web pre-commit run --all-files
