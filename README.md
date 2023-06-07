![workflow](https://github.com/social-network-ya-practicum/backend/actions/workflows/main.yml/badge.svg?event=pull_request)
# Backend for CSN project

**Stack**:
* Python 3.10
* Django Rest Framework
* Djoiser
* Postgres
* Docker

## Launch the project

### 1. Git clone:
```
git clone https://github.com/social-network-ya-practicum/corporate-social-network.git && \
cd corporate-social-network/backend
```
### 2. Install depencies.
```
pip install -r requirements.txt
```
### 3. Rename .env_example to .env
```
mv ./.env_example ./.env
```
### 4. Run docker-compose from /infra
```
docker-compose up -d --build
```
### 5. Make migrates and collectstatic
```
docker exec -it infra-web-1 python manage.py migrate && \
docker exec -it infra-web-1 python manage.py collectstatic --no-input
```
### 6. Project documentation is available at:
http://80.87.106.53/redoc/ http://80.87.106.53/swagger/
