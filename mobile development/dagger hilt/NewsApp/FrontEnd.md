`presentation/article_screen/ArticleScreen.kt`

```kotlin

@OptIn(ExperimentalMaterial3Api::class)  
@Composable  
fun ArticleScreen(  
    url: String?,  
    onBackPressed: () -> Unit  
) {  
    val context = LocalContext.current  
    var isLoading by remember { mutableStateOf(true) }  
  
    Scaffold(  
        modifier = Modifier.fillMaxSize(),  
        topBar = {  
            TopAppBar(  
                title = { Text(text = "Article", fontWeight = FontWeight.Bold) },  
                navigationIcon = {  
                    IconButton(onClick = onBackPressed) {  
                        Icon(imageVector = Icons.Default.ArrowBack, contentDescription = "Back")  
                    }  
                },  
                colors = TopAppBarDefaults.topAppBarColors(  
                    containerColor = MaterialTheme.colorScheme.primaryContainer,  
                    navigationIconContentColor = MaterialTheme.colorScheme.onPrimaryContainer,  
                    titleContentColor = MaterialTheme.colorScheme.onPrimaryContainer  
                )  
            )  
        }  
    ) { padding ->  
        Box(  
            modifier = Modifier  
                .fillMaxSize()  
                .padding(padding),  
            contentAlignment = Alignment.Center  
        ) {  
            AndroidView(factory = {  
                WebView(context).apply {  
                    webViewClient = object  : WebViewClient() {  
                        override fun onPageFinished(view: WebView?, url: String?) {  
                            isLoading = false  
                        }  
                    }  
                    loadUrl(url ?: "")  
                }  
            })  
            if (isLoading && url != null) {  
                CircularProgressIndicator()  
            }  
        }  
    }}

```

## Adding the component
These are files that will be used by other files

`presentation/component/BottomSheetContent.kt`

```kotlin

@Composable  
fun BottomSheetContent(  
    article: Article,  
    onReadFullStoryButtonClicked: () -> Unit  
) {  
    Surface(  
        modifier = Modifier.padding(16.dp)  
    ) {  
        Column(horizontalAlignment = Alignment.CenterHorizontally) {  
            Text(  
                text = article.title,  
                style = MaterialTheme.typography.titleMedium  
            )  
            Spacer(modifier = Modifier.height(8.dp))  
            Text(  
                text = article.description ?: "",  
                style = MaterialTheme.typography.bodyMedium  
            )  
            Spacer(modifier = Modifier.height(8.dp))  
            ImageHolder(imageUrl = article.urlToImage)  
            Spacer(modifier = Modifier.height(8.dp))  
            Text(  
                text = article.content ?: "",  
                style = MaterialTheme.typography.bodyMedium  
            )  
            Spacer(modifier = Modifier.height(8.dp))  
            Row(  
                modifier = Modifier.fillMaxWidth(),  
                horizontalArrangement = Arrangement.SpaceBetween  
            ) {  
                Text(  
                    text = article.author ?: "",  
                    style = MaterialTheme.typography.bodySmall,  
                    fontWeight = FontWeight.Bold  
                )  
                Text(  
                    text = article.source.name ?: "",  
                    style = MaterialTheme.typography.bodySmall,  
                    fontWeight = FontWeight.Bold  
                )  
            }  
            Spacer(modifier = Modifier.height(8.dp))  
            Button(  
                modifier = Modifier.fillMaxWidth(),  
                onClick = onReadFullStoryButtonClicked  
            ) {  
                Text(text = "Read Full Story")  
            }  
        }    }}

```

```kotlin

@OptIn(ExperimentalFoundationApi::class)  
@Composable  
fun CategoryTabRow(  
    pagerState: PagerState,  
    categories: List<String>,  
    onTabSelected: (Int) -> Unit  
) {  
    ScrollableTabRow(  
        selectedTabIndex = pagerState.currentPage,  
        edgePadding = 0.dp,  
        containerColor = MaterialTheme.colorScheme.primaryContainer,  
        contentColor = MaterialTheme.colorScheme.onPrimaryContainer,  
    ) {  
        categories.forEachIndexed { index, category ->  
            Tab(  
                selected = pagerState.currentPage == index,  
                onClick = { onTabSelected(index) },  
                content = {  
                    Text(  
                        text = category,  
                        modifier = Modifier.padding(vertical = 8.dp, horizontal = 2.dp)  
                    )  
                }  
            )  
        }  
    }}

```


