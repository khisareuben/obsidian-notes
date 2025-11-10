
```kotlin

else {  
    LazyVerticalGrid(  
        columns = GridCells.Fixed(2),  
        modifier = Modifier.fillMaxSize(),  
        contentPadding = PaddingValues(  
            start = 8.dp,  
            end = 8.dp,  
            top = innerPadding.calculateTopPadding() + 8.dp,  
            bottom = innerPadding.calculateBottomPadding() + 8.dp  
        ),  
        verticalArrangement = Arrangement.spacedBy(8.dp, alignment = Alignment.Top),  
        horizontalArrangement = Arrangement.spacedBy(8.dp)  
    ) {  
        items(notes) {  
            NoteCard(note = notes, onClick = {})  
        }  
    }}

```

```kotlin

@Composable  
fun NoteCard(note: Note, onClick: () -> Unit){  
    Card(onClick = onClick,  
        modifier = Modifier.padding(2.dp).heightIn(200.dp),  
        elevation = CardDefaults.cardElevation(8.dp),  
        shape = RoundedCornerShape(10.dp)  
    ) {  
        Column(modifier = Modifier.padding(12.dp)) {  
  
            Text(  
                text = note.content.take(50) + if (note.content.length > 50) "..." else "",  
                style = MaterialTheme.typography.bodyMedium,  
                maxLines = 5  
            )  
  
  
        }  
    }}

```