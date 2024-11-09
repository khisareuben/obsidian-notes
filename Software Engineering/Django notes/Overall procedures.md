
1. Create an overall folder to hold everything
2. create the virtual environment
3. create the django project
4. inside the project create the app 
5. include the app in the settings.py file on installed apps
6. inside the app include templates folder
7. inside the templates create a folder with the same name of the app
	1. inside template/myapp create a .html file e.g. `base.html`
8.  then create the urls.py in myapp and make the necessary changes in both urls
9. Then go to my project folder and create a staticfiles folder which will hold our css and images
	1. then in the static folder create two folders one called **css** and the other called **images**
	2. then create the style.css and the images respectively
10. in the settings file, on the static_url change **static** to **staticfiles**
	1. then below the valriable write another code
		```python
		MEDIA_URL = '/images/'  #(optional)
		
		STATIC_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]
		or
		STATICFILES_DIRS = [BASE_DIR / 'staticfiles']
		 
		# i prever the second one coz i keep gettting errors with the first one
```


11. Then link the css file in the html file
```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">

your html code

```