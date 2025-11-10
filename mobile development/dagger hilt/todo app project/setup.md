
**Note to my future self**: I will not include the UI component for this because its in the git repository(todo)
this is just to learn the back end (dagger hilt)

## Step-by-Step: Room + ViewModel + Koin + Jetpack Compose

### ✅ 1. Add Koin Dependencies

In your `build.gradle` (app-level):

#### ✅ 1. **Create the columns of the database** : These are the different sections that will be in your database /data
#### `Note.kt`



```kotlin
@Entity(tableName = "todos")  
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
  
    @Query("select * from todos")  
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
  
    val getAllData: Flow<List<Todo>> = dao.getAllData()  
    suspend fun insertData(todo: Todo) = dao.insertData(todo)  
    suspend fun updateData(todo: Todo) = dao.updateData(todo)  
    suspend fun deleteData(todo: Todo) = dao.deleteData(todo)  
  
}

```

#### `NoteViewModel.kt`

#### 5. Create your viewModel /presentation

```kotlin

@HiltViewModel  
class TodoViewModel @Inject constructor(private val repository: TodoRepository): ViewModel() {  
    private val _notesList = MutableStateFlow<List<Todo>>(emptyList())  
    val notesList: StateFlow<List<Todo>> = _notesList  
  
    private val _isLoading = MutableStateFlow(true)  
    val isLoading: StateFlow<Boolean> = _isLoading  
  
  
    init {  
        viewModelScope.launch {  
            repository.getAllData.collect { todos ->  
                _notesList.value = todos.sortedByDescending { it.id }  
                _isLoading.value = false  
            }  
        }    }  
  
  
    fun insertData(todo: Todo){  
        viewModelScope.launch {  
            repository.insertData(todo)  
        }  
    }  
  
    fun updateData(todo: Todo) {  
        viewModelScope.launch {  
            repository.updateData(todo)  
        }  
    }  
  
    fun deleteData(todo: Todo){  
        viewModelScope.launch {  
            repository.deleteData(todo)  
        }  
    }  
  
}


```



## What Is a hilt Module?

A hilt module** is like a **recipe** that tells hilt how to create and provide the things your app needs—like your database, DAO, repository, and ViewModel.

You write this recipe once, and hilt uses it to "cook up" the objects whenever your app asks for them.

## 🧩 Let's Break Down the hilt Module Line by Line

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
object DatabaseModule {  
  
    @Provides  
    @Singleton    
    fun provideDatabase(@ApplicationContext context: Context): TodoDatabase {  
        return Room.databaseBuilder(  
            context,  
            TodoDatabase::class.java,  
            "todoDatabase.db"  
        ).build()  
    }  
  
    @Provides  
    fun provideDao(database: TodoDatabase): TodoDao {  
        return database.getDao()  
    }  
}  
  
@Module  
@InstallIn(SingletonComponent::class)  
object RepositoryModule {  
  
    @Provides  
    @Singleton    
    fun provideTodoRepository(dao: TodoDao): TodoRepository {  
        return TodoRepository(dao)  
    }  
}



```

