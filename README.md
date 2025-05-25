# Импорт и экспорт данных Miro

**Импорт и экспорт данных Miro** - это софт для работы с элементами доски Miro, с помощью Api

## Требования 

Для запуска софта необходимы следующие компоненты:

- **Python 3.9+**
- **API-ключ Miro**
- **PostgreSQL**

## Руководство по сборке и запуску

Представлено два вида софта, веб версия и интерфейс командной строки(CLI), для работы с CLI перейдите в ветку cli-ver.

### 1. Клонирование репозитория
1. Склонируйте репозиторий игры с GitHub, используя следующую команду:
   ```bash
   git clone https://github.com/Sepl-flek/API_MIRO_TSPP

### 2. Установка пакетов
1. Установите нужные пакеты из requirements.txt:
   ```bash
   pip install -r requirements.txt

### 3. Настройка базы данных
1. Войдите в консоль PostgreSQL:
   ```bash
   psql -U postgres
2. Создайте базу данных (замените mydb на нужное имя):
   ```bash
   CREATE DATABASE mydb;
3. Создайте пользователя (замените myuser и mypassword на свои значения):
   ```bash
   CREATE USER myuser WITH PASSWORD 'mypassword';
4. Назначьте привилегии:
   ```bash
   GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
   ALTER DATABASE mydb OWNER TO myuser;
   \q
5. Создайте файл .env в корне проекта и добавьте настройки БД:
   ```ini
   DB_NAME=mydb
   DB_USER=myuser 
   DB_PASSWORD=mypassword
   DB_HOST=localhost
   DB_PORT=5432
6. Применение миграций:
   ```bash
   cd src/mirotspp
   python manage.py migrate

### 4. Запуск проекта
1. Запустите сервер:
   ```bash
   python manage.py runserver
2. Зарегестрируйтесь по адресу accounts/signup.
3. После регистрации у вас откроется ваш профиль, где вы можете нажать кнопку my boards.
4. После можете, добавлять вашу доску, и работать с ней!
