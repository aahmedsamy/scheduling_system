# SchedulingSystem

## Running the app locally

**Note:** If you're building the docker image for the first time, copy requirements-{ENV}.txt from packaging/requirements/ to the project's root.

### Copy requirements file

```sh
cp packaging/requirements/requirements.dev.txt requirements.txt
```

### Copy environment file

```shell script
cp packaging/environment/.env.dev.example .env.dev
```

### **NOTE: Make sure Docker is installed and running.**
### Build docker-compose
```shell script
docker-compose up --build
```

### Apply database migrations in a separate terminal tab

```sh
docker-compose run web python manage.py migrate
```

### Create test users (you can generate as many users as you want by repeating the following steps)
#### _**NOTE**_: _all users has all privileges_
```sh
 docker-compose run web python manage.py createsuperuser
```
### NOTE: you will be asked for email and password to generate the user

# TESTING
### 1- Navigate to [localhost:8000/admin/](http://localhost:8000/admin/) and login
### 2- Navigate to [localhost:8000/graphql/](http://localhost:8000/graphql/) for playground
#### NOTE: the playground queries is documented (see docs in the top right corner)
 