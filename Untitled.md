
```kotlin

items(filteredNotes) { item ->  
    CardM3(  
        note = item,  
        selectionMode = selectionMode,  
        isSelected = selectedItems.contains(item.id),  
        onTapClick = {  
            navController.navigate("edit/${item.title}/${item.body}/${item.id}")  
        },  
        onLongClick = {  
            selectionMode = true  
            selectedItems.add(item.id)  
        },  
        onSelectToggle = {  
            if (selectedItems.contains(item.id)) {  
                selectedItems.remove(item.id)  
                if (selectedItems.isEmpty()) selectionMode = false  
            } else {  
                selectedItems.add(item.id)  
            }  
        }  
    )  
}

```
