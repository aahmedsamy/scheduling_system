# SchedulingSystem

## Running the app locally

```shell script
docker-compose up --build
```

### Apply database migrations in a separate terminal tab

```sh
docker exec -it scheduling_system_web_1 sh -c "python manage.py migrate"
```

### Create test users (you can generate as many users as you want by repeating the following steps)
#### _**NOTE**_: _all users has all privileges_
```sh
docker exec -it scheduling_system_web_1 sh -c "python manage.py createsuperuser"
```
### NOTE: you will be asked for email and password to generate the user

# TESTING
### 1- Navigate to [localhost:8000/admin/](http://localhost:8000/admin/) and login
### 2- Navigate to [localhost:8000/graphql/](http://localhost:8000/graphql/) for playground
#### NOTE: the playground queries is documented (see docs in the top right corner)
