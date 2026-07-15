# Интернет-магазин ДВФУ

## Инструкция по запуску

### 1. Backend (Django)
```bash
# Создание среды
python -m venv venv
venv\Scripts\activate

# Установка и запуск
pip install -r requirements.txt
cd backend
python manage.py migrate
python manage.py runserver
```

### 2. Frontend (Quasar)
```bash
cd frontend
npm install
quasar dev
```
