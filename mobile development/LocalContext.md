
## What Is `LocalContext.current` in Jetpack Compose?

In **Jetpack Compose**, `LocalContext.current` is how you access the **Android** `Context` inside a `@Composable` function.

### 🔹 What is `Context` in Android?

In traditional Android development, `Context` is an object that gives you access to:

- System services (like `ClipboardManager`, `LocationManager`)
    
- Resources (like strings, colors, dimensions)
    
- Starting activities or showing toasts
    
- Accessing databases, preferences, etc.
    

In an `Activity`, you’d normally use `this` or `applicationContext` to get it.


```kotlin

val appModule = module {  
  
    single {  
        val contentType = "application/json".toMediaType()  
        val json = Json { ignoreUnknownKeys = true }  
  
        val client = OkHttpClient.Builder()  
            .addInterceptor(AuthInterceptor())  
            .build()  
  
        Retrofit.Builder()  
            .baseUrl(Constants.BASE_URL)  
            .client(client)  
            .addConverterFactory(json.asConverterFactory(contentType))  
            .build()  
            .create(UnsplashApiService::class.java)  
    }  
  
    single {  
        Room.databaseBuilder(  
            androidContext(),  
            PhotoFetchDatabase::class.java,  
            PHOTO_FETCH_DATABASE  
        ).build()  
    }  
  
  
    single<ImageRepository> { ImageRepositoryImpl(get(), get()) }  
  
    single<Downloader> { AndroidImageDownloader(get()) }  
  
    single<NetworkConnectivityObserver> { NetworkConnectivityObserverImpl(context = androidContext(), scope = get()) }  
  
    single<CoroutineScope> { CoroutineScope(SupervisorJob() + Dispatchers.Default) }  
  
  
    viewModel { HomeViewModel(get()) }  
    viewModel { SearchViewModel(get()) }  
  
    viewModel { (imageId: String) ->  
        FullImageViewModel(  
            repository = get(),  
            downloader = get(),  
            savedStateHandle = SavedStateHandle ().apply {  
                set("imageId", imageId)  
            },  
        )  
    }  
  
  
  
}  

//this is for the api key  
class AuthInterceptor : Interceptor {  
    override fun intercept(chain: Interceptor.Chain): Response {  
        val request = chain.request().newBuilder()  
            .addHeader("Authorization", "Client-ID ${Constants.API_KEY}")  
            .build()  
        return chain.proceed(request)  
    }  
}

```

```kotlin
// for storing constant variables
object Constants {  
  
    const val IV_LOG_TAG = "ImageVistaLogs"  
  
    const val API_KEY = BuildConfig.UNSPLASH_API_KEY  
    const val BASE_URL = "https://api.unsplash.com/"  
  
    const val PHOTO_FETCH_DATABASE = "unsplash_images.db"  
  
    const val FAVORITE_IMAGES_TABLE = "favorite_images_table"  
  
    const val ITEMS_PER_PAGE = 10  
}

```

```kotlin

interface UnsplashApiService {  
  
    //@Headers("Authorization: Client-ID $API_KEY")  
    @GET("/photos")  
    suspend fun getEditorialFeedImages(): List<UnsplashImageDto>  
  
    @GET("/search/photos")  
    suspend fun searchImages(  
        @Query("query") query: String,  
        @Query("page") page: Int,  
        @Query("per_page") perPage: Int,  
    ): UnsplashImagesSearchResult  
  
    @GET("/photos/{id}")  
    suspend fun getImage(  
        @Path("id") imageId: String  
    ): UnsplashImageDto  
  
}

```