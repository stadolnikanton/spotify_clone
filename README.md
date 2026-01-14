# Spotify Clone

Клон музыкального сервиса с возможностью воспроизведения треков и авторизацией пользователей.

## Особенности

* 🎵 Воспроизведение музыки (Web Player)
* 👤 Регистрация и вход пользователей
* 🎨 Современный интерфейс с Bootstrap
* 🔍 Поиск по песням и артистам
* 🎭 Фильтрация по жанрам
* 📱 Адаптивный дизайн

## Технологии

* **Backend**: Django 5.2.7
* **Database**: PostgreSQL
* **Frontend**: Bootstrap 5.3.3
* **Python**: 3.x

## Структура проекта

```
spotify_clone/
├── app/                    # Основное приложение
│   ├── models.py          # Модели: Genre, Artist, Album, Song
│   ├── views.py           # Представления
│   ├── forms.py           # Формы регистрации
│   ├── urls.py            # URL-маршруты приложения
│   └── admin.py           # Админ-панель
├── musicPortal/           # Настройки проекта
│   ├── settings.py        # Конфигурация Django
│   └── urls.py            # Главные URL-маршруты
├── templates/             # HTML шаблоны
│   ├── base.html         # Базовый шаблон
│   ├── main.html         # Главная страница
│   ├── login.html        # Страница входа
│   └── register.html     # Страница регистрации
├── static/               # Статические файлы
│   └── css/
│       └── styles.css    # Пользовательские стили
└── media/                # Загруженные файлы (создается автоматически)
```

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd spotify_clone
```

### 2. Установка системных зависимостей

**Для Linux (Debian/Ubuntu):**

```bash
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip libpq-dev postgresql-client
```

**Для macOS:**

```bash
brew install postgresql
```

**Для Windows:**

Установите PostgreSQL с официального сайта: https://www.postgresql.org/download/windows/

### 3. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 4. Установка зависимостей Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Примечание**: Если возникают проблемы с установкой `psycopg2-binary`, убедитесь, что установлены системные зависимости (см. шаг 2).

### 5. Настройка переменных окружения

Скопируйте файл `.env.example` в `.env` и заполните значения:

```bash
cp .env.example .env
```

Затем отредактируйте `.env` файл и укажите свои значения:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=spotify_clone
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

**Важно**: Файл `.env` уже добавлен в `.gitignore` и не будет закоммичен в репозиторий.

### 6. Настройка базы данных

Создайте базу данных PostgreSQL:

```sql
CREATE DATABASE spotify_clone;
```

### 7. Применение миграций

```bash
python manage.py migrate
```

### 8. Создание суперпользователя (опционально)

```bash
python manage.py createsuperuser
```

### 9. Запуск сервера разработки

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000/

## Использование

### Админ-панель

Для управления контентом (артисты, альбомы, песни, жанры) используйте админ-панель:
http://127.0.0.1:8000/admin/

### Основные функции

1. **Регистрация**: Создайте новый аккаунт на странице `/register/`
2. **Вход**: Войдите в систему на странице `/login/`
3. **Просмотр песен**: На главной странице отображаются все доступные песни
4. **Поиск**: Используйте поисковую строку для поиска по названию песни или артисту
5. **Фильтрация**: Выберите жанр для фильтрации песен
6. **Воспроизведение**: Нажмите на кнопку воспроизведения в карточке песни

## Модели данных

- **Genre**: Жанры музыки
- **Artist**: Артисты/исполнители
- **Album**: Альбомы
- **Song**: Песни/треки

## Разработка

### Добавление контента

Контент можно добавлять через админ-панель Django или через Django shell:

```bash
python manage.py shell
```

### Отладка

Для разработки включен `django-debug-toolbar`. Он доступен только в режиме DEBUG.

## Лицензия

Учебный проект для изучения Django.

## Автор

© 2025 Учебный проект Django Music