```kotlin

@Composable  
fun ImageHolder(  
    imageUrl: String?,  
    modifier: Modifier = Modifier  
) {  
    AsyncImage(  
        model = ImageRequest  
            .Builder(LocalContext.current)  
            .data(imageUrl)  
            .crossfade(true)  
            .build(),  
        contentDescription = "Image",  
        contentScale = ContentScale.Crop,  
        modifier = modifier  
            .clip(RoundedCornerShape(4.dp))  
            .fillMaxWidth()  
            .aspectRatio(16 / 9f),  
        placeholder = painterResource(R.drawable.placeholder_loading),  
        error = painterResource(R.drawable.placeholder_news)  
    )  
}

```

```kotlin

@Composable  
fun NewsArticleCard(  
    modifier: Modifier = Modifier,  
    article: Article,  
    onCardClicked: (Article) -> Unit  
) {  
    val date = dateFormatter(article.publishedAt)  
    Card(  
        modifier = modifier.clickable { onCardClicked(article) }  
    ) {  
        Column(modifier = Modifier.padding(12.dp)) {  
            ImageHolder(imageUrl = article.urlToImage)  
            Spacer(modifier = Modifier.height(8.dp))  
            Text(  
                text = article.title,  
                style = MaterialTheme.typography.titleMedium,  
                maxLines = 1,  
                overflow = TextOverflow.Ellipsis  
            )  
            Spacer(modifier = Modifier.height(8.dp))  
            Row(  
                modifier = Modifier.fillMaxWidth(),  
                horizontalArrangement = Arrangement.SpaceBetween  
            ) {  
                Text(  
                    text = article.source.name ?: "",  
                    style = MaterialTheme.typography.bodySmall  
                )  
                Text(  
                    text = date,  
                    style = MaterialTheme.typography.bodySmall  
                )  
            }  
        }    }}

```


```kotlin

@OptIn(ExperimentalMaterial3Api::class)  
@Composable  
fun NewsScreenTopBar(  
    scrollBehavior: TopAppBarScrollBehavior,  
    onSearchIconClicked: () -> Unit  
) {  
    TopAppBar(  
        scrollBehavior = scrollBehavior,  
        title = { Text(text = "Newsroom", fontWeight = FontWeight.Bold)},  
        actions = {  
            IconButton(onClick = onSearchIconClicked) {  
                Icon(imageVector = Icons.Default.Search, contentDescription = "Search")  
            }  
        },  
        colors = TopAppBarDefaults.topAppBarColors(  
            containerColor = MaterialTheme.colorScheme.primaryContainer,  
            titleContentColor = MaterialTheme.colorScheme.onPrimaryContainer,  
            actionIconContentColor = MaterialTheme.colorScheme.onPrimaryContainer  
        )  
    )  
}

```


```kotlin

@Composable  
fun RetryContent(  
    error: String,  
    onRetry: () -> Unit,  
    modifier: Modifier = Modifier  
) {  
    Column(  
        modifier = modifier  
    ) {  
        Text(text = error, color = Color.Red, fontSize = 18.sp)  
        Spacer(modifier = Modifier.height(8.dp))  
        Button(  
            onClick = onRetry,  
            modifier = Modifier.align(CenterHorizontally)  
        ) {  
            Text(text = "Retry")  
        }  
    }}

```

```kotlin

@Composable  
fun SearchAppBar(  
    modifier: Modifier = Modifier,  
    value: String,  
    onValueChange: (String) -> Unit,  
    onCloseIconClicked: () -> Unit,  
    onSearchClicked: () -> Unit,  
) {  
    TextField(  
        modifier = modifier.fillMaxWidth(),  
        value = value,  
        onValueChange = onValueChange,  
        textStyle = TextStyle(color = Color.White, fontSize = 16.sp),  
        leadingIcon = {  
            Icon(  
                imageVector = Icons.Filled.Search,  
                contentDescription = "Search Icon",  
                tint = Color.White.copy(alpha = 0.7f)  
            )  
        },  
        placeholder = {  
            Text(text = "Search...", color = Color.White.copy(alpha = 0.7f))  
        },  
        trailingIcon = {  
            IconButton(onClick = {  
                if (value.isNotEmpty()) onValueChange("")  
                else onCloseIconClicked()  
            }) {  
                Icon(  
                    imageVector = Icons.Filled.Close,  
                    contentDescription = "Close",  
                    tint = Color.White  
                )  
            }  
        },  
        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),  
        keyboardActions = KeyboardActions(onSearch = { onSearchClicked() }),  
        colors = TextFieldDefaults.colors(  
            focusedContainerColor = MaterialTheme.colorScheme.primaryContainer,  
            unfocusedContainerColor = MaterialTheme.colorScheme.primaryContainer,  
            cursorColor = Color.White,  
            focusedIndicatorColor = Color.White  
        )  
    )  
}

```

