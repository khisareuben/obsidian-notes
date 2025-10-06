
## 2. File Structure


```
com.harold.notesapp/
├── data/
│   ├── local/
│   │   ├── entity/
│   │   │   └── NoteEntity.kt
│   │   ├── dao/
│   │   │   └── NoteDao.kt
│   │   └── NoteDatabase.kt
│   ├── mapper/
│   │   └── NoteMapper.kt
│   └── repository/
│       └── NoteRepositoryImpl.kt
│
├── domain/
│   ├── model/
│   │   └── Note.kt
│   ├── repository/
│   │   └── NoteRepository.kt
│   └── usecase/
│       ├── GetNotesUseCase.kt
│       ├── AddNoteUseCase.kt
│       ├── UpdateNoteUseCase.kt
│       └── DeleteNoteUseCase.kt
│
├── presentation/
│   ├── notes_list/
│   │   ├── NotesListScreen.kt
│   │   └── NotesListViewModel.kt
│   ├── add_note/
│   │   ├── AddNoteScreen.kt
│   │   └── AddNoteViewModel.kt
│   └── note_detail/
│       ├── NoteDetailScreen.kt
│       └── NoteDetailViewModel.kt
│
├── di/
│   └── AppModule.kt
│
├── MainActivity.kt
└── NotesApplication.kt
```

## 3. Data Layer

### 3.1 NoteEntity.kt



```kotlin
package com.harold.notesapp.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "notes")
data class NoteEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val title: String,
    val content: String
)
```

### 3.2 NoteDao.kt



```kotlin
package com.harold.notesapp.data.local.dao

import androidx.room.*
import com.harold.notesapp.data.local.entity.NoteEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface NoteDao {
    @Query("SELECT * FROM notes")
    fun getAllNotes(): Flow<List<NoteEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(note: NoteEntity)

    @Update
    suspend fun update(note: NoteEntity)

    @Delete
    suspend fun delete(note: NoteEntity)
}
```

### 3.3 NoteDatabase.kt



```kotlin
package com.harold.notesapp.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import com.harold.notesapp.data.local.dao.NoteDao
import com.harold.notesapp.data.local.entity.NoteEntity

@Database(entities = [NoteEntity::class], version = 1)
abstract class NoteDatabase : RoomDatabase() {
    abstract fun noteDao(): NoteDao
}
```

### 3.4 NoteMapper.kt



```kotlin
package com.harold.notesapp.data.mapper

import com.harold.notesapp.data.local.entity.NoteEntity
import com.harold.notesapp.domain.model.Note


/**
 * Converts from type F to T and back.
 */
interface Mapper<F, T> {
    fun map(input: F): T
    fun reverseMap(input: T): F
}


```


### Implement NoteMapper as a Bi-Directional Mapper



```kotlin

package com.harold.notesapp.data.mapper

import com.harold.notesapp.data.local.entity.NoteEntity
import com.harold.notesapp.domain.model.Note

object NoteMapper : Mapper<NoteEntity, Note> {

    override fun map(input: NoteEntity): Note {
        return Note(
            id      = input.id,
            title   = input.title,
            content = input.content
        )
    }

    override fun reverseMap(input: Note): NoteEntity {
        return NoteEntity(
            id      = input.id,
            title   = input.title,
            content = input.content
        )
    }
}


```

### 3.5 NoteRepositoryImpl.kt



```kotlin

package com.harold.notesapp.data.repository

import com.harold.notesapp.data.local.dao.NoteDao
import com.harold.notesapp.data.mapper.NoteMapper
import com.harold.notesapp.domain.model.Note
import com.harold.notesapp.domain.repository.NoteRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject

class NoteRepositoryImpl @Inject constructor(
    private val dao: NoteDao
) : NoteRepository {

    override fun getAllNotes(): Flow<List<Note>> =
        dao.getAllNotes()
           .map { entities ->
               entities.map { NoteMapper.map(it) }
           }

    override suspend fun addNote(note: Note) {
        dao.insert(NoteMapper.reverseMap(note))
    }

    override suspend fun updateNote(note: Note) {
        dao.update(NoteMapper.reverseMap(note))
    }

    override suspend fun deleteNote(note: Note) {
        dao.delete(NoteMapper.reverseMap(note))
    }
}


```

