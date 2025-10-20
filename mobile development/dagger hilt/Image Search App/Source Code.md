
1. Include all the dependencies for retrofit, dagger hilt, coil, and others
2. Get the responses from the API e.g pixabay.com which is in json format, copy them in the Json to kotlin extension.
   - Right click on remote -> new -> Kotlin data file class from Json -> Paste the json code -> name the file


# Configure the domain model

`domain/model/Image.kt`

```kotlin

import java.util.UUID  
  
data class Image(  
    val uuid:String = UUID.randomUUID().toString(),  
    val id: String,  
    val imageUrl: String  
)

```


`domain/repository/ImageRepository`

```kotlin

interface ImageRepository {  
  
    fun getImages(q: String): Pager<Int, Image>  
  
}

```

# Adding the dependencies

`data/di/AppModule.kt`

```kotlin

@InstallIn(SingletonComponent::class)  
@Module  
object DataModule {  
    // https://pixabay.com/api/?key=40308333-07c19e899666cb68334ed3a46&q=yellow+flowers&image_type=photo&pretty=true  
    @Provides  
    @Singleton    
    fun provideRetrofit(): Retrofit {  
        return Retrofit.Builder()  
            .baseUrl("https://pixabay.com/")  
            .addConverterFactory(GsonConverterFactory.create())  
            .build()  
    }  
  
    @Provides  
    fun provideApiService(retrofit: Retrofit): ApiService {  
        return retrofit.create(ApiService::class.java)  
    }  
  
    @Provides  
    fun provideRepoImpl(apiService: ApiService, mapper: ImageDTOToImageMapper): ImageRepository {  
        return ImageRepoImpl(apiService, mapper)  
    }  
  
}

```

```kotlin

@HiltAndroidApp  
class MyApp : Application()

```

- Include it in the manifest file and also add the internet permissions
# Adding the ApiService

`data/remote/ApiService.kt`

```kotlin

// https://pixabay.com/api/?key=40308333-07c19e899666cb68334ed3a46&q=yellow+flowers&page=1  
  
interface ApiService {  
  
    @GET("api/")  
    suspend fun getImages(  
        @Query("key") apiKey: String = "40308333-07c19e899666cb68334ed3a46",  
        @Query("q") q: String,  
        @Query("page") page: Int  
    ): ImageResponse  
  
}

```


# Adding the paging source

`data/pagingSource/ImagePagingSource.kt`

```kotlin

class ImagePagingSource(  
    private val apiService: ApiService,  
    private val q: String,  
    private val imageDtoToImageMapper:ImageDTOToImageMapper  
) : PagingSource<Int, Image>() {  

    override fun getRefreshKey(state: PagingState<Int, Image>): Int? {  
        return state.anchorPosition?.let {  
            state.closestPageToPosition(it)?.prevKey?.plus(1)  
                ?: state.closestPageToPosition(it)?.nextKey?.minus(1)  
        }  
    }  
  
    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, Image> {  
        return try {  
            val pageNumber = params.key ?: 1  
            val pageSize = params.loadSize  
  
            val images = apiService.getImages(q = q, page = pageNumber)  
            return LoadResult.Page(  
                data = imageDtoToImageMapper.mapAll(images.hits),  
                prevKey = if (pageNumber == 1) null else pageNumber.minus(1),  
                nextKey = if (images.hits.size < pageSize) null else pageNumber.plus(1)  
            )  
  
        } catch (e: Exception) {  
            LoadResult.Error(e)  
        }  
    }  
}

```

# Adding the mappers

`data/mappers/Mapper.kt`

```kotlin

interface Mapper<F, T> {  
    fun map(from: F): T  
}  
  
fun <F, T> Mapper<F, T>.mapAll(list: List<F>): List<T> = list.map { map(from = it) }

```

`data/mappers/ImageDTOToImageMapper.kt`

```kotlin

class ImageDTOToImageMapper @Inject constructor() : Mapper<ImageDTO, Image> {  
  
    override fun map(from: ImageDTO): Image {  
        return Image(  
            id = from.id.toString(),  
            imageUrl = from.largeImageURL  
        )  
    }  
}

```


# Adding the repository implementation

`data/repository/ImageRepoImpl.kt` 

```kotlin

class ImageRepoImpl(  
    private val apiService: ApiService,  
    private val mapper: ImageDTOToImageMapper  
) : ImageRepository {  
    override  fun getImages(q: String): Pager<Int, Image> {  
        return Pager(  
            config = PagingConfig(  
                pageSize = 10,  
                prefetchDistance = 1,  
                enablePlaceholders = false,  
                initialLoadSize = 10,  
            ),  
            pagingSourceFactory = {  
                ImagePagingSource(  
                    apiService = apiService, imageDtoToImageMapper = mapper,  
                    q = q  
                )  
            }  
        )  
  
    }  
}

```

