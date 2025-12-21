# Minimalist Django Blog Platform

A modern, production-ready blog application built with Django and Tailwind CSS. This platform helps authors publish content and interact with a community of readers through comments, reactions, and subscriptions.

## 🚀 Features

### Phase 1: Core Content Management

- **Post Management**: Create, edit, and publish rich-text posts using CKEditor.
- **User System**: Custom user model with extended profile fields.
- **Responsive Design**: Mobile-first UI built with Tailwind CSS.

### Phase 2: User Engagement

- **Authentication**: Full registration and login system.
- **Comments**: Nested commenting system (threaded replies) using `django-mptt`.
- **Newsletter**: Email subscription for both guests and registered users.
- **User Profiles**: Manage personal details and subscription settings.

### Phase 3: Advanced Features & Optimization

- **Tagging System**: Organize posts with #tags.
- **Search**: Full-text search for posts.
- **Interactivity**: AJAX-powered "Like" button for posts.
- **SEO**: Dynamic Meta tags, Open Graph support, sitemaps, and robots.txt.
- **Performance**: Database query optimization (`select_related`, `prefetch_related`) and view caching.
- **Deployment Readiness**: Dockerized application with Whitenoise for static files.

## 🛠️ Technology Stack

- **Backend**: Python 3.12+, Django 5.2+
- **Database**: SQLite (Development/MVP), easily switchable to PostgreSQL
- **Frontend**: HTML5, Tailwind CSS (CDN/Standalone)
- **Dependencies**: `django-ckeditor`, `django-mptt`, `whitenoise`, `gunicorn`

## 📦 Installation

### Option 1: Docker (Recommended)

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/ahmedxxzz/Django-Modern-Blog.git
    cd Django-Modern-Blog/week_5
    ```
2.  **Run with Docker Compose**:
    ```bash
    docker-compose up --build
    ```
    The application will be available at `http://localhost:8000`.

### Option 2: Local Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/ahmedxxzz/Django-Modern-Blog.git
    cd Django-Modern-Blog/week_5
    ```
2.  **Create a Virtual Environment**:
    ```bash
    python -m venv env
    # Windows
    .\env\Scripts\activate
    # Linux/MacOS
    source env/bin/activate
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run Migrations**:
    ```bash
    python manage.py migrate
    ```
5.  **Create Superuser**:
    ```bash
    python manage.py createsuperuser
    ```
6.  **Run Server**:
    ```bash
    python manage.py runserver
    ```

## 📝 Usage

1.  **Access Admin Panel**: Go to `/admin` and log in with your superuser credentials to post articles.
2.  **Register as User**: Go to `/accounts/register/` to create a standard user account.
3.  **Interact**: Read posts, search for topics, like articles, and leave nested comments.