## 4. Domain Layer

### 4.1 Note.kt



```kotlin
package com.harold.notesapp.domain.model

data class Note(
    val id: Int = 0,
    val title: String,
    val content: String
)
```

### 4.2 NoteRepository.kt



```kotlin
package com.harold.notesapp.domain.repository

import com.harold.notesapp.domain.model.Note
import kotlinx.coroutines.flow.Flow

interface NoteRepository {
    fun getAllNotes(): Flow<List<Note>>
    suspend fun addNote(note: Note)
    suspend fun updateNote(note: Note)
    suspend fun deleteNote(note: Note)
}
```

### 4.3 UseCases



```kotlin
package com.harold.notesapp.domain.usecase

import com.harold.notesapp.domain.model.Note
import com.harold.notesapp.domain.repository.NoteRepository
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject

class GetNotesUseCase @Inject constructor(
    private val repo: NoteRepository
) {
    operator fun invoke(): Flow<List<Note>> = repo.getAllNotes()
}

class AddNoteUseCase @Inject constructor(
    private val repo: NoteRepository
) {
    suspend operator fun invoke(note: Note) = repo.addNote(note)
}

class UpdateNoteUseCase @Inject constructor(
    private val repo: NoteRepository
) {
    suspend operator fun invoke(note: Note) = repo.updateNote(note)
}

class DeleteNoteUseCase @Inject constructor(
    private val repo: NoteRepository
) {
    suspend operator fun invoke(note: Note) = repo.deleteNote(note)
}
```

## 5. DI Module



```kotlin
package com.harold.notesapp.di

import android.content.Context
import androidx.room.Room
import com.harold.notesapp.data.local.NoteDatabase
import com.harold.notesapp.data.repository.NoteRepositoryImpl
import com.harold.notesapp.domain.repository.NoteRepository
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideDatabase(appContext: Context): NoteDatabase {
        return Room.databaseBuilder(
            appContext,
            NoteDatabase::class.java,
            "notes_db"
        ).build()
    }

    @Provides
    fun provideNoteDao(db: NoteDatabase) = db.noteDao()

    @Provides
    @Singleton
    fun provideNoteRepository(dao: com.harold.notesapp.data.local.dao.NoteDao
    ): NoteRepository {
        return NoteRepositoryImpl(dao)
    }
}
```

## 6. Application Class



```kotlin
package com.harold.notesapp

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class NotesApplication : Application()
```

Add to **AndroidManifest.xml**:



```xml
<application
    android:name=".NotesApplication"
    ...>
    ...
</application>
```

## 7. Presentation Layer

### 7.1 Navigation Graph



```kotlin
package com.harold.notesapp.presentation

import androidx.compose.runtime.Composable
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavType
import androidx.navigation.compose.*
import com.harold.notesapp.presentation.add_note.AddNoteScreen
import com.harold.notesapp.presentation.add_note.AddNoteViewModel
import com.harold.notesapp.presentation.note_detail.NoteDetailScreen
import com.harold.notesapp.presentation.note_detail.NoteDetailViewModel
import com.harold.notesapp.presentation.notes_list.NotesListScreen
import com.harold.notesapp.presentation.notes_list.NotesListViewModel

@Composable
fun AppNavHost() {
    val navController = rememberNavController()
    NavHost(navController, startDestination = "notes_list") {

        composable("notes_list") {
            val vm: NotesListViewModel = hiltViewModel()
            NotesListScreen(
                viewModel = vm,
                onAddClick = { navController.navigate("add_note") },
                onNoteClick = { id ->
                    navController.navigate("note_detail/$id")
                }
            )
        }

        composable("add_note") {
            val vm: AddNoteViewModel = hiltViewModel()
            AddNoteScreen(
                viewModel = vm,
                onDone = { navController.popBackStack() }
            )
        }

        composable(
            "note_detail/{noteId}",
            arguments = listOf(navArgument("noteId") { type = NavType.IntType })
        ) { backStackEntry ->
            val noteId = backStackEntry.arguments?.getInt("noteId") ?: 0
            val vm: NoteDetailViewModel = hiltViewModel()
            NoteDetailScreen(
                viewModel = vm,
                noteId = noteId,
                onDone = { navController.popBackStack() }
            )
        }
    }
}
```