## Adding the news_screen

`presentation/NewsScreen.kt, NewsScreenEvent.kt, NewsScreenState.kt, NewsScreenViewModel.kt`

```kotlin

@OptIn(  
    ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class,  
    ExperimentalComposeUiApi::class  
)  
@Composable  
fun NewsScreen(  
    state: NewsScreenState,  
    onEvent: (NewsScreenEvent) -> Unit,  
    onReadFullStoryButtonClick: (String) -> Unit  
) {  
    val scrollBehavior = TopAppBarDefaults.enterAlwaysScrollBehavior()  
    val pagerState = rememberPagerState()  
    val coroutineScope = rememberCoroutineScope()  
  
    val categories = listOf(  
        "General", "Business", "Health", "Science", "Sports", "Technology", "Entertainment"  
    )  
  
    val focusRequester = remember { FocusRequester() }  
    val focusManager = LocalFocusManager.current  
    val keyboardController = LocalSoftwareKeyboardController.current  
  
    LaunchedEffect(key1 = pagerState) {  
        snapshotFlow { pagerState.currentPage }.collect { page ->  
            onEvent(NewsScreenEvent.OnCategoryChanged(category = categories[page]))  
        }  
    }  
    LaunchedEffect(key1 = Unit) {  
        if (state.searchQuery.isNotEmpty()) {  
            onEvent(NewsScreenEvent.OnSearchQueryChanged(searchQuery = state.searchQuery))  
        }  
    }  
  
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)  
    var shouldBottomSheetShow by remember { mutableStateOf(false) }  
  
    if (shouldBottomSheetShow) {  
        ModalBottomSheet(  
            onDismissRequest = { shouldBottomSheetShow = false },  
            sheetState = sheetState,  
            content = {  
                state.selectedArticle?.let {  
                    BottomSheetContent(  
                        article = it,  
                        onReadFullStoryButtonClicked = {  
                            onReadFullStoryButtonClick(it.url)  
                            coroutineScope.launch { sheetState.hide() }.invokeOnCompletion {  
                                if (!sheetState.isVisible) shouldBottomSheetShow = false  
                            }  
                        }                    )  
                }  
            }        )  
    }  
  
    Column(  
        modifier = Modifier.fillMaxSize()  
    ) {  
        Crossfade(targetState = state.isSearchBarVisible) { isVisible ->  
            if (isVisible) {  
                Column {  
                    SearchAppBar(  
                        modifier = Modifier.focusRequester(focusRequester),  
                        value = state.searchQuery,  
                        onValueChange = { newValue ->  
                            onEvent(NewsScreenEvent.OnSearchQueryChanged(newValue))  
                        },  
                        onCloseIconClicked = { onEvent(NewsScreenEvent.OnCloseIconClicked) },  
                        onSearchClicked = {  
                            keyboardController?.hide()  
                            focusManager.clearFocus()  
                        }  
                    )  
                    NewsArticleList(  
                        state = state,  
                        onCardClicked = { article ->  
                            shouldBottomSheetShow = true  
                            onEvent(NewsScreenEvent.OnNewsCardClicked(article = article))  
                        },  
                        onRetry = {  
                            onEvent(NewsScreenEvent.OnSearchQueryChanged(state.searchQuery))  
                        }  
                    )  
                }  
            } else {  
                Scaffold(  
                    modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection),  
                    topBar = {  
                        NewsScreenTopBar(  
                            scrollBehavior = scrollBehavior,  
                            onSearchIconClicked = {  
                                onEvent(NewsScreenEvent.OnSearchIconClicked)  
                                coroutineScope.launch {  
                                    delay(500)  
                                    focusRequester.requestFocus()  
                                }  
                            }                        )  
                    }  
                ) { padding ->  
                    Column(  
                        modifier = Modifier  
                            .fillMaxSize()  
                            .padding(padding)  
                    ) {  
                        CategoryTabRow(  
                            pagerState = pagerState,  
                            categories = categories,  
                            onTabSelected = { index ->  
                                coroutineScope.launch { pagerState.animateScrollToPage(index) }  
                            }                        )  
                        HorizontalPager(  
                            pageCount = categories.size,  
                            state = pagerState  
                        ) {  
                            NewsArticleList(  
                                state = state,  
                                onCardClicked = { article ->  
                                    shouldBottomSheetShow = true  
                                    onEvent(NewsScreenEvent.OnNewsCardClicked(article = article))  
                                },  
                                onRetry = {  
                                    onEvent(NewsScreenEvent.OnCategoryChanged(state.category))  
                                }  
                            )  
                        }  
                    }                }            }  
        }  
    }  
  
}  
  
@Composable  
fun NewsArticleList(  
    state: NewsScreenState,  
    onCardClicked: (Article) -> Unit,  
    onRetry: () -> Unit,  
) {  
    LazyColumn(  
        contentPadding = PaddingValues(16.dp),  
        verticalArrangement = Arrangement.spacedBy(16.dp)  
    ) {  
        items(state.articles) { article ->  
            NewsArticleCard(  
                article = article,  
                onCardClicked = onCardClicked  
            )  
        }  
    }    Box(  
        modifier = Modifier.fillMaxSize(),  
        contentAlignment = Alignment.Center  
    ) {  
        if (state.isLoading) {  
            CircularProgressIndicator()  
        }  
        if (state.error != null) {  
            RetryContent(  
                error = state.error,  
                onRetry = onRetry  
            )  
        }  
    }  
}

```


