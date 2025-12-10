

# Tutorial: Building an Android app with Ktor, Paging 3, and Dagger Hilt using JSONPlaceholder

You’re about to build a clean, modern Android app that fetches posts from JSONPlaceholder, paginates them with Paging 3, uses Ktor for networking, and wires everything together with Hilt. I’ll include all the Ktor pieces so you get comfortable with the client setup, plugins, and request building.

## Project setup and dependencies

### Gradle configuration

Add these to your app-level `build.gradle`:



```kotlin
plugins {
    id "com.android.application"
    id "org.jetbrains.kotlin.android"
    id "org.jetbrains.kotlin.plugin.serialization" version "1.9.22"
    id "com.google.dagger.hilt.android"
    id "kotlin-kapt"
}

android {
    namespace "com.example.jsonplaceholder"
    compileSdk 34

    defaultConfig {
        applicationId "com.example.jsonplaceholder"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    buildFeatures {
        compose true
    }
    composeOptions {
        kotlinCompilerExtensionVersion "1.5.12"
    }
}

dependencies {
    // Compose
    implementation "androidx.compose.ui:ui:1.6.5"
    implementation "androidx.compose.material3:material3:1.2.1"
    implementation "androidx.activity:activity-compose:1.8.2"
    implementation "androidx.navigation:navigation-compose:2.7.5"

    // Lifecycle
    implementation "androidx.lifecycle:lifecycle-runtime-ktx:2.6.2"
    implementation "androidx.lifecycle:lifecycle-viewmodel-compose:2.6.2"

    // Coroutines
    implementation "org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3"

    // Paging 3
    implementation "androidx.paging:paging-runtime:3.2.1"
    implementation "androidx.paging:paging-compose:3.2.1"

    // Hilt
    implementation "com.google.dagger:hilt-android:2.51"
    kapt "com.google.dagger:hilt-compiler:2.51"

    // Ktor Client
    implementation "io.ktor:ktor-client-core:2.3.7"
    implementation "io.ktor:ktor-client-cio:2.3.7"
    implementation "io.ktor:ktor-client-content-negotiation:2.3.7"
    implementation "io.ktor:ktor-serialization-kotlinx-json:2.3.7"
    implementation "io.ktor:ktor-client-logging:2.3.7"
}
```

Add Hilt to your project-level `build.gradle` classpath if needed:



```kotlin
dependencies {
    classpath "com.google.dagger:hilt-android-gradle-plugin:2.51"
}
```

## Package structure and models

Use these packages:

- data
    
- domain
    
- presentation
    
- di
    
- utils
    

### Utils

`utils/Constants.kt`



```kotlin
object Constants {
    const val BASE_URL = "https://jsonplaceholder.typicode.com"
    const val PAGE_SIZE = 20
}
```

`utils/Resource.kt`



```kotlin
sealed class Resource<T>(val data: T? = null, val message: String? = null) {
    class Success<T>(data: T) : Resource<T>(data)
    class Error<T>(message: String, data: T? = null) : Resource<T>(data, message)
    class Loading<T>(data: T? = null): Resource<T>(data)
}
```

### DTOs and domain models (kotlinx.serialization)

`data/remote/dto/PostDto.kt`



```kotlin
import kotlinx.serialization.Serializable

@Serializable
data class PostDto(
    val userId: Int,
    val id: Int,
    val title: String,
    val body: String
)
```

`domain/model/Post.kt`



```kotlin
data class Post(
    val id: Int,
    val title: String,
    val body: String
)

fun PostDto.toPost(): Post {
    return Post(
        id = id,
        title = title,
        body = body
    )
}
```

## Ktor client and API service

### Ktor client provider

`data/remote/KtorClientProvider.kt`



```kotlin
import io.ktor.client.HttpClient
import io.ktor.client.engine.cio.CIO
import io.ktor.client.plugins.DefaultRequest
import io.ktor.client.plugins.HttpTimeout
import io.ktor.client.plugins.logging.Logging
import io.ktor.client.plugins.logging.LogLevel
import io.ktor.client.plugins.logging.Logger
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.http.URLProtocol
import io.ktor.serialization.kotlinx.json.json
import kotlinx.serialization.json.Json

object KtorClientProvider {
    val client = HttpClient(CIO) {
        // Serialization
        install(ContentNegotiation) {
            json(Json {
                ignoreUnknownKeys = true     // Don’t crash on extra fields
                isLenient = true             // Allow non-strict JSON
                prettyPrint = false
            })
        }

        // Logging (useful while learning)
        install(Logging) {
            logger = Logger.DEFAULT
            level = LogLevel.INFO
        }

        // Timeouts (safe defaults)
        install(HttpTimeout) {
            requestTimeoutMillis = 30_000
            connectTimeoutMillis = 15_000
            socketTimeoutMillis = 30_000
        }

        // Default request config (base host, default headers)
        install(DefaultRequest) {
            url {
                protocol = URLProtocol.HTTPS
                host = "jsonplaceholder.typicode.com"
            }
            headers.append("Accept", "application/json")
        }
    }
}
```

