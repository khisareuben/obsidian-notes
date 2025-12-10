

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
  
  
    private val _uiState = MutableStateFlow(UiState())  
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()  
  
    init {  
        viewModelScope.launch {  
            getAllNotesUseCase.invoke().collect { notes ->  
                _uiState.update { it.copy(data = notes) }  
            }  
        }  
    }  
  
    fun insert(note: Note) = viewModelScope.launch {  
        insertUseCase.invoke(note)  
    }  
    fun update(note: Note) = viewModelScope.launch {  
        updateUseCase.invoke(note)  
    }  
    fun delete(note: Note) = viewModelScope.launch {  
        deleteUseCase.invoke(note)  
    }  
  
  
    fun toggleSelection(noteId: Int) {  
        _uiState.update { current ->  
            val newSelection = if (noteId in current.selectedNotes) {  
                current.selectedNotes - noteId  
            } else {  
                current.selectedNotes + noteId  
            }  
            current.copy(  
                selectedNotes = newSelection,  
                isSelectedMode = newSelection.isNotEmpty()  
            )  
        }  
    }  
  
    fun clearSelection() {  
        _uiState.update { it.copy(selectedNotes = emptySet(), isSelectedMode = false) }  
    }  
  
    fun deleteSelected() = viewModelScope.launch {  
        val selectedIds = _uiState.value.selectedNotes  
        _uiState.value.data.filter { it.id in selectedIds }.forEach { deleteUseCase.invoke(it) }  
        clearSelection()  
    }  
  
    fun selectAll() {  
        val allIds = _uiState.value.data.map { it.id }.toSet()  
        _uiState.update { it.copy(selectedNotes = allIds, isSelectedMode = allIds.isNotEmpty()) }  
    }  
  
  
}  
  
data class UiState(  
    val data: List<Note> = emptyList(),  
    val selectedNotes: Set<Int> = emptySet(),  
    val isSelectedMode: Boolean = false  
)

```


`presentation/MainScreen.kt`
```kotlin

