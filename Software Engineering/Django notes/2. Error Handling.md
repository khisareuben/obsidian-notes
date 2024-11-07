## Error Handling

- **Client error responses** 
	400 - bad request. parameter passed the request is not what the server expects 
	401 - User must log into an account before processing the request
	403 - permission denied. the webserver refuses to process it, user does not have the required permission to view the resource
	404 - page not found. the requested resource cannot be found on the server

- **Sever error responses**
	Application failure or Response time limit exceeded
	500 - server error. internal server error, the server failed to process the request

#### settings.py(myproject folder)
change the **DEBUG** value to false
add a value in the allowed host
```python
DEBUG = False

ALLOWED_HOST = ['*'] # all possible hosts
```

##### to create a custom error page
create a `views.py`  file in the myproject folder
the open the urls.py in the myproject folder

```python
# in the new views.py
from django import HttpResponse
def handler404(request, exception):
	return HtttpResponse("404 : page not found")
```


```python
# urls.py we add another urlpattern
handler404 = "myproject.views.handler404"
```