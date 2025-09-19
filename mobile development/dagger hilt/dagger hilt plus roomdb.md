



## Step-by-Step: Room + ViewModel + Koin + Jetpack Compose

### ✅ 1. Add Koin Dependencies

In your `build.gradle` (app-level):

#### ✅ 1. **Create the columns of the database** : These are the different sections that will be in your database /data
#### `Note.kt`



```kotlin
@Entity  
data class Todo(  
    val title: String,  
    val body: String,  
    @PrimaryKey(autoGenerate = true)  
    val id: Int = 0  
)
```

#### `NoteDao.kt`

#### 2. **Create the Dao(Data access object)** : This will help interact with the database and performing functions like insert, delete, update /data

```kotlin
@Dao  
interface TodoDao {  
  
    @Query("SELECT * FROM todo")  
    fun getAllData(): Flow<List<Todo>>  
  
    @Insert(onConflict = OnConflictStrategy.REPLACE)  
    suspend fun insertData(todo: Todo)  
  
    @Update  
    suspend fun updateData(todo: Todo)  
  
    @Delete  
    suspend fun deleteData(todo: Todo)  
}
```

#### `NoteDatabase.kt`

#### **Create the database** : This will integrate the columns and the dao together /data

```kotlin
@Database(entities = [Todo::class], version = 1)  
abstract class TodoDatabase: RoomDatabase() {  
  
    abstract fun getDao(): TodoDao  
  
}
```

### ✅ 3. Create Repository and ViewModel

#### `NoteRepository.kt`

#### 4. Create a notes event (real action)/presentation

```kotlin

class TodoRepository @Inject constructor(private val dao: TodoDao) {  
  
    fun getAllData(): Flow<List<Todo>> = dao.getAllData()  
  
    suspend fun insertData(todo: Todo) = dao.upsertData(todo)  
  
    suspend fun updateData(todo: Todo) = dao.updateData(todo)  
  
    suspend fun deleteData(todo: Todo) = dao.deleteData(todo)  
}

```

#### `NoteViewModel.kt`

#### 5. Create your viewModel /presentation

```kotlin

@HiltViewModel
class MyViewModel @Inject constructor(
    private val repository: TodoRepository
) : ViewModel() {

    val notesList: StateFlow<List<Todo>> = repository
        .getAllData()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    fun insertData(todo: Todo) {
        viewModelScope.launch {
            repository.insertData(todo)
        }
    }

    fun updateData(todo: Todo) {
        viewModelScope.launch {
            repository.updateData(todo)
        }
    }

    fun deleteData(todo: Todo) {
        viewModelScope.launch {
            repository.deleteData(todo)
        }
    }
}


```



## What Is a Koin Module?

A **Koin module** is like a **recipe** that tells Koin how to create and provide the things your app needs—like your database, DAO, repository, and ViewModel.

You write this recipe once, and Koin uses it to "cook up" the objects whenever your app asks for them.

## 🧩 Let's Break Down the Koin Module Line by Line

Here’s the code again:

```kotlin

@HiltAndroidApp
class MyApp : Application()


```

Register it in `AndroidManifest.xml`:

```xml
<application
    android:name=".MyApp"
    ... >
```

```kotlin

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): TodoDatabase {
        return Room.databaseBuilder(
            context,
            TodoDatabase::class.java,
            "todo.db"
        ).build()
    }

    @Provides
    fun provideTodoDao(db: TodoDatabase): TodoDao = db.getDao()

    @Provides
    fun provideRepository(dao: TodoDao): TodoRepository = TodoRepository(dao)
}



```


This is the UI but its not complete so put it in a function and pass the viewmodel as an argument...


```kotlin

@Composable  
fun MainUI(  
    viewModel: MyViewModel = hiltViewModel()
) {  
    val notes by viewModel.notesList.collectAsState()  
  
    var showDialog by remember { mutableStateOf(false) }  
    var name by remember { mutableStateOf("") }  
    var body by remember { mutableStateOf("") }  
    var noteToDelete by remember { mutableStateOf<Todo?>(null) }  
    var noteToEdit by remember { mutableStateOf<Todo?>(null) }  
  
    Surface(  
        modifier = Modifier.fillMaxSize(),  
        color = MaterialTheme.colorScheme.background  
    ) {  
        Column(  
            modifier = Modifier.padding(16.dp),  
            verticalArrangement = Arrangement.spacedBy(12.dp)  
        ) {  
            TextField(  
                value = name,  
                onValueChange = { name = it },  
                placeholder = { Text("Title") }  
            )  
            TextField(  
                value = body,  
                onValueChange = { body = it },  
                placeholder = { Text("Body") }  
            )  
            Button(onClick = {  
                if (noteToEdit != null) {  
                    val updated = noteToEdit!!.copy(title = name, body = body)  
                    viewModel.updateData(updated)  
                    noteToEdit = null  
                } else {  
                    val todo = Todo(title = name, body = body)  
                    viewModel.upsertData(todo)  
                }  
                name = ""  
                body = ""  
            }) {  
                Text(if (noteToEdit != null) "Update Note" else "Add Note")  
            }  
  
            LazyColumn {  
                items(notes) { note ->  
                    Card(  
                        modifier = Modifier  
                            .fillMaxWidth()  
                            .clickable {  
                                name = note.title  
                                body = note.body  
                                noteToEdit = note  
                            }  
                            .combinedClickable(  
                                onClick = {  
                                    name = note.title  
                                    body = note.body  
                                    noteToEdit = note  
                                },  
                                onLongClick = {  
                                    noteToDelete = note  
                                    showDialog = true  
                                }  
                            ),  
                        elevation = CardDefaults.cardElevation(4.dp)  
                    ) {  
                        Column(modifier = Modifier.padding(12.dp)) {  
                            Text(text = note.title, style = MaterialTheme.typography.titleMedium)  
                            Text(text = note.body, style = MaterialTheme.typography.bodyMedium)  
                        }  
                    }                    Spacer(modifier = Modifier.padding(10.dp))  
                }  
            }        }  
        if (showDialog && noteToDelete != null) {  
            AlertDialog(  
                onDismissRequest = {  
                    showDialog = false  
                    noteToDelete = null  
                },  
                title = { Text("Delete Note") },  
                text = { Text("Are you sure you want to delete '${noteToDelete?.title}'?") },  
                confirmButton = {  
                    TextButton(onClick = {  
                        noteToDelete?.let { viewModel.deleteData(it) }  
                        showDialog = false  
                        noteToDelete = null  
                    }) {  
                        Text("Yes")  
                    }  
                },  
                dismissButton = {  
                    TextButton(onClick = {  
                        showDialog = false  
                        noteToDelete = null  
                    }) {  
                        Text("No")  
                    }  
                }            
			)  
        }  
    }  
}

```