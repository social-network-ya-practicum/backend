### Temporary readme

# Backend for CSN project

**Stack**:
* Python 3.10
* Django Rest Framework
* Djoiser
* Postgres
* Docker

## Launch the project

### 1. Rename .env_example to .env
```
mv ./.env_example ./.env
```
### 2. Run docker-compose from /infra
```
docker-compose up -d --build
```
### 3. Make migrates and collectstatic
```
docker exec -it infra-web-1 python manage.py migrate && \
docker exec -it infra-web-1 python manage.py collectstatic --no-input
```
