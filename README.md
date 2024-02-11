# Restaurant API

### Для работы с приложением клонируйте репозиторий:
```
git clone https://github.com/VoronovaDA/restaurant_api_fastapi.git  
```
### Установите виртуальное окружение и зависимости:
```
python -m venv venv
```
```
venv/Scripts/activate
```
```
pip install -r requirements.txt
```
### Настройте БД:
- В папке .env пропишите данные подключения к postgreSQL
- В терминале создайте БД:
```
createdb -U username dbname
```
- Или запустите docker
```
docker-compose up -d
```
### Для миграций, создайте папку с миграциями и конфигурационный файл для алембика:
```
alembic init -t async alembic  
```
### В alembic/env.py:

- Задайте адрес БД
```
target_metadata = Base.metadata
```
- Перезапишите sqlalchemy.url на url вашей БД
```
config.set_main_option("sqlalchemy.url", DATABASE_URL)
```
### Создайте миграции
```
alembic revision --autogenerate -m "comment" 
```
### Проведите миграции
```
alembic upgrade heads
```
### Для запуска приложения в терминале введите команду:
```
 uvicorn main:app --reload
```
### После запуска документация доступна по адресу: 
- http://127.0.0.1:8000/docs