### 7.2 NotesListScreen & ViewModel



```kotlin
// NotesListViewModel.kt
package com.harold.notesapp.presentation.notes_list

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.harold.notesapp.domain.model.Note
import com.harold.notesapp.domain.usecase.GetNotesUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class NotesListViewModel @Inject constructor(
    private val getNotes: GetNotesUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow<List<Note>>(emptyList())  
	val uiState: StateFlow<List<Note>> = _uiState  
	    .onStart { loadNotes() }  // intead of using init {}
	    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())  
	  
	  
	private fun loadNotes() {  
	    viewModelScope.launch {  
	        getNotes().collect { list ->  
	            _uiState.value = list.sortedByDescending { it.id }  
	        }  
	    }  
	}
}

```



```kotlin
// NotesListScreen.kt
package com.harold.notesapp.presentation.notes_list

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.*
import androidx.compose.material.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.harold.notesapp.domain.model.Note

@Composable
fun NotesListScreen(
    viewModel: NotesListViewModel,
    onAddClick: () -> Unit,
    onNoteClick: (Int) -> Unit
) {
    val state = viewModel.uiState.collectAsState().value

    Scaffold(
        topBar = { TopAppBar(title = { Text("My Notes") }) },
        floatingActionButton = {
            FloatingActionButton(onClick = onAddClick) {
                Icon(Icons.Default.Add, contentDescription = "Add")
            }
        }
    ) { padding ->
        if (state.isLoading) {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
        } else {
            LazyColumn(
                contentPadding = padding,
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(state.notes) { note ->
                    NoteItem(note, onNoteClick) // just pass the arguments here instead of using navhost
                }
            }
        }
    }
}

@Composable
fun NoteItem(note: Note, onClick: (Int) -> Unit) {
    Card(
        Modifier
            .fillMaxWidth()
            .clickable { onClick(note.id) } 
            .padding(horizontal = 16.dp)
    ) {
        Column(Modifier.padding(16.dp)) {
            Text(note.title, style = MaterialTheme.typography.h6)
            Spacer(Modifier.height(4.dp))
            Text(note.content, style = MaterialTheme.typography.body2)
        }
    }
}
```

### 7.3 AddNoteScreen & ViewModel



```kotlin
// AddNoteViewModel.kt
package com.harold.notesapp.presentation.add_note

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.harold.notesapp.domain.model.Note
import com.harold.notesapp.domain.usecase.AddNoteUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class AddNoteViewModel @Inject constructor(
    private val addNote: AddNoteUseCase
) : ViewModel() {

    fun saveNote(title: String, content: String, onDone: () -> Unit) {
        viewModelScope.launch {
            addNote(Note(title = title, content = content))
            onDone()
        }
    }
}
```



