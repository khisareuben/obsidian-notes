
## 1. Add Dependencies

In your `build.gradle` (app-level):



```kotlin
dependencies {
    // Paging 3
    implementation "androidx.paging:paging-runtime:3.3.0"

    // Ktor client
    implementation "io.ktor:ktor-client-core:2.3.0"
    implementation "io.ktor:ktor-client-cio:2.3.0" // CIO engine
    implementation "io.ktor:ktor-client-content-negotiation:2.3.0"
    implementation "io.ktor:ktor-serialization-kotlinx-json:2.3.0"

    // Hilt (already in your project)
    implementation "com.google.dagger:hilt-android:2.51"
    kapt "com.google.dagger:hilt-compiler:2.51"
}
```

## 2. Setup Ktor Client

Create a file `data/remote/KtorClientProvider.kt`:



```kotlin
import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.json.Json

object KtorClientProvider {
    val client = HttpClient(CIO) {
        install(ContentNegotiation) {
            json(Json {
                ignoreUnknownKeys = true // avoids crashes if API returns extra fields
                prettyPrint = true
                isLenient = true
            })
        }
    }
}
```

This replaces Retrofit. The `HttpClient` is reusable across your app.

## 3. Define API Service with Ktor

Create `data/remote/CoinApi.kt`:



```kotlin
import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.request.*
import io.ktor.http.*

class CoinApi(private val client: HttpClient) {

    suspend fun getCoins(page: Int, pageSize: Int): List<CoinDto> {
        return client.get("https://api.coinpaprika.com/v1/coins") {
            parameter("offset", (page - 1) * pageSize)
            parameter("limit", pageSize)
        }.body()
    }

    suspend fun getCoinDetail(coinId: String): CoinDetailDto {
        return client.get("https://api.coinpaprika.com/v1/coins/$coinId").body()
    }
}
```

Notice how `client.get` replaces Retrofit’s `@GET` annotations. You directly build requests.

## 4. Create PagingSource

Paging 3 needs a `PagingSource`. Create `data/paging/CoinPagingSource.kt`:



```kotlin
import androidx.paging.PagingSource
import androidx.paging.PagingState

class CoinPagingSource(
    private val api: CoinApi,
    private val pageSize: Int = 20
) : PagingSource<Int, Coin>() {

    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, Coin> {
        return try {
            val page = params.key ?: 1
            val coins = api.getCoins(page, pageSize).map { it.toDomain() }

            LoadResult.Page(
                data = coins,
                prevKey = if (page == 1) null else page - 1,
                nextKey = if (coins.isEmpty()) null else page + 1
            )
        } catch (e: Exception) {
            LoadResult.Error(e)
        }
    }

    override fun getRefreshKey(state: PagingState<Int, Coin>): Int? {
        return state.anchorPosition?.let { anchor ->
            state.closestPageToPosition(anchor)?.prevKey?.plus(1)
                ?: state.closestPageToPosition(anchor)?.nextKey?.minus(1)
        }
    }
}
```

## 5. Repository Layer

Create `data/repository/CoinRepository.kt`:



```kotlin
import androidx.paging.Pager
import androidx.paging.PagingConfig
import androidx.paging.PagingData
import kotlinx.coroutines.flow.Flow

class CoinRepository(private val api: CoinApi) {

    fun getCoinsPaged(): Flow<PagingData<Coin>> {
        return Pager(
            config = PagingConfig(
                pageSize = 20,
                enablePlaceholders = false
            ),
            pagingSourceFactory = { CoinPagingSource(api) }
        ).flow
    }

    suspend fun getCoinDetail(coinId: String): CoinDetail {
        return api.getCoinDetail(coinId).toDomain()
    }
}
```

## 6. Update ViewModels

### CoinListViewModel



```kotlin
@HiltViewModel
class CoinListViewModel @Inject constructor(
    private val repository: CoinRepository
) : ViewModel() {

    val coins: Flow<PagingData<Coin>> = repository.getCoinsPaged()
        .cachedIn(viewModelScope)
}
```

### CoinDetailViewModel



```kotlin
@HiltViewModel
class CoinDetailViewModel @Inject constructor(
    private val repository: CoinRepository,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val _state = mutableStateOf(CoinDetailState())
    val state: State<CoinDetailState> = _state

    init {
        savedStateHandle.get<String>(Constants.PARAM_COIN_ID)?.let { coinId ->
            getCoin(coinId)
        }
    }

    private fun getCoin(coinId: String) {
        viewModelScope.launch {
            try {
                val coin = repository.getCoinDetail(coinId)
                _state.value = CoinDetailState(coin = coin)
            } catch (e: Exception) {
                _state.value = CoinDetailState(error = e.message ?: "Unexpected error")
            }
        }
    }
}
```

## 7. Update UI with Paging

In `CoinListScreen.kt`:



```kotlin
@Composable
fun CoinListScreen(
    navController: NavController,
    viewModel: CoinListViewModel = hiltViewModel()
) {
    val coins = viewModel.coins.collectAsLazyPagingItems()

    LazyColumn(modifier = Modifier.fillMaxSize()) {
        items(coins) { coin ->
            coin?.let {
                CoinListItem(
                    coin = it,
                    onItemClick = { navController.navigate(Screen.CoinDetailScreen.route + "/${it.id}") }
                )
            }
        }

        coins.apply {
            when {
                loadState.refresh is LoadState.Loading -> {
                    item { CircularProgressIndicator(modifier = Modifier.align(Alignment.CenterHorizontally)) }
                }
                loadState.append is LoadState.Error -> {
                    item { Text("Error loading more coins") }
                }
            }
        }
    }
}
```

# ✅ Summary

You now have:

- **Ktor client** replacing Retrofit
    
- **PagingSource + Pager** for infinite scrolling
    
- **Repository** bridging API and ViewModel
    
- **ViewModels** updated to expose PagingData
    
- **UI** updated to consume `LazyPagingItems`
    

This setup is clean, scalable, and modern.