@OptIn(ExperimentalMaterial3Api::class)  
@Composable  
fun MainScreen(  
    uiState: UiState,  
    onAddClick: () -> Unit,  
    onEditClick: (Int) -> Unit,  
    onDelete: (Note) -> Unit,  
    onToggleSelection: (Int) -> Unit,  
    onClearSelection: () -> Unit,  
    onDeleteSelected: () -> Unit,  
    onSelectAll: () -> Unit  
) {  
    val theme = LocalTheme.current  
  
    Scaffold(  
        topBar = {  
            if (uiState.isSelectedMode) {  
                TopAppBar(  
                    title = { Text("${uiState.selectedNotes.size} selected", color = theme.buttonColor) },  
                    actions = {  
                        IconButton(onClick = onSelectAll) {  
                            Icon(  
                                painter = painterResource(R.drawable.outline_select_all_24),  
                                contentDescription = "Select All"  
                            )  
                        }  
                        IconButton(onClick = onDeleteSelected) {  
                            Icon(  
                                painter = painterResource(R.drawable.baseline_delete_24),  
                                contentDescription = "Delete"  
                            )  
                        }  
                        IconButton(onClick = onClearSelection) {  
                            Icon(  
                                painter = painterResource(R.drawable.outline_close_24),  
                                contentDescription = "Cancel"  
                            )  
                        }  
                    },  
                    colors = TopAppBarDefaults.topAppBarColors(  
                        containerColor = theme.containerColor  
                    )  
                )  
            } else {  
                TopAppBarUI(title = "MainScreen")  
            }  
        },  
        floatingActionButton = {  
            if (!uiState.isSelectedMode) {  
                FloatingActionButton(  
                    onClick = onAddClick,  
                    containerColor = theme.buttonColor  
                ) {  
                    Image(  
                        painter = painterResource(R.drawable.baseline_add_24),  
                        contentDescription = null  
                    )  
                }  
            }  
        }  
    ) { paddingValues ->  
  
        if (uiState.data.isEmpty()) {  
            Box(  
                modifier = Modifier.fillMaxSize()  
                    .background(theme.containerColor)  
                    .padding(paddingValues),  
                contentAlignment = Alignment.Center  
            ) {  
                Column(  
                    horizontalAlignment = Alignment.CenterHorizontally  
                ) {  
                    Image(  
                        painter = painterResource(R.drawable.outline_note_stack_add_24), // optional illustration  
                        contentDescription = null,  
                        modifier = Modifier.size(120.dp),  
                        colorFilter = ColorFilter.tint(  
                            theme.buttonColor  
                        )  
                    )  
                    Spacer(modifier = Modifier.height(16.dp))  
                    Text(  
                        text = "No notes yet!",  
                        style = MaterialTheme.typography.titleMedium,  
                        fontWeight = FontWeight.Bold  
                    )  
                    Text(  
                        text = "Tap + to add your first note",  
                        style = MaterialTheme.typography.bodyMedium,  
                        color = Color.Gray  
                    )  
                }  
            }        }  
        else {  
            LazyVerticalStaggeredGrid(  
                columns = StaggeredGridCells.Fixed(2),  
                modifier = Modifier  
                    .background(theme.containerColor)  
                    .fillMaxSize()  
                    .padding(paddingValues),  
                verticalItemSpacing = 8.dp,  
                horizontalArrangement = Arrangement.spacedBy(4.dp)  
            ) {  
                items(uiState.data) { note ->  
                    val isSelected = note.id in uiState.selectedNotes  
                    Card(  
                        shape = RoundedCornerShape(  
                            topStart = 0.dp,  
                            topEnd = 16.dp,  
                            bottomEnd = 0.dp,  
                            bottomStart = 32.dp  
                        ),  
                        modifier = Modifier  
                            .padding(8.dp)  
                            .combinedClickable(  
                                onClick = {  
                                    if (uiState.isSelectedMode) {  
                                        onToggleSelection(note.id)  
                                    } else {  
                                        onEditClick(note.id)  
                                    }  
                                },  
                                onLongClick = { onToggleSelection(note.id) }  
                            ),  
                        colors = CardDefaults.cardColors(  
                            containerColor = if (isSelected) Color.LightGray else theme.cardBackground  
                        )  
                    ) {  
                        Row(  
                            modifier = Modifier.fillMaxWidth().padding(16.dp),  
                            horizontalArrangement = Arrangement.SpaceBetween,  
                            verticalAlignment = Alignment.CenterVertically  
                        ) {  
                            Column(modifier = Modifier.weight(1f)) {  
                                Text(  
                                    text = note.title,  
                                    fontWeight = FontWeight.Bold,  
                                    maxLines = 1,  
                                    overflow = TextOverflow.Ellipsis  
                                )  
                                Text(  
                                    text = note.content,  
                                    maxLines = 9,  
                                    overflow = TextOverflow.Ellipsis  
                                )  
                            }  
  
                            if (uiState.isSelectedMode) {  
                                Checkbox(  
                                    checked = isSelected,  
                                    onCheckedChange = { onToggleSelection(note.id) }  
                                )  
                            }  
                        }  
                    }                }            }        }  
  
    }  
}

```


`presentation/AddNoteScreen`
```kotlin