```kotlin

sealed class NewsScreenEvent {  
    data class OnNewsCardClicked(var article: Article) : NewsScreenEvent()  
    data class OnCategoryChanged(var category: String) : NewsScreenEvent()  
    data class OnSearchQueryChanged(var searchQuery: String) : NewsScreenEvent()  
    object OnSearchIconClicked: NewsScreenEvent()  
    object OnCloseIconClicked: NewsScreenEvent()  
}

```

```kotlin

data class NewsScreenState(  
    val isLoading: Boolean = false,  
    val articles: List<Article> = emptyList(),  
    val error: String? = null,  
    val isSearchBarVisible: Boolean= false,  
    val selectedArticle: Article? = null,  
    val category: String = "General",  
    val searchQuery: String = ""  
)

```

```kotlin

@HiltViewModel  
class NewsScreenViewModel @Inject constructor(  
    private val newsRepository: NewsRepository  
) : ViewModel() {  
  
    var state by mutableStateOf(NewsScreenState())  
  
    private var searchJob: Job? = null  
  
    fun onEvent(event: NewsScreenEvent) {  
        when (event) {  
            is NewsScreenEvent.OnCategoryChanged -> {  
                state = state.copy(category = event.category)  
                getNewsArticles(category = state.category)  
            }  
  
            is NewsScreenEvent.OnNewsCardClicked -> {  
                state = state.copy(selectedArticle = event.article)  
            }  
  
            NewsScreenEvent.OnSearchIconClicked -> {  
                state = state.copy(  
                    isSearchBarVisible = true,  
                    articles = emptyList()  
                )  
            }  
  
            NewsScreenEvent.OnCloseIconClicked -> {  
                state = state.copy(isSearchBarVisible = false)  
                getNewsArticles(category = state.category)  
            }  
  
            is NewsScreenEvent.OnSearchQueryChanged -> {  
                state = state.copy(searchQuery = event.searchQuery)  
                searchJob?.cancel()  
                searchJob = viewModelScope.launch {  
                    delay(1000L)  
                    searchForNews(query = state.searchQuery)  
                }  
            }  
        }  
    }  
  
    private fun getNewsArticles(category: String) {  
        viewModelScope.launch {  
            state = state.copy(isLoading = true)  
            val result = newsRepository.getTopHeadlines(category = category)  
            when (result) {  
                is Resource.Success -> {  
                    state = state.copy(  
                        articles = result.data ?: emptyList(),  
                        isLoading = false,  
                        error = null  
                    )  
                }  
  
                is Resource.Error -> {  
                    state = state.copy(  
                        articles = emptyList(),  
                        isLoading = false,  
                        error = result.message  
                    )  
                }  
            }  
        }  
    }  
  
    private fun searchForNews(query: String) {  
        if (query.isEmpty()) {  
            return  
        }  
        viewModelScope.launch {  
            state = state.copy(isLoading = true)  
            val result = newsRepository.searchForNews(query = query)  
            when (result) {  
                is Resource.Success -> {  
                    state = state.copy(  
                        articles = result.data ?: emptyList(),  
                        isLoading = false,  
                        error = null  
                    )  
                }  
  
                is Resource.Error -> {  
                    state = state.copy(  
                        articles = emptyList(),  
                        isLoading = false,  
                        error = result.message  
                    )  
                }  
            }  
        }  
    }  
}

```


## Finalizing with the MainActivity

```kotlin

@AndroidEntryPoint  
class MainActivity : ComponentActivity() {  
    override fun onCreate(savedInstanceState: Bundle?) {  
        super.onCreate(savedInstanceState)  
        setContent {  
            NewsroomTheme {  
                val navController = rememberNavController()  
                NavGraphSetup(navController = navController)  
            }  
        }    }  
}

```