### API service (Ktor requests)

`data/remote/JsonPlaceholderApi.kt`



```kotlin
import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.request.get
import io.ktor.client.request.parameter

class JsonPlaceholderApi(private val client: HttpClient) {

    // Note: JSONPlaceholder supports _start and _limit for pagination.
    suspend fun getPostsPage(page: Int, pageSize: Int): List<PostDto> {
        val start = (page - 1) * pageSize
        return client.get("/posts") {
            parameter("_start", start)
            parameter("_limit", pageSize)
        }.body()
    }

    suspend fun getPostById(id: Int): PostDto {
        return client.get("/posts/$id").body()
    }
}
```

Tip:

> If you want to observe raw responses while learning Ktor, reduce `Logging` to `LogLevel.BODY` in the client config.

## Paging 3 integration and repository

### PagingSource for posts

`data/paging/PostsPagingSource.kt`



```kotlin
import androidx.paging.PagingSource
import androidx.paging.PagingState

class PostsPagingSource(
    private val api: JsonPlaceholderApi,
    private val pageSize: Int
) : PagingSource<Int, Post>() {

    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, Post> {
        return try {
            val page = params.key ?: 1
            val posts = api.getPostsPage(page, pageSize).map { it.toPost() }

            LoadResult.Page(
                data = posts,
                prevKey = if (page == 1) null else page - 1,
                nextKey = if (posts.isEmpty()) null else page + 1
            )
        } catch (e: Exception) {
            LoadResult.Error(e)
        }
    }

    override fun getRefreshKey(state: PagingState<Int, Post>): Int? {
        return state.anchorPosition?.let { anchor ->
            state.closestPageToPosition(anchor)?.prevKey?.plus(1)
                ?: state.closestPageToPosition(anchor)?.nextKey?.minus(1)
        }
    }
}
```

### Repository bridging Ktor and Paging

`data/repository/PostRepository.kt`



```kotlin
import androidx.paging.Pager
import androidx.paging.PagingConfig
import androidx.paging.PagingData
import kotlinx.coroutines.flow.Flow

class PostRepository(
    private val api: JsonPlaceholderApi
) {

    fun getPostsPaged(pageSize: Int): Flow<PagingData<Post>> {
        return Pager(
            config = PagingConfig(
                pageSize = pageSize,
                enablePlaceholders = false
            ),
            pagingSourceFactory = { PostsPagingSource(api, pageSize) }
        ).flow
    }

    suspend fun getPostById(id: Int): Post {
        return api.getPostById(id).toPost()
    }
}
```

## Dependency injection with Hilt

### Application class

`MyApp.kt`



```kotlin
import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class MyApp : Application()
```

### Hilt module

`di/AppModule.kt`



```kotlin
import com.example.jsonplaceholder.data.remote.JsonPlaceholderApi
import com.example.jsonplaceholder.data.remote.KtorClientProvider
import com.example.jsonplaceholder.data.repository.PostRepository
import com.example.jsonplaceholder.utils.Constants
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import io.ktor.client.HttpClient
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideHttpClient(): HttpClient = KtorClientProvider.client

    @Provides
    @Singleton
    fun provideJsonPlaceholderApi(client: HttpClient): JsonPlaceholderApi =
        JsonPlaceholderApi(client)

    @Provides
    @Singleton
    fun providePostRepository(api: JsonPlaceholderApi): PostRepository =
        PostRepository(api)
}
```

## Presentation layer with Paging and Compose

### Navigation routes

`presentation/Screen.kt`



```kotlin
sealed class Screen(val route: String) {
    object PostList : Screen("post_list")
    object PostDetail : Screen("post_detail")
}
```

### ViewModels

`presentation/post_list/PostListViewModel.kt`



```kotlin
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.paging.PagingData
import androidx.paging.cachedIn
import com.example.jsonplaceholder.data.repository.PostRepository
import com.example.jsonplaceholder.domain.model.Post
import com.example.jsonplaceholder.utils.Constants
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject

@HiltViewModel
class PostListViewModel @Inject constructor(
    repository: PostRepository
) : ViewModel() {

    val posts: Flow<PagingData<Post>> =
        repository.getPostsPaged(Constants.PAGE_SIZE).cachedIn(viewModelScope)
}
```

