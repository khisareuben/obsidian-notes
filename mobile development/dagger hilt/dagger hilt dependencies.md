
### step 1: Add this to your top level `build.gradle.kts`

```kotlin

plugins {  

    id("com.google.dagger.hilt.android") version "2.57.2" apply false  
	id("com.google.devtools.ksp") version "2.1.21-2.0.2" apply false
    
}

```

### step 2: Add this to your `build.gradle.kts(:app)`

```kotlin

plugins {  
    
    kotlin("plugin.serialization") version "2.0.21"  
    id("com.google.dagger.hilt.android")  
    id("com.google.devtools.ksp") 
    
}


dependencies {   
  
    implementation ("com.squareup.retrofit2:retrofit:3.0.0")  
    implementation ("com.squareup.retrofit2:converter-gson:3.0.0")  
  
  
    val nav_version = "2.9.5"  
  
	// Jetpack Compose integration  
	implementation("androidx.navigation:navigation-compose:$nav_version")  
	implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.9.4")  
	implementation("androidx.paging:paging-runtime:3.3.6") // For non-Compose parts  
	implementation("androidx.paging:paging-compose:3.3.6") // Compose integration  
	  
	// dagger hilt  
	implementation("com.google.dagger:hilt-android:2.57.2")  
	ksp("com.google.dagger:hilt-android-compiler:2.57.2")  
	ksp("androidx.hilt:hilt-compiler:1.3.0")  
	implementation("androidx.hilt:hilt-navigation-compose:1.3.0")  
	implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.9.4")  
	  
	val room_version = "2.8.3"  
	implementation("androidx.room:room-runtime:$room_version")  
	ksp("androidx.room:room-compiler:$room_version")
  
}

```


```kotlin

//navigation  
val nav_version = "2.9.5"  
implementation("androidx.navigation:navigation-compose:$nav_version")  
  
// room database  
val room_version = "2.8.2"  
implementation("androidx.room:room-runtime:$room_version")  
ksp("androidx.room:room-compiler:2.8.2")  
implementation("androidx.room:room-paging:2.8.2")  
  
// koin dependency injection  
implementation("io.insert-koin:koin-core:4.1.1")  
implementation("io.insert-koin:koin-android:4.1.1")  
implementation("io.insert-koin:koin-androidx-compose:4.1.1")  
  
// dagger hilt  
implementation("com.google.dagger:hilt-android:2.57.2")  
ksp("com.google.dagger:hilt-android-compiler:2.57.2")  
ksp("androidx.hilt:hilt-compiler:1.3.0")  
implementation("androidx.hilt:hilt-navigation-compose:1.3.0")  
implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.9.4")  
  
  
// retrofit  
implementation("com.squareup.retrofit2:retrofit:3.0.0")  
implementation("com.squareup.retrofit2:converter-gson:3.0.0")  
implementation("com.squareup.okhttp3:okhttp:5.2.1")  
implementation("com.squareup.okhttp3:logging-interceptor:5.2.1")  
  
// Lifecycle components  
implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.9.4")  
implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.9.4")  
implementation("androidx.lifecycle:lifecycle-livedata-ktx:2.9.4")  
  
// Coil for Jetpack Compose  
implementation("io.coil-kt:coil-compose:2.7.0")  
  
// Splash screen API  
implementation("androidx.core:core-splashscreen:1.0.1")  
  
// cloudy for blurring effect  
implementation("com.github.skydoves:cloudy:0.2.7")  
  
// Paging runtime  
implementation("androidx.paging:paging-runtime:3.3.6")  
implementation("androidx.paging:paging-compose:3.3.6")  
  
implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.9.0")  
  
implementation("com.jakewharton.retrofit:retrofit2-kotlinx-serialization-converter:1.0.0")

```