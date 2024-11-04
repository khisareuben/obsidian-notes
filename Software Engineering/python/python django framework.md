
### Django Comprehensive Notes

#### Topics

1. Introduction to Django
    
2. Setting Up a Django Project
    
3. Django Project Structure
    
4. Models and Databases
    
5. Views and URL Routing
    
6. Templates and Static Files
    
7. Forms and User Input
    
8. Authentication and Authorization
    
9. Django Admin Interface
    
10. Deployment and Production
    

### 1. Introduction to Django

- Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.
    
- Follows the "Don't Repeat Yourself" (DRY) principle.
    
- Provides an ORM (Object-Relational Mapping) for database manipulation.
    

### 2. Setting Up a Django Project

- **Create a project directory**:

	```bash
	mkdir <name>
	cd name
```
    
- **create a virtual environment**:

	```bash
	python3 -m venv <name-env>
	
	source name-env/Scripts/activate
```
    
- **create django project**: 

	```bash
	pip3 install django
	
	python3 -m django version

	django-admin startproject <project-name>
```

- **Run development server**: 

	```bash
	cd project-name
	python3 manage.py runserver
```
- Access the server at `http://127.0.0.1:8000/`


## How to create an app in django

An app is just different sections of the website, e.g `home` `about` `contacts`  and others
This should be done inside the projects folder

```bash
python -m django startapp myapp
```


### 3. Django Project Structure

- **[manage.py](https://manage.py/?form=MG0AV3)**: Command-line utility for project management.
    
- **projectname/**: Main project folder.
    
    - **[settings.py](https://settings.py/?form=MG0AV3)**: Configuration settings.
        
    - **[urls.py](https://urls.py/?form=MG0AV3)**: URL declarations.
        
    - **[wsgi.py](https://wsgi.py/?form=MG0AV3)**: WSGI configuration for deployment.
        
    - **[asgi.py](https://asgi.py/?form=MG0AV3)**: ASGI configuration for deployment.
        

### 4. Models and Databases

- **Define Models**: Create a model in `models.py`.
    
    python
    
    ```
    from django.db import models
    class Article(models.Model):
        title = models.CharField(max_length=100)
        content = models.TextField()
    ```
    
- **Migrations**:
    
    - Create Migration: `python manage.py makemigrations`
        
    - Apply Migration: `python manage.py migrate`
        
- **Querying**:
    
    python
    
    ```
    articles = Article.objects.all()
    article = Article.objects.get(id=1)
    ```
    

### 5. Views and URL Routing

- **Define Views**: Create view functions in `views.py`.
    
    python
    
    ```
    from django.shortcuts import render
    def home(request):
        return render(request, 'home.html')
    ```
    
- **URL Configuration**: Map URLs to views in `urls.py`.
    
    python
    
    ```
    from django.urls import path
    from . import views
    urlpatterns = [
        path('', views.home, name='home'),
    ]
    ```
    

### 6. Templates and Static Files

- **Templates**: Store HTML files in a `templates` folder.
    
    html
    
    ```
    <!-- home.html -->
    <!DOCTYPE html>
    <html>
    <head><title>Home</title></head>
    <body><h1>Welcome to Django</h1></body>
    </html>
    ```
    
- **Static Files**: Store CSS, JavaScript, and images in a `static` folder. Reference them in templates using `{% load static %}` and `{% static 'path/to/file' %}`.
    

### 7. Forms and User Input

- **Create Forms**: Define forms in `forms.py`.
    
    python
    
    ```
    from django import forms
    class ArticleForm(forms.ModelForm):
        class Meta:
            model = Article
            fields = ['title', 'content']
    ```
    
- **Handle Forms in Views**:
    
    python
    
    ```
    def create_article(request):
        if request.method == 'POST':
            form = ArticleForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            form = ArticleForm()
        return render(request, 'create_article.html', {'form': form})
    ```
    

### 8. Authentication and Authorization

- **User Authentication**: Use Django's built-in authentication system.
    
    python
    
    ```
    from django.contrib.auth import authenticate, login
    user = authenticate(request, username='username', password='password')
    if user is not None:
        login(request, user)
    ```
    
- **Protecting Views**: Use decorators to restrict access.
    
    python
    
    ```
    from django.contrib.auth.decorators import login_required
    @login_required
    def dashboard(request):
        return render(request, 'dashboard.html')
    ```
    

### 9. Django Admin Interface

- **Activate Admin Site**: Add your app to `INSTALLED_APPS` in `settings.py`.
    
    python
    
    ```
    INSTALLED_APPS = [
        'django.contrib.admin',
        ...
    ]
    ```
    
- **Create Admin User**: Run `python manage.py createsuperuser`.
    
- **Register Models**: Register models in `admin.py`.
    
    python
    
    ```
    from django.contrib import admin
    from .models import Article
    admin.site.register(Article)
    ```
    

### 10. Deployment and Production

- **Prepare for Deployment**: Set `DEBUG = False` in `settings.py`.
    
- **Database Configuration**: Use a production-ready database like PostgreSQL.
    
- **Static Files**: Collect static files using `python manage.py collectstatic`.
    
- **Deploying**: Use platforms like Heroku, AWS, or DigitalOcean. Follow their specific instructions for deploying Django applications.