`presentation/post_detail/PostDetailViewModel.kt`



```kotlin
import androidx.compose.runtime.State
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.jsonplaceholder.data.repository.PostRepository
import com.example.jsonplaceholder.domain.model.Post
import com.example.jsonplaceholder.utils.Resource
import dagger.hilt.android.lifecycle.HiltViewModel
import androidx.lifecycle.SavedStateHandle
import kotlinx.coroutines.launch
import javax.inject.Inject

data class PostDetailState(
    val isLoading: Boolean = false,
    val post: Post? = null,
    val error: String = ""
)

@HiltViewModel
class PostDetailViewModel @Inject constructor(
    private val repository: PostRepository,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val _state = mutableStateOf(PostDetailState())
    val state: State<PostDetailState> = _state

    init {
        // Expecting nav route like "post_detail/{postId}"
        val postId = savedStateHandle.get<String>("postId")?.toIntOrNull()
        postId?.let { loadPost(it) }
    }

    private fun loadPost(id: Int) {
        viewModelScope.launch {
            _state.value = PostDetailState(isLoading = true)
            try {
                val post = repository.getPostById(id)
                _state.value = PostDetailState(post = post)
            } catch (e: Exception) {
                _state.value = PostDetailState(error = e.message ?: "Unexpected error")
            }
        }
    }
}
```

### Composables

`presentation/post_list/components/PostListItem.kt`



```kotlin
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.example.jsonplaceholder.domain.model.Post

@Composable
fun PostListItem(
    post: Post,
    onClick: (Post) -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick(post) }
            .padding(16.dp)
    ) {
        Text(
            text = "${post.id}. ${post.title}",
            style = MaterialTheme.typography.titleMedium,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
        Spacer(Modifier.height(8.dp))
        Text(
            text = post.body,
            style = MaterialTheme.typography.bodyMedium,
            maxLines = 2,
            overflow = TextOverflow.Ellipsis
        )
    }
}
```

`presentation/post_list/PostListScreen.kt`



```kotlin
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavController
import androidx.paging.LoadState
import androidx.paging.compose.collectAsLazyPagingItems
import androidx.paging.compose.items
import com.example.jsonplaceholder.presentation.Screen

@Composable
fun PostListScreen(
    navController: NavController,
    viewModel: PostListViewModel = hiltViewModel()
) {
    val posts = viewModel.posts.collectAsLazyPagingItems()

    LazyColumn(modifier = Modifier.fillMaxSize()) {

        items(posts) { post ->
            post?.let {
                PostListItem(post = it) { selected ->
                    navController.navigate("${Screen.PostDetail.route}/${selected.id}")
                }
            }
        }

        when {
            posts.loadState.refresh is LoadState.Loading -> {
                item { LinearProgressIndicator(modifier = Modifier.fillParentMaxWidth()) }
            }
            posts.loadState.append is LoadState.Loading -> {
                item { CircularProgressIndicator() }
            }
            posts.loadState.refresh is LoadState.Error -> {
                val e = posts.loadState.refresh as LoadState.Error
                item {
                    Text(
                        text = "Error: ${e.error.message}",
                        color = MaterialTheme.colorScheme.error
                    )
                }
            }
            posts.loadState.append is LoadState.Error -> {
                val e = posts.loadState.append as LoadState.Error
                item {
                    Text(
                        text = "More load error: ${e.error.message}",
                        color = MaterialTheme.colorScheme.error
                    )
                }
            }
        }
    }
}
```

`presentation/post_detail/PostDetailScreen.kt`



```kotlin
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.hilt.navigation.compose.hiltViewModel

@Composable
fun PostDetailScreen(
    viewModel: PostDetailViewModel = hiltViewModel()
) {
    val state = viewModel.state.value

    Box(Modifier.fillMaxSize()) {
        state.post?.let { post ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(16.dp)
            ) {
                Text(text = "${post.id}. ${post.title}", style = MaterialTheme.typography.titleLarge)
                Spacer(Modifier.height(12.dp))
                Text(text = post.body, style = MaterialTheme.typography.bodyLarge)
            }
        }

        if (state.isLoading) {
            CircularProgressIndicator(Modifier.align(Alignment.Center))
        }

        if (state.error.isNotBlank()) {
            Text(
                text = state.error,
                color = MaterialTheme.colorScheme.error,
                modifier = Modifier.align(Alignment.Center)
            )
        }
    }
}
```

