run:
	uv run manage.py runserver

startapp:
	uv run manage.py startapp $(name)

createsuperuser:
	uv run manage.py createsuperuser

makemigrations:
	uv run manage.py makemigrations

migrate:
	uv run manage.py migrate

lint:
	uv run pre-commit run --all-files

print_posts:
	uv run manage.py print_posts

print_published_posts:
	uv run manage.py print_published_posts

create_post:
	uv run manage.py create_post -t "$(title)" -c "$(content)"

delete_post:
	uv run manage.py delete_post $(id)

update_post:
	uv run manage.py update_post $(id) -t "$(title)"

shell_plus:
	uv run manage.py shell_plus --print-sql

test_all:
	uv run manage.py test

create_docker_container:
	docker run \
	--name blog_db \
	-e POSTGRES_USER=admin \
	-e POSTGRES_PASSWORD=admin \
	-e POSTGRES_DB=blog_db \
	-p 5435:5432 \
	-v blog_db_data:/var/lib/postgresql/data \
	-d postgres:17

docker_run:
	docker start blog_db
