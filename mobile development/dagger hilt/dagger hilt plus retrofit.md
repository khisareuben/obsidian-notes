
``` 

com.example.learnretrofit/
├── di/
│   └── AppModule.kt
├── data/
│   ├── api/
│   │   └── ApiService.kt
│   ├── model/
│   │   └── Post.kt
│   ├── repository/
│   │   ├── PostRepository.kt
│   │   └── PostRepositoryImpl.kt
|	├── paging/
│   │   └── PagingSource.kt
├── ui/
│   ├── PostScreen.kt
│   └── theme/
│       └── MyAppTheme.kt
├── viewmodel/
│   └── PostViewModel.kt
├── MyApp.kt
└── MainActivity.kt


```


## 🌐 1. Permissions (📄 `AndroidManifest.xml`)


```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>

<application
    android:name=".MyApp"
    ...
/>
```



## 2. Data Model (📄 `Post.kt` inside `data/model`)


```kotlin
package com.example.learnretrofit.data.model

data class Post(
    val id: String,
    val title: String,
    val body: String
)
```


## 🔌 3. Retrofit API Interface (📄 `ApiService.kt` inside `data/api`)


```kotlin
package com.example.learnretrofit.data.api

import com.example.retrokoin.data.model.Post  
import retrofit2.http.GET  
import retrofit2.http.Query  
  
interface ApiService {  
  
    @GET("posts")  
    suspend fun getPosts(  
        @Query("_page") page: Int,  
        @Query("_limit") limit: Int  
    ): List<Post>  
  
}
```


# Paging 3 (📄 `PagingSource.kt` inside `data/paging`)

```kotlin

import androidx.paging.PagingSource  
import androidx.paging.PagingState  
import com.example.retrokoin.data.api.ApiService  
import com.example.retrokoin.data.model.Post  
  
  
class PostPagingSource(private val apiService: ApiService) : PagingSource<Int, Post>() {  
    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, Post> {  
        return try {  
            val page = params.key ?: 1  
            val limit = params.loadSize  
            val posts = apiService.getPosts(page, limit)  
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


## 🛠️ 5. Repository Layer (📄 `PostRepository.kt` and `PostRepositoryImpl.kt` inside `data/repository`)



```kotlin
package com.example.learnretrofit.data.repository

import com.example.learnretrofit.data.model.Post

interface PostRepository {  
  
    fun getPagedPosts(): Flow<PagingData<Post>> 
  
}
```


```kotlin
package com.example.learnretrofit.data.repository

import com.example.learnretrofit.data.api.ApiService

class PostRepositoryImpl(private val apiService: ApiService): PostRepository {  
  
    override fun getPagedPosts(): Flow<PagingData<Post>> {  
	    return Pager(  
	        config = PagingConfig(pageSize = 5),  
	        pagingSourceFactory = { PostPagingSource(apiService)}  
	    ).flow  
	}
}

```



## 🔧 6. Dagger hilt Setup (📄 `AppModule.kt` inside `di`)



```kotlin


import com.example.retrokoin.data.api.ApiService  
import com.example.retrokoin.data.repository.PostRepository  
import com.example.retrokoin.data.repository.PostRepositoryImpl  
import dagger.Module  
import dagger.Provides  
import dagger.hilt.InstallIn  
import dagger.hilt.components.SingletonComponent  
import retrofit2.Retrofit  
import retrofit2.converter.gson.GsonConverterFactory  
import javax.inject.Singleton  
  
@Module  
@InstallIn(SingletonComponent::class)  
object AppModule {  

	@Provides  
	@Singleton  
	fun provideRetrofit(): Retrofit {
	    return Retrofit.Builder()  
	        .baseUrl("https://jsonplaceholder.typicode.com")  
	        .addConverterFactory(GsonConverterFactory.create())  
	        .build()  
	}  
	  
	@Provides 
	@Singleton 
	fun provideApiService(retrofit: Retrofit): ApiService {  
	    return retrofit.create(ApiService::class.java)  
	}
	

	@Provides  
    @Singleton    
    fun providePostRepository(apiService: ApiService): PostRepository {  
        return PostRepositoryImpl(apiService)  
    }  
  
}

```



## 🏁 7. Dagger hilt Initialization (📄 `MyApp.kt`)



```kotlin

import android.app.Application  
import dagger.hilt.android.HiltAndroidApp  
  
  
@HiltAndroidApp  
class MyApp : Application()

```



## 🧠 8. ViewModel Layer (📄 `PostViewModel.kt` inside `viewmodel`)



```kotlin

@HiltViewModel  
class PostViewModel @Inject constructor(private val repository: PostRepository): ViewModel() {  
  
  
    val pagedPosts: Flow<PagingData<Post>> = repository  
        .getPagedPosts()  
        .cachedIn(viewModelScope)  
  
  
  
}


```


## 🎨 9. Composable UI Screen (📄 `PostScreen.kt`)


```kotlin

@Composable  
fun PostListScreen(  
    viewModel: PostViewModel = hiltViewModel(),  
    navController: NavHostController  
) {  
    val posts = viewModel.pagedPosts.collectAsLazyPagingItems()  
  
    LazyColumn(  
        modifier = Modifier.padding(16.dp),  
        verticalArrangement = Arrangement.spacedBy(16.dp)  
    ) {  
        items(posts.itemCount) { index ->  
            posts[index]?.let { post ->  
                PostCard(post = post) {  
                    navController.navigate("postDetail/${post.id}/${post.title}/${post.body}")  
                }  
            }        }  
        when {  
            posts.loadState.append is LoadState.Loading -> {  
                item {  
                    CircularProgressIndicator(  
                        modifier = Modifier  
                            .fillMaxWidth()  
                            .padding(16.dp)  
                            .wrapContentWidth(Alignment.CenterHorizontally),  
                        color = MaterialTheme.colorScheme.primary  
                    )  
                }  
            }  
  
            posts.loadState.refresh is LoadState.Error -> {  
                item {  
                    Text(  
                        text = "Failed to load posts. Try again.",  
                        modifier = Modifier.padding(16.dp)  
                    )  
                }  
            }  
        }  
    }  
}  
  
@Composable  
fun PostCard(post: Post, onClick: () -> Unit) {  
  
    Card(  
        modifier = Modifier  
            .fillMaxWidth()  
            .clickable { onClick() },  
        colors = CardDefaults.cardColors(LocalTheme.current.background)  
    ) {  
        Column(modifier = Modifier.padding(16.dp)) {  
            Text(  
                text = "Post ID: ${post.id}",  
                style = MaterialTheme.typography.titleMedium,  
                color = LocalTheme.current.text  
            )  
            Text(text = "Title: ${post.title}",  
                style = MaterialTheme.typography.bodyLarge,  
                color = LocalTheme.current.text)  
            Text(text = "Body: ${post.body}",  
                style = MaterialTheme.typography.bodySmall,  
                color = LocalTheme.current.text)  
  
        }  
    }  
}

```



## 🧪 10. MainActivity Scaffold Setup (📄 `MainActivity.kt`)


```kotlin
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint  
class MainActivity : ComponentActivity() {  
    override fun onCreate(savedInstanceState: Bundle?) {  
        super.onCreate(savedInstanceState)  
        //enableEdgeToEdge()  
        setContent {  
            RetrokoinTheme {  
                val themeColors = if (isSystemInDarkTheme()) darkThemeColors else lightThemeColors  
                CompositionLocalProvider(LocalTheme provides themeColors) {  
                    AppNavGraph()  
                    //Charlie()  
                }  
            }        
		}    
	}  
}

```



## Define Navigation Graph (📄 `NavGraph.kt`)

```kotlin
package com.example.learnretrofit.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.example.learnretrofit.ui.PostDetailScreen
import com.example.learnretrofit.ui.PostListScreen

@Composable
fun AppNavGraph(navController: NavHostController) {
    NavHost(navController = navController, startDestination = "postList") {
        composable("postList") {
            PostListScreen(navController = navController)
        }

        composable("postDetail/{id}/{title}/{body}") { backStackEntry ->
            val id = backStackEntry.arguments?.getString("id") ?: ""
            val title = backStackEntry.arguments?.getString("title") ?: ""
            val body = backStackEntry.arguments?.getString("body") ?: ""

            PostDetailScreen(id = id, title = title, body = body)
        }
    }
}
```


## 📱 4. Create PostDetailScreen (📄 `PostDetailScreen.kt`)



```kotlin
package com.example.learnretrofit.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun PostDetailScreen(id: String, title: String?, body: String?) {
    Column(modifier = Modifier.padding(24.dp)) {
        Text(text = "Post #$id", style = MaterialTheme.typography.headlineMedium)
        Spacer(modifier = Modifier.height(16.dp))
        Text(text = title, style = MaterialTheme.typography.titleLarge)
        Spacer(modifier = Modifier.height(8.dp))
        Text(text = body, style = MaterialTheme.typography.bodyLarge)
    }
}
```

