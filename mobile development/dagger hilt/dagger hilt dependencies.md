
### step 1: Add this to your top level `build.gradle.kts`

```kotlin

plugins {  

    id("com.google.dagger.hilt.android") version "2.57.1" apply false  
    id("com.google.devtools.ksp") version "2.1.21-2.0.1" apply false  
    
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
  
  
    val nav_version = "2.9.2"  
  
    // Jetpack Compose integration  
    implementation("androidx.navigation:navigation-compose:$nav_version")  
    implementation("androidx.paging:paging-runtime:3.3.6") // For non-Compose parts  
    implementation("androidx.paging:paging-compose:3.3.6") // Compose integration  
  
    // dagger hilt    
    implementation("com.google.dagger:hilt-android:2.57.1")  
	ksp("com.google.dagger:hilt-android-compiler:2.57.1")  
	ksp("androidx.hilt:hilt-compiler:1.3.0")  
	implementation("androidx.hilt:hilt-navigation-compose:1.3.0")
  
}

```