```kotlin
// AddNoteScreen.kt
package com.harold.notesapp.presentation.add_note

import androidx.compose.foundation.layout.*
import androidx.compose.material.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun AddNoteScreen(
    viewModel: AddNoteViewModel,
    onDone: () -> Unit
) {
    var title by remember { mutableStateOf("") }
    var content by remember { mutableStateOf("") }

    Scaffold(
        topBar = { TopAppBar(title = { Text("Add Note") }) },
        floatingActionButton = {
            FloatingActionButton {
                viewModel.saveNote(title, content, onDone)
            }
        }
    ) { padding ->
        Column(
            Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp)
        ) {
            OutlinedTextField(
                value = title,
                onValueChange = { title = it },
                label = { Text("Title") },
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(Modifier.height(8.dp))
            OutlinedTextField(
                value = content,
                onValueChange = { content = it },
                label = { Text("Content") },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(200.dp)
            )
        }
    }
}
```

### 7.4 NoteDetailScreen & ViewModel



```kotlin
// NoteDetailViewModel.kt
package com.harold.notesapp.presentation.note_detail

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.harold.notesapp.domain.model.Note
import com.harold.notesapp.domain.usecase.DeleteNoteUseCase
import com.harold.notesapp.domain.usecase.GetNotesUseCase
import com.harold.notesapp.domain.usecase.UpdateNoteUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class NoteDetailViewModel @Inject constructor(
    private val getNotes: GetNotesUseCase,
    private val updateNote: UpdateNoteUseCase,
    private val deleteNote: DeleteNoteUseCase
) : ViewModel() {

    private val _note = MutableStateFlow<Note?>(null)
    val note: StateFlow<Note?> = _note.asStateFlow()

    fun loadNote(id: Int) {
        viewModelScope.launch {
            getNotes().collect { list ->
                _note.value = list.firstOrNull { it.id == id }
            }
        }
    }

    fun saveChanges(updated: Note, onDone: () -> Unit) {
        viewModelScope.launch {
            updateNote(updated)
            onDone()
        }
    }

    fun remove(onDone: () -> Unit) {
        viewModelScope.launch {
            _note.value?.let { deleteNote(it) }
            onDone()
        }
    }
}
```



```kotlin
// NoteDetailScreen.kt
package com.harold.notesapp.presentation.note_detail

import androidx.compose.foundation.layout.*
import androidx.compose.material.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun NoteDetailScreen(
    viewModel: NoteDetailViewModel,
    noteId: Int,
    onDone: () -> Unit
) {
    LaunchedEffect(noteId) {
        viewModel.loadNote(noteId)
    }

    val note by viewModel.note.collectAsState()
    var title by remember { mutableStateOf(note?.title.orEmpty()) }
    var content by remember { mutableStateOf(note?.content.orEmpty()) }

    Scaffold(
        topBar = { TopAppBar(title = { Text("Edit Note") }) },
        floatingActionButton = {
            Row {
                FloatingActionButton(onClick = { viewModel.remove(onDone) }) {
                    Icon(Icons.Default.Delete, contentDescription = "Delete")
                }
                Spacer(Modifier.width(16.dp))
                FloatingActionButton(onClick = {
                    viewModel.saveChanges(
                        note!!.copy(title = title, content = content),
                        onDone
                    )
                }) {
                    Icon(Icons.Default.Save, contentDescription = "Save")
                }
            }
        }
    ) { padding ->
        Column(
            Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp)
        ) {
            OutlinedTextField(
                value = title,
                onValueChange = { title = it },
                label = { Text("Title") },
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(Modifier.height(8.dp))
            OutlinedTextField(
                value = content,
                onValueChange = { content = it },
                label = { Text("Content") },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(200.dp)
            )
        }
    }
}
```

## 8. MainActivity.kt



```kotlin
package com.harold.notesapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.harold.notesapp.presentation.AppNavHost
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            AppNavHost()
        }
    }
}
```

## 9. How It All Works Together

- **AppModule** provides Room, DAO, Repository, and UseCases via Hilt.
    
- **UseCases** encapsulate each business operation (get, add, update, delete).
    
- **ViewModels** inject only the UseCases they need, keep UI state in `StateFlow`.
    
- **Compose Screens** collect state, call ViewModel functions for user actions.
    
- **Navigation** passes IDs between screens; each ViewModel loads data by ID.