
## Adding the viewModel

`presentation/MainViewModel.kt`
```kotlin

@HiltViewModel  
class MainViewModel @Inject constructor(  
    private val insertUseCase: InsertUseCase,  
    private val updateUseCase: UpdateUseCase,  
    private val deleteUseCase: DeleteUseCase,  
    private val getAllNotesUseCase: GetAllNotesUseCase  
) : ViewModel() {  
  
    val uiState = getAllNotesUseCase.invoke()  
    .map { UiState(it) }  
    .stateIn(viewModelScope, SharingStarted.Eagerly, UiState())
  
    fun insert(note: Note) = viewModelScope.launch {  
        insertUseCase.invoke(note)  
    }  
  
    fun update(note: Note) = viewModelScope.launch {  
        updateUseCase.invoke(note)  
    }  
  
    fun delete(note: Note) = viewModelScope.launch {  
        deleteUseCase.invoke(note)  
    }  
  
}  
  
data class UiState(  
    val data: List<Note> = emptyList()  
)

```


`presentation/MainScreen.kt`
```kotlin

@Composable  
fun MainScreen(  
    uiState: UiState,  
    onAddClick: () -> Unit,  
    onEditClick: (Int) -> Unit,  
    onDelete: (Note) -> Unit  
) {  
    Scaffold(  
        floatingActionButton = {  
            FloatingActionButton(onClick = onAddClick) {  
                //Icon(imageVector = Icons, contentDescription = null)  
            }  
        }    ) { paddingValues ->  
        LazyColumn {  
            items(uiState.data) { note ->  
                Card(  
                    modifier = Modifier  
                        .fillMaxWidth()  
                        .padding(paddingValues)  
                        .padding(8.dp)  
                        .clickable { onEditClick(note.id) }  
                ) {  
                    Row(  
                        Modifier  
                            .fillMaxWidth()  
                            .padding(16.dp),  
                        horizontalArrangement = Arrangement.SpaceBetween  
                    ) {  
                        Column {  
                            Text(note.title, fontWeight = FontWeight.Bold)  
                            Text(note.desc)  
                        }  
                        IconButton(onClick = { onDelete(note) }) {  
                            //Icon(imageVector = Icons.Default.Delete, contentDescription = "Delete")  
                        }  
                    }                
				}           
			}        
		}    
	}
}

```


`presentation/AddNoteScreen`
```kotlin

@Composable  
fun AddNoteScreen(onSave: (Note) -> Unit) {  
    var title by remember { mutableStateOf("") }  
    var desc by remember { mutableStateOf("") }  
  
    Column(Modifier.padding(16.dp)) {  
        OutlinedTextField(value = title, onValueChange = { title = it }, label = { Text("Title") })  
        Spacer(Modifier.height(8.dp))  
        OutlinedTextField(value = desc, onValueChange = { desc = it }, label = { Text("Content") })  
        Spacer(Modifier.height(16.dp))  
        Button(onClick = {  
            if (title.isNotBlank() && desc.isNotBlank()) {  
                onSave(Note(id = 0, title = title, desc = desc)) // id = 0 for new  
            }  
        }) {  
            Text("Save")  
        }  
    }
}

```

`presentation/EditNoteScreen`
```kotlin

@Composable  
fun EditNoteScreen(note: Note, onUpdate: (Note) -> Unit) {  
    var title by remember { mutableStateOf(note.title) }  
    var desc by remember { mutableStateOf(note.desc) }  
  
    Column(Modifier.padding(16.dp)) {  
        OutlinedTextField(value = title, onValueChange = { title = it }, label = { Text("Title") })  
        Spacer(Modifier.height(8.dp))  
        OutlinedTextField(value = desc, onValueChange = { desc = it }, label = { Text("Content") })  
        Spacer(Modifier.height(16.dp))  
        Button(onClick = {  
            if (title.isNotBlank() && desc.isNotBlank()) {  
                onUpdate(note.copy(title = title, desc = desc))  
            }  
        }) {  
            Text("Update")  
        }  
    }
}


```


`presentation/Navigation.kt`
```kotlin

@Composable  
fun NotesApp(viewModel: MainViewModel = hiltViewModel()) {  
    val navController = rememberNavController()  
  
    NavHost(navController, startDestination = "main") {  
        composable("main") {  
            MainScreen(  
                uiState = viewModel.uiState.collectAsState().value,  
                onAddClick = { navController.navigate("add") },  
                onEditClick = { noteId -> navController.navigate("edit/$noteId") },  
                onDelete = viewModel::delete  
            )  
        }  
        composable("add") {  
            AddNoteScreen(onSave = {  
                viewModel.insert(it)  
                navController.popBackStack()  
            })  
        }  
        composable("edit/{noteId}") { backStackEntry ->  
            val noteId = backStackEntry.arguments?.getString("noteId")?.toIntOrNull()  
            val note = viewModel.uiState.collectAsState().value.data.find { it.id == noteId }  
            note?.let { it -> //i added this to remove some error 
                EditNoteScreen(note = it, onUpdate = {  
                    viewModel.update(it)  
                    navController.popBackStack()  
                })  
            }  
        }    
	}
}

```


`MainActivity.kt`
```kotlin

@AndroidEntryPoint  
class MainActivity : ComponentActivity() {  
    override fun onCreate(savedInstanceState: Bundle?) {  
        super.onCreate(savedInstanceState)  
        enableEdgeToEdge()  
        setContent {  
            NotesAppTheme {  
                NotesApp()  
            }  
        }    
	}  
}

```