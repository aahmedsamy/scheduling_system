RUN = docker-compose exec -it web

makemigrations: # for make migrations files
	$(RUN) python manage.py makemigrations

create-super-user: # for creating new user with system wide privilege
	$(RUN) python manage.py createsuperuser

open_container_shell:
	$(RUN) sh

migrate-database:
	$(RUN) python manage.py migrate

system-start: # for building the system and run in
	docker-compose up --build

system-build: # for building the system
	docker-compose build

system-stop:
	$(RUN) down

system-clean:
	$(RUN) down -v