# Adding the UseCases

`domain/useCase/GetImagesUseCase`

```kotlin

class GetImagesUseCase @Inject constructor(private val repository: ImageRepository) {  
  
    operator fun invoke(q: String) = repository.getImages(q)  
  
}

```

# Presentation(UI)

`presentation/ImageViewModel.kt`

```kotlin

@OptIn(ExperimentalCoroutinesApi::class, FlowPreview::class)  
@HiltViewModel  
class ImageViewModel @Inject constructor(  
    private val getImagesUseCase: GetImagesUseCase  
) : ViewModel() {  
  
    private val _query = MutableStateFlow("")  
  
    val images = _query  
        .filter { it.isNotBlank() }  
        .debounce(1000)  
        .flatMapLatest { query ->  
            getImagesUseCase.invoke(query).flow  
        }.cachedIn(viewModelScope)  
  
    fun updateQuery(q:String) = _query.update { q }  
  
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
            val viewModel = hiltViewModel<ImageViewModel>()  
            var query by rememberSaveable { mutableStateOf("") }  
            ImageSearchAppTheme {  
                Scaffold(modifier = Modifier  
                    .safeContentPadding()  
                    .fillMaxSize(),  
                    topBar = {  
                        TextField(modifier = Modifier.fillMaxWidth(),  
                            value = query,  
                            onValueChange = {  
                                query = it  
                                viewModel.updateQuery(query)  
                            })  
                    }) { innerPadding ->  
                    MainContent(  
                        modifier = Modifier  
                            .padding(innerPadding)  
                            .fillMaxSize(), viewModel  
                    )  
                }  
            }        }    }  
}  
  
@Composable  
fun MainContent(modifier: Modifier = Modifier, viewModel: ImageViewModel) {  
  
    val paging = viewModel.images.collectAsLazyPagingItems()  
  
  
    if (paging.loadState.refresh is LoadState.Error) {  
        Button(modifier = Modifier  
            .padding(24.dp)  
            .fillMaxWidth(), onClick = {  
            paging.retry()  
        }) {  
            Text("Retry")  
        }  
    }  
  
    if (paging.loadState.refresh is LoadState.Loading) {  
        Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {  
            CircularProgressIndicator()  
        }  
    }  
  
    if (paging.loadState.refresh is LoadState.NotLoading) {  
        if (paging.itemCount == 0) {  
            Box(  
                modifier = Modifier.fillMaxSize(1f),  
                contentAlignment = Alignment.Center  
            ) {  
                Text("Nothing found")  
            }  
        }  
    }  
  
    LazyVerticalGrid(  
        modifier = modifier,  
        columns = GridCells.Fixed(2)  
    ) {  
        item {  
            if (paging.loadState.prepend is LoadState.Loading) {  
                Box(Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {  
                    CircularProgressIndicator()  
                }  
            }  
        }  
  
        item {  
            if (paging.loadState.prepend is LoadState.Error) {  
                Button(modifier = Modifier  
                    .fillMaxWidth(), onClick = {  
                    paging.retry()  
                }) {  
                    Text("Retry")  
                }  
            }  
        }  
  
        if (paging.loadState.refresh is LoadState.NotLoading) {  
            if (paging.itemCount != 0) {  
                items(  
                    count = paging.itemCount,  
                    key = paging.itemKey { it.uuid },  
                    contentType = paging.itemContentType { "contentType" }) { index ->  
                    paging[index]?.let { item ->  
                        AsyncImage(  
                            model = item.imageUrl,  
                            contentDescription = null,  
                            contentScale = ContentScale.Crop,  
                            modifier = Modifier  
                                .padding(2.dp)  
                                .fillMaxWidth()  
                                .height(200.dp)  
                        )  
                    }  
                }            }  
        }  
  
        item {  
            if (paging.loadState.append is LoadState.Loading) {  
                Box(Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {  
                    CircularProgressIndicator()  
                }  
            }  
        }  
        item {  
            if (paging.loadState.append is LoadState.Error) {  
                Button(modifier = Modifier  
                    .padding(24.dp)  
                    .fillMaxWidth(), onClick = {  
                    paging.retry()  
                }) {  
                    Text("Retry")  
                }  
            }  
        }  
    }  
  
}

```