### MainActivity and NavHost

`MainActivity.kt`



```kotlin
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.jsonplaceholder.presentation.Screen
import com.example.jsonplaceholder.presentation.post_detail.PostDetailScreen
import com.example.jsonplaceholder.presentation.post_list.PostListScreen
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            Surface(color = MaterialTheme.colorScheme.background) {
                val navController = rememberNavController()
                NavHost(
                    navController = navController,
                    startDestination = Screen.PostList.route
                ) {
                    composable(Screen.PostList.route) {
                        PostListScreen(navController)
                    }
                    composable("${Screen.PostDetail.route}/{postId}") {
                        PostDetailScreen()
                    }
                }
            }
        }
    }
}
```

## What to pay attention to while learning Ktor

- **Client plugins:**
    
    - **ContentNegotiation**: Decodes JSON into Kotlin data classes using kotlinx.serialization..
        
    - **Logging**: Helps you see requests/responses.
        
    - **HttpTimeout**: Avoids hanging requests.
        
    - **DefaultRequest**: Base URL and default headers so you don’t repeat yourself.
        
- **Request building with Ktor:**
    
    - **GET calls** are built with `client.get("/path") { parameter("key", value) }`.
        
    - **Path params**: Direct string interpolation like `"/posts/$id"`.
        
    - **Query params**: Use `parameter("key", value)` blocks inside the request.
        
- **PagingSource contracts:**
    
    - **load**: Fetch data for a given page key and return a `LoadResult.Page` or `LoadResult.Error`.
        
    - **getRefreshKey**: Defines where to restart loading on refresh based on the current list anchor.
        
- **Hilt wiring:**
    
    - **Provide the HttpClient** once, reuse it everywhere.
        
    - **Provide your API service** and repository as singletons.
        
    - **Inject repositories into ViewModels** to keep UI logic clean.
        

## Next steps

- **Add caching with Room + RemoteMediator** for offline support.
    
- **Write tests with Ktor’s MockEngine** to simulate responses without hitting the network.
    
- **Add retry UI** on Paging errors and pull-to-refresh.
    

If you want, I can extend this with a MockEngine example and a RemoteMediator variant for Room caching — both are great for mastering Ktor and Paging 3.

i saw that you used the resource file and i always thought that the resource was for apps that don't use pagination because paging library does the things that the resource file has already

That’s a sharp observation, Harold 👍 — you’re right that **Paging 3** already handles a lot of what `Resource` was designed for in non‑paginated apps. Let’s break it down so you see where each fits:

## 🧩 What `Resource` Does

The `Resource<T>` wrapper is a **manual state holder** for:

- Loading: show a spinner while waiting for data.
    
- Success: deliver the data when the request succeeds.
    
- Error: capture and display error messages.
    

This pattern is common when you’re fetching a single object or a one‑time list (e.g. `GetCoinUseCase` returning a list of coins). It gives you a simple way to expose state to the UI.

## 📚 What Paging 3 Already Provides

Paging 3 has its own LoadState system:

- `LoadState.Loading` → while fetching pages.
    
- `LoadState.NotLoading` → when data is ready.
    
- `LoadState.Error` → when a page fails to load.
    

These states are automatically exposed through `LazyPagingItems.loadState` in Compose. That’s why you saw me remove `Resource` in the paging example — because Paging 3 already covers loading/error/success transitions for lists.

## 🔑 When to Use Each

- **Use** `Resource` for:
    
    - Single network calls (e.g. fetching one coin detail).
        
    - Non‑paginated lists.
        
    - Wrapping use cases where you want explicit control over success/error/loading.
        
- **Use Paging 3’s** `LoadState` for:
    
    - Infinite scrolling lists.
        
    - Large datasets where you don’t want to load everything at once.
        
    - Cases where you want built‑in retry, append, prepend, and refresh handling.
        

## ⚡ Hybrid Approach

In a real app, you often use **both**:

- **Coin list** → Paging 3 with `LoadState`.
    
- **Coin detail** → `Resource` because it’s a single fetch.
    

That way, you don’t reinvent the wheel for lists, but you still have a clean state wrapper for one‑off requests.

So your instinct was right: `Resource` is most useful in non‑paginated flows, while Paging 3 replaces it for lists. But keeping `Resource` around for detail screens or other one‑time calls is still a best practice.

Would you like me to show you a **side‑by‑side example** of how the UI consumes `Resource` vs `LoadState`, so you can see the difference in Compose code?