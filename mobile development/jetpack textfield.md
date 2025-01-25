
```kotlin
var text by remember { mutableStateOf("Redmagic") }
TextField(  
  value = text,  
  onValueChange = {  
  newText -> text = newText },  
  label = {  
    Text(text = "Title")  
  },  
  leadingIcon = {  
    IconButton(onClick = {}) {  
      Icon(  
        imageVector = Icons.Filled.Email,  
        contentDescription = "Email Icon"  
      )  
    }  
  }  
  
  )
```

### outline textfield

```kotlin
OutlinedTextField(  
  value = text,  
  onValueChange = {  
  newText -> text = newText },  
  label = {  
    Text(text = "Title")  
  },  
  leadingIcon = {  
    IconButton(onClick = {}) {  
      Icon(  
        imageVector = Icons.Filled.Email,  
        contentDescription = "Email Icon"  
      )  
    }  
  }  
  
  )
```