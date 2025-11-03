
## Adding the API

`data/remote/NewsApi.kt`


```kotlin

interface NewsApi {  
  
    //https://newsapi.org/v2/top-headlines?country=us&apiKey=2b3350c2e130493a94f280d8c05ca388  
  
    @GET("top-headlines")  
    suspend fun getBreakingNews(  
        @Query("category") category: String,  
        @Query("country") country: String = "us",  
        @Query("apiKey") apiKey: String = API_KEY  
    ): NewsResponse  
  
    @GET("everything")  
    suspend fun searchForNews(  
        @Query("q") query: String,  
        @Query("apiKey") apiKey: String = API_KEY  
    ): NewsResponse  
  
    companion object {  
        const val API_KEY = "2b3350c2e130493a94f280d8c05ca388"  
        const val BASE_URL = "https://newsapi.org/v2/"  
    }  
}

```


## Adding the data

**Note:** This did not follow the clean architecture pattern, so this file should be in the data and not in the model. So this project does not have usecases and other clean architecture patterns and should only be used for familiarity and not to be followed explicitly.

https://newsapi.org/v2/top-headlines?country=us&apiKey=2b3350c2e130493a94f280d8c05ca388

Open the url to get the json response and then copy everything -> Right click on remote/dto -> new -> Kotlin data file class from Json -> Paste the json code -> name the file

`domain/model/Article.kt,NewsResponse.kt,Source.kt`

```kotlin

data class Article(  
    val author: String?,  
    val content: String?,  
    val description: String?,  
    val publishedAt: String?,  
    val source: Source,  
    val title: String,  
    val url: String,  
    val urlToImage: String  
)

```

```kotlin

data class NewsResponse(  
    val articles: List<Article>,  
    val status: String,  
    val totalResults: Int  
)

```

```kotlin

data class Source(  
    val id: String,  
    val name: String?  
)

```


## Adding the resource file
This handles the error, success of the app as we are not using paging

```kotlin

sealed class Resource<T>(val data: T? = null, val message: String? = null) {  
    class Success<T>(data: T?) : Resource<T>(data = data)  
    class Error<T>(message: String?) : Resource<T>(message = message)  
}

```

## Adding the repository and its implementation

`domain/repository/NewsRepository.kt`

```kotlin

interface NewsRepository {  
  
    suspend fun getTopHeadlines(  
        category: String  
    ): Resource<List<Article>>  
  
  
    suspend fun searchForNews(  
        query: String  
    ): Resource<List<Article>>  
}

```


`data/repository/NewsRepositoryImpl.kt`

```kotlin

class NewsRepositoryImpl(  
    private val newsApi: NewsApi  
): NewsRepository {  
  
    override suspend fun getTopHeadlines(category: String): Resource<List<Article>> {  
        return try {  
            val response = newsApi.getBreakingNews(category = category)  
            Resource.Success(data = response.articles)  
        } catch (e: Exception) {  
            Resource.Error(message = "Failed to fetch news ${e.message}")  
        }  
    }  
  
    override suspend fun searchForNews(query: String): Resource<List<Article>> {  
        return try {  
            val response = newsApi.searchForNews(query = query)  
            Resource.Success(data = response.articles)  
        } catch (e: Exception) {  
            Resource.Error(message = "Failed to fetch news ${e.message}")  
        }  
    }  
}

```


## Adding the di

`di/AppModule.kt`
```kotlin

@Module  
@InstallIn(SingletonComponent::class)  
object AppModule {  
  
    @Provides  
    @Singleton    
    fun provideNewsApi(): NewsApi {  
        val retrofit = Retrofit.Builder()  
            .baseUrl(BASE_URL)  
            .addConverterFactory(GsonConverterFactory.create())  
            .build()  
        return retrofit.create(NewsApi::class.java)  
    }  
  
    @Provides  
    @Singleton    
    fun provideNewsRepository(newsApi: NewsApi): NewsRepository {  
        return NewsRepositoryImpl(newsApi = newsApi)  
    }  
}

```

`MyApp.kt`

```kotlin

@HiltAndroidApp  
class MyApplication: Application()

```


# Adding the Utils

`util/DateFormatter.kt, NavGraphSetup.kt`

```kotlin

fun dateFormatter(inputDateTime: String?): String {  
    val inputFormatter = DateTimeFormatter.ISO_OFFSET_DATE_TIME  
    val outputFormatter = DateTimeFormatter  
        .ofLocalizedDate(FormatStyle.LONG)  
        .withLocale(Locale.getDefault())  
    val dateString = try {  
        val dateTime = OffsetDateTime.parse(inputDateTime, inputFormatter)  
        dateTime.format(outputFormatter)  
    } catch (e: Exception) {  
        ""  
    }  
    return dateString  
}

```

```kotlin

@Composable  
fun NavGraphSetup(  
    navController: NavHostController  
) {  
    val argKey = "web_url"  
  
    NavHost(  
        navController = navController,  
        startDestination = "news_screen"  
    ) {  
        composable(route = "news_screen") {  
            val viewModel: NewsScreenViewModel = hiltViewModel()  
            NewsScreen(  
                state = viewModel.state,  
                onEvent = viewModel::onEvent,  
                onReadFullStoryButtonClick = { url ->  
                    navController.navigate("article_screen?$argKey=$url")  
                }  
            )  
        }  
        composable(  
            route = "article_screen?$argKey={$argKey}",  
            arguments = listOf(navArgument(name = argKey) {  
                type = NavType.StringType  
            })  
        ) { backStackEntry ->  
            ArticleScreen(  
                url = backStackEntry.arguments?.getString(argKey),  
                onBackPressed = { navController.navigateUp() }  
            )  
        }  
    }}

```