@OptIn(ExperimentalMaterial3Api::class)  
@Composable  
fun AddNoteScreen(onSave: (Note) -> Unit) {  
  
    var title by remember { mutableStateOf("") }  
    var content by remember { mutableStateOf("") }  
    val theme = LocalTheme.current  
  
    Scaffold(  
        topBar = {  
            TopAppBar(  
                title = {  
                    Box(  
                        modifier = Modifier.fillMaxWidth(),  
                        contentAlignment = Alignment.Center  
                    ) {  
                        Text(  
                            text = "Add Note",  
                            fontWeight = FontWeight.Bold  
                        )  
                    }  
                },  
                actions = {  
                    IconButton(onClick = {  
                        if (title.isNotBlank() && content.isNotBlank()) {  
                            onSave(Note(id = 0, title = title, content = content))  
                        }  
                    }) {  
                        Image(  
                            painter = painterResource(R.drawable.outline_check_circle_24),  
                            contentDescription = null,  
                            colorFilter = ColorFilter.tint(  
                                theme.buttonColor  
                            )  
                        )  
                    }  
                },  
                colors = TopAppBarDefaults.topAppBarColors(  
                    containerColor = theme.containerColor  
                )  
            )  
        }  
    ) { paddingValues ->  
  
        Column(  
            Modifier.background(theme.containerColor).padding(paddingValues),  
            horizontalAlignment = Alignment.CenterHorizontally  
        ) {  
            OutlinedTextField(  
                modifier = Modifier.fillMaxWidth().padding(horizontal = 10.dp),  
                value = title,  
                onValueChange = { title = it },  
                label = { Text("Title") },  
                maxLines = 1,  
                colors = TextFieldDefaults.colors(  
                    cursorColor = theme.buttonColor,  
                    focusedContainerColor = theme.containerColor,  
                    unfocusedContainerColor = theme.containerColor,  
                    focusedIndicatorColor = theme.buttonColor  
  
                )  
            )  
  
            Box(modifier = Modifier  
                .fillMaxWidth()  
                .padding(10.dp)  
                .height(55.dp)  
                .border(  
                    width = 1.dp,  
                    color = Color.Gray,  
                    shape = RoundedCornerShape(4.dp)  
                ),  
                contentAlignment = Alignment.Center  
            ) {  
                Text(text = "${content.length} characters")  
            }  
  
            OutlinedTextField(  
                modifier = Modifier.fillMaxHeight().fillMaxWidth()  
                    .padding(start = 10.dp, end = 10.dp, bottom = 10.dp),  
                value = content,  
                onValueChange = { content = it },  
                placeholder = {Text("Start typing", color = Color.Gray)},  
                label = { Text("Content") },  
                colors = TextFieldDefaults.colors(  
                    cursorColor = theme.buttonColor,  
                    focusedContainerColor = theme.containerColor,  
                    unfocusedContainerColor = theme.containerColor,  
                    focusedIndicatorColor = theme.buttonColor  
  
                )  
  
            )  
  
    }  
  
  
    }  
}

```

`presentation/EditNoteScreen`
```kotlin

@OptIn(ExperimentalMaterial3Api::class)  
@Composable  
fun EditNoteScreen(note: Note, onUpdate: (Note) -> Unit) {  
    var title by remember { mutableStateOf(note.title) }  
    var content by remember { mutableStateOf(note.content) }  
    val theme = LocalTheme.current  
  
    Scaffold(  
        topBar = {  
            TopAppBar(  
                title = {  
                    Box(  
                        modifier = Modifier.fillMaxWidth(),  
                        contentAlignment = Alignment.Center  
                    ) {  
                        Text(  
                            text = "Edit",  
                            fontWeight = FontWeight.Bold  
                        )  
                    }  
                },  
                actions = {  
                    IconButton(onClick = {  
                        if (title.isNotBlank() && content.isNotBlank()) {  
                            onUpdate(note.copy(title = title, content = content))  
                        }  
                    }) {  
                        Image(  
                            painter = painterResource(R.drawable.outline_check_circle_24),  
                            contentDescription = null,  
                            colorFilter = ColorFilter.tint(  
                                theme.buttonColor  
                            )  
                        )  
                    }  
                },  
                colors = TopAppBarDefaults.topAppBarColors(  
                    containerColor = theme.containerColor  
                )  
            )  
        }  
    ) {  paddingValues ->  
  
        Column(Modifier.fillMaxSize()  
            .background(theme.containerColor)  
            .padding(paddingValues),  
            horizontalAlignment = Alignment.CenterHorizontally  
        ) {  
            OutlinedTextField(  
                modifier = Modifier.fillMaxWidth().padding(horizontal = 10.dp),  
                value = title,  
                onValueChange = { title = it },  
                label = { Text("Title") },  
                maxLines = 1,  
                colors = TextFieldDefaults.colors(  
                    focusedIndicatorColor = theme.buttonColor,  
                    cursorColor = theme.buttonColor,  
                    focusedContainerColor = theme.containerColor,  
                    unfocusedContainerColor = theme.containerColor  
                )  
            )  
            Box(modifier = Modifier  
                .fillMaxWidth()  
                .padding(10.dp)  
                .height(55.dp)  
                .border(  
                    width = 1.dp,  
                    color = Color.Gray,  
                    shape = RoundedCornerShape(4.dp)  
                ),  
                contentAlignment = Alignment.Center  
            ) {  
                Text(text = "${content.length} characters")  
            }  
            OutlinedTextField(  
                modifier = Modifier.fillMaxHeight().fillMaxWidth()  
                    .padding(start = 10.dp, end = 10.dp, bottom = 10.dp),  
                value = content,  
                onValueChange = { content = it },  
                placeholder = {Text("Start typing", color = Color.Gray)},  
                label = { Text("Content") },  
                colors = TextFieldDefaults.colors(  
                    focusedIndicatorColor = theme.buttonColor,  
                    cursorColor = theme.buttonColor,  
                    focusedContainerColor = theme.containerColor,  
                    unfocusedContainerColor = theme.containerColor  
                )  
            )  
  
        }  
  
    }  
  
}


