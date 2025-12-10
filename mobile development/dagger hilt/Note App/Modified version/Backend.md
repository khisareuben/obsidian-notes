

- Create your project structure; data, domain, presentation, di


## 1. Adding the note Entity, Dao, and Database

`data/local/NoteEntity.kt`

```kotlin

const val notes_table = "notes"  
  
@Entity(notes_table)  
data class NoteEntity(  
    @PrimaryKey(autoGenerate = true)  
    @ColumnInfo("id") val id:Int = 0, //changing the column names  
    @ColumnInfo("title") val title: String,  
    @ColumnInfo("content") val content: String  
) {  
    constructor() : this(0, "", "")  
}

```

`data/local/NoteDao.kt`
```kotlin

@Dao  
interface NoteDao {  
  
    @Insert(onConflict = OnConflictStrategy.REPLACE)  
    suspend fun insert(noteEntity: NoteEntity): Long  
  
    @Update  
    suspend fun update(noteEntity: NoteEntity): Int  
  
    @Delete  
    suspend fun delete(noteEntity: NoteEntity): Int  
  
    @Query("SELECT * FROM notes")  
    fun getAllNotes(): Flow<List<NoteEntity>>  
  
}

```

`data/local/NoteDatabase.kt`
```kotlin

@Database(entities = [NoteEntity::class], version = 1)  
abstract class NoteDatabase : RoomDatabase() {  
  
    abstract fun getNoteDao(): NoteDao  
  
}

```


## Adding di(dagger hilt)

`di/NoteAppModule.kt`
```kotlin

@Module  
@InstallIn(SingletonComponent::class)  
object NoteAppModule {  
  
    @Provides  
    @Singleton    
    fun provideDatabase(@ApplicationContext context: Context): NoteDatabase {  
        return Room.databaseBuilder(  
            context,  
            NoteDatabase::class.java,  
            "Note.db"  
        ).build()  
    }  
  
    @Provides  
    fun provideNoteDao(noteDatabase: NoteDatabase): NoteDao {  
        return noteDatabase.getNoteDao()  
    }  
  
    @Provides  
    fun provideRepository(noteDao: NoteDao): NoteRepository {  
        return NoteRepoImpl(noteDao)  
    }  
  
}

```

`MyApp.kt`
```kotlin

@HiltAndroidApp  
class MyApp: Application()

```

Add it in the `AndroidManifest.xml` 


## Adding the domain model and repository

`domain/model/Note.kt`
```kotlin

data class Note(  
    val id: Int,  
    val title: String,  
    val content: String  
)

```

`domain/NoteRepository.kt`
```kotlin

interface NoteRepository {  
  
    suspend fun insert(note: Note)  
    suspend fun update(note: Note)  
    suspend fun delete(note: Note)  
    fun getAllNotes(): Flow<List<Note>>  
  
}

```

## Adding the repository implementation

`data/mappers/Mappers.kt`
```kotlin

fun Note.toNoteEntity(): NoteEntity {  
    return NoteEntity(id, title, content)  
}  
  
fun NoteEntity.toNote(): Note {  
    return Note(id, title, content)  
}

```


`data/repository/NoteRepoImpl.kt`
```kotlin

class NoteRepoImpl(private val noteDao: NoteDao): NoteRepository {  
  
    override suspend fun insert(note: Note) {  
        noteDao.insert(note.toNoteEntity())  
    }  
  
    override suspend fun update(note: Note) {  
        noteDao.update(note.toNoteEntity())  
    }  
  
    override suspend fun delete(note: Note) {  
        noteDao.delete(note.toNoteEntity())  
    }  
  
    override fun getAllNotes(): Flow<List<Note>> =  
        noteDao.getAllNotes().map { it.map { it.toNote() } }  
}

```


## Adding UseCases

`domain/useCases/AllUseCases.kt`
```kotlin

class InsertUseCase @Inject constructor(private val noteRepository: NoteRepository) {  
  
    suspend operator fun invoke(note: Note) = noteRepository.insert(note)  
  
}  
  
class DeleteUseCase @Inject constructor(private val noteRepository: NoteRepository) {  
  
    suspend operator fun invoke(note: Note) = noteRepository.delete(note)  
  
}  
  
class UpdateUseCase @Inject constructor(private val noteRepository: NoteRepository) {  
  
    suspend operator fun invoke(note: Note) = noteRepository. update(note)  
  
}  
  
class GetAllNotesUseCase @Inject constructor(private val noteRepository: NoteRepository) {  
  
    operator fun invoke() = noteRepository.getAllNotes()  
  
}

```


