
### forms

```html
<form action="" method="post">

	<div>

		<label for="login-email">Email address</label>

		<input type="email" name="login-email" id="login-email" autofocus>

	</div>

</form>
```


<form action="" method="post">

<div>

<label for="login-email">Email address</label>

<input type="email" name="login-email" id="login-email" autofocus>

</div>

</form>


### checkbox
This also should be inside the form tag

```html
<label for="login-remember">

	<input type="checkbox" name="login-remember" id="login-remember"> Remember me

</label>
```


### Drop down

```html
<label for="oder-state">City</label>

<select name="order-state" id="order-state">

	<option value="Nairobi">Nairobi</option>
	
	<option value="Nairobi">Mombasa</option>
	
	<option value="Nairobi">Kilifi</option>
	
	<option value="Nairobi">Bungoma</option>
	
	<option value="Nairobi">Eldoret</option>

</select>
```


### Radio button
when you use the same name in radio button you can only select one, but if you use different names you can select multiple buttons

```html
<label for="team-large">

	<input type="radio" name="team-size" id="team-large" value="10+"> 10+ people

</label>
```

<label for="team-large">

<input type="radio" name="team-size" id="team-large" value="10+"> 10+ people

</label>