```


`presentation/Navigation.kt`
```kotlin

@Composable  
fun NotesApp(viewModel: MainViewModel = hiltViewModel()) {  
  
    val navController = rememberNavController()  
  
    NavHost(  
        navController = navController,  
        startDestination = Dest.MainScreen,  
        enterTransition = { slideInHorizontally { it } },  
        exitTransition = { slideOutHorizontally { -it } },  
        popEnterTransition = { slideInHorizontally { -it } },  
        popExitTransition = { slideOutHorizontally { it } }  
    ) {  
        composable<Dest.MainScreen> {  
            MainScreen(  
                uiState = viewModel.uiState.collectAsState().value,  
                onAddClick = { navController.navigate(Dest.AddNoteScreen) },  
                onEditClick = { noteId -> navController.navigate(Dest.EditNoteScreen(noteId)) },  
                onDelete = viewModel::delete,  
                onToggleSelection = viewModel::toggleSelection,  
                onClearSelection = viewModel::clearSelection,  
                onDeleteSelected = viewModel::deleteSelected,  
                onSelectAll = viewModel::selectAll  
            )  
        }  
        composable<Dest.AddNoteScreen> {  
            AddNoteScreen(  
                onSave = {  
                    viewModel.insert(it)  
                    navController.popBackStack()  
                }  
            )  
        }  
        composable<Dest.EditNoteScreen> {  
            val nodeId = it.toRoute<Dest.EditNoteScreen>().id  
            val note = viewModel.uiState.collectAsState().value.data.find { it.id == nodeId }  
            note?.let { it ->  
                EditNoteScreen(  
                    note = it,  
                    onUpdate = {  
                        viewModel.update(it)  
                        navController.popBackStack()  
                    }  
                )  
            }  
  
        }    }  
}  
  
  
sealed class Dest {  
    @Serializable  
    data object MainScreen: Dest()  
  
    @Serializable  
    data object AddNoteScreen: Dest()  
  
    @Serializable  
    data class EditNoteScreen(val id: Int): Dest()  
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
            TodoNotesTheme {  
                val theme = if (isSystemInDarkTheme()) darkThemeColors else lightThemeColor  
                CompositionLocalProvider(LocalTheme provides theme) {  
                    NotesApp()  
                }  
  
            }        
		}    
	}  
}

```

# Custom color theme

```kotlin

data class CustomTheme(  
    val containerColor: Color,  
    val buttonColor: Color,  
    val background: Color,  
    val cardBackground: Color,  
    val titleColor: Color,  
    val bodyColor: Color,  
    val logoColor: Color  
)  
  
  
val darkThemeColors = CustomTheme(  
    containerColor = Color(0xFF0A0A0A),  
    buttonColor = Color(0xFFFFAB00),  
    background = Color(0xFF0A0A0A),  
    cardBackground = Color.DarkGray,  
    titleColor = Color(0xFFFFFFFF),  
    bodyColor = Color.LightGray,  
    logoColor = Color(0xFFFFAB00)  
)  
  
val lightThemeColor = CustomTheme(  
    containerColor = Color(0xFFF1F1F1),  
    buttonColor = Color(0xFFFFAB00),  
    background = Color.White,  
    cardBackground = Color(0xFFFFFFFF),  
    titleColor = Color(0xFF0A0A0A),  
    bodyColor = Color.Gray,  
    logoColor = Color(0xFFFFAB00)  
)  
  
val LocalTheme = staticCompositionLocalOf<CustomTheme> {  
    error("No theme provided")  
}

```