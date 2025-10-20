
```zsh

com.example.learnretrofit/
├── di/
│   └── AppModule.kt
│       └── Provides ApiService, PostRepositoryImpl, UseCases, and Mapper for injection into ViewModel
│
├── domain/
│   ├── model/
│   │   └── Post.kt
│   │       └── Clean domain model used by UI and UseCases; mapped from PostDto
│   ├── repository/
│   │   └── PostRepository.kt
│   │       └── Interface used by UseCases; implemented by PostRepositoryImpl
│   └── usecase/
│       ├── GetPostsUseCase.kt
│       │   └── Calls PostRepository to fetch all posts
│       └── GetPaginatedPostsUseCase.kt
│           └── Uses PostRepository to fetch paginated posts via PagingSource
│
├── data/
│   ├── api/
│   │   └── ApiService.kt
│   │       └── Retrofit interface used by PostRepositoryImpl to fetch data
│   ├── model/
│   │   └── PostDto.kt
│   │       └── API response model; mapped to domain Post via Mapper
│   ├── mapper/
│   │   └── PostMapper.kt
│   │       └── Converts PostDto to Post; used by PostRepositoryImpl
│   ├── repository/
│   │   └── PostRepositoryImpl.kt
│   │       └── Implements PostRepository; uses ApiService and PostMapper
│   └── paging/
│       └── PagingSource.kt
│           └── Used by PostRepositoryImpl and GetPaginatedPostsUseCase for pagination
│
├── ui/
│   ├── PostScreen.kt
│   │   └── Observes PostViewModel and displays Post data
│   └── theme/
│       └── MyAppTheme.kt
│           └── Wraps UI with consistent styling
│
├── viewmodel/
│   └── PostViewModel.kt
│       └── Injects UseCases; exposes state to PostScreen
│
├── MyApp.kt
│   └── Sets up Compose theme and launches PostScreen
│
└── MainActivity.kt
    └── Hosts MyApp and initializes Compose UI



```


## Updated Project Structure with Use Cases

```
com.example.learnretrofit/
├── di/
│   └── AppModule.kt
├── domain/
│   ├── model/
│   │   └── Post.kt
│   ├── repository/
│   │   └── PostRepository.kt
│   └── usecase/
│       ├── GetPostsUseCase.kt
│       └── GetPaginatedPostsUseCase.kt
├── data/
│   ├── api/
│   │   └── ApiService.kt
│   ├── model/
│   │   └── PostDto.kt
│   ├── repository/
│   │   └── PostRepositoryImpl.kt
│   └── paging/
│       └── PagingSource.kt
├── ui/
│   ├── PostScreen.kt
│   └── theme/
│       └── MyAppTheme.kt
├── viewmodel/
│   └── PostViewModel.kt
├── MyApp.kt
└── MainActivity.kt
```

## 📘 File-by-File Breakdown

### 🔧 `di/AppModule.kt`

- **Purpose**: Provides dependency injection setup using Hilt or Koin.
    
- **Connects**: Binds `ApiService`, `PostRepository`, and use cases for injection into ViewModel.
    

### 🧠 `domain/`

#### `model/Post.kt`

- **Purpose**: Represents the clean domain model used across the app.
    
- **Connects**: Used by use cases and UI; mapped from `PostDto`.
    

#### `repository/PostRepository.kt`

- **Purpose**: Interface defining data operations (e.g., fetch posts).
    
- **Connects**: Implemented by `PostRepositoryImpl`, used by use cases.
    

#### `usecase/`

- `GetPostsUseCase.kt`: Fetches all posts (non-paginated).
    
- `GetPaginatedPostsUseCase.kt`: Handles paginated post fetching via PagingSource.
    
- **Connects**: Called by `PostViewModel` to abstract business logic.
    

### 🗃️ `data/`

#### `api/ApiService.kt`

- **Purpose**: Retrofit interface for network calls.
    
- **Connects**: Used by `PostRepositoryImpl` to fetch data.
    

#### `model/PostDto.kt`

- **Purpose**: Data Transfer Object (DTO) from API.
    
- **Connects**: Mapped to `Post` domain model.
    

#### `repository/PostRepositoryImpl.kt`

- **Purpose**: Implements `PostRepository`, handles API calls and mapping.
    
- **Connects**: Uses `ApiService`, returns domain models to use cases.
    

#### `paging/PagingSource.kt`

- **Purpose**: Custom PagingSource for paginated API calls.
    
- **Connects**: Used by `GetPaginatedPostsUseCase` and `PostViewModel`.
    

### 🎨 `ui/`

#### `PostScreen.kt`

- **Purpose**: Composable screen displaying posts.
    
- **Connects**: Observes `PostViewModel` state and renders UI.
    

#### `theme/MyAppTheme.kt`

- **Purpose**: Defines app-wide theme (colors, typography).
    
- **Connects**: Used by `MyApp.kt` to wrap the UI.
    

### 🎛️ `viewmodel/PostViewModel.kt`

- **Purpose**: Holds UI state, calls use cases, exposes data to UI.
    
- **Connects**: Injects use cases, observed by `PostScreen`.
    

### 🚀 `MyApp.kt`

- **Purpose**: Entry point for Jetpack Compose app.
    
- **Connects**: Sets up theme and navigation.
    

### 📱 `MainActivity.kt`

- **Purpose**: Hosts Compose content.
    
- **Connects**: Launches `MyApp`.
    

## 🧠 How It All Comes Together

1. **UI** (`PostScreen`) observes **ViewModel** (`PostViewModel`).
    
2. **ViewModel** calls **UseCases** (`GetPostsUseCase`, `GetPaginatedPostsUseCase`).
    
3. **UseCases** depend on **Repository Interface** (`PostRepository`).
    
4. **RepositoryImpl** uses **ApiService** to fetch data and maps **DTOs** to **domain models**.
    
5. **DI Module** wires everything together for injection.