run:
	uv run manage.py runserver

createsuperuser:
	uv run manage.py createsuperuser

makemigrations:
	uv run manage.py makemigrations

migrate:
	uv run manage.py migrate

lint:
	uv run pre-commit run --all-files
