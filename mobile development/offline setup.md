
### 🔧 Steps to Make Android Studio Work Offline

1. **Enable Gradle Offline Mode**
    
    - In Android Studio, go to:
        
        Code
        
        ```
        File → Settings → Build, Execution, Deployment → Gradle
        ```
        
    - Check **“Offline work”**.
        
    - This tells Gradle to use cached dependencies instead of fetching them online.
        
2. **Pre‑download Dependencies**
    
    - Open your project while online once.
        
    - Run:
        
        bash
        
        ```
        ./gradlew build
        ```
        
    - This will download all required libraries and cache them locally in `~/.gradle/caches`.
        
    - After that, Gradle can reuse them offline.
        
3. **Download SDKs and Tools in Advance**
    
    - Open **SDK Manager** in Android Studio.
        
    - Install:
        
        - Android SDK platforms (for the versions you plan to use).
            
        - SDK Tools (Build Tools, Platform Tools, Emulator, etc.).
            
    - Once installed, they’re stored locally in `~/Android/Sdk`.
        
4. **Download Plugins Beforehand**
    
    - Any plugins you need (Kotlin, Flutter, etc.) should be installed while online.
        
    - They’ll remain available offline.
        
5. **Use Local Maven Repositories (Optional)**
    
    - If you want to be fully independent, you can mirror Maven repositories locally.
        
    - But for most projects, Gradle’s cache is enough.
        

### ✅ What You Can Do Offline

- Write and edit code.
    
- Build and run apps (using cached Gradle dependencies).
    
- Use the emulator (if system images are pre‑downloaded).
    
- Debug and test locally.
    

### ⚠️ Limitations

- You won’t be able to fetch **new libraries** or update dependencies offline.
    
- If your project references something you haven’t downloaded yet, the build will fail until you reconnect.
    

👉 Since you’re in a rural setup where internet may be unreliable, the best workflow is:

1. Connect once, open your project, run a full build.
    
2. Install all SDKs and tools you think you’ll need.
    
3. Switch Gradle to offline mode.
    

That way, you can keep coding and testing even without internet.

Would you like me to show you a **step‑by‑step offline workflow example** (e.g., setting up a new Kotlin app, caching dependencies, and running it offline) so you can try it immediately?



### 🛠 Step‑by‑Step Offline Setup

#### 1. Create a New Project

- Open Android Studio → **New Project** → pick “Empty Activity” (or any template).
    
- Give it a name, package, and save location.
    
- Finish setup — now you have a clean project.
    

#### 2. Add Dependencies You’ll Need

Open your project’s `app/build.gradle` and add libraries you want (e.g., Hilt):



```gradle
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
    id 'com.google.dagger.hilt.android' version '2.51.1' apply false
}

android {
    namespace "com.example.offlineproject"
    compileSdk 34

    defaultConfig {
        applicationId "com.example.offlineproject"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }
}

dependencies {
    implementation "androidx.core:core-ktx:1.12.0"
    implementation "androidx.appcompat:appcompat:1.6.1"
    implementation "com.google.dagger:hilt-android:2.51.1"
    kapt "com.google.dagger:hilt-compiler:2.51.1"
}
```

_(You can add Retrofit, Room, Glide, etc. here too — the key is to declare everything you’ll need before going offline.)_

#### 3. Sync Gradle Online Once

- While connected to the internet, click **Sync Project with Gradle Files**.
    
- Or run in terminal:
    
    bash
    
    ```
    ./gradlew build
    ```
    
- This downloads all declared dependencies and caches them in `~/.gradle/caches`.
    

#### 4. Enable Offline Mode

- Go to **File → Settings → Build, Execution, Deployment → Gradle**.
    
- Check **“Offline work”**.
    
- Now Gradle will use cached dependencies instead of trying to fetch online.
    

#### 5. Pre‑download SDKs & Tools

- Open **Tools → SDK Manager**.
    
- Install:
    
    - Android SDK Platforms (for the versions you’ll use).
        
    - SDK Tools (Build Tools, Platform Tools, Emulator system images).
        
- Once installed, they’re stored locally in `~/Android/Sdk`.
    

#### 6. Verify Offline Build

- Disconnect from the internet.
    
- Run:
    
    bash
    
    ```
    ./gradlew assembleDebug
    ```
    
- If everything was cached, the build will succeed offline.
    
- You can now code, build, and run without internet.
    

### ✅ What This Achieves

- All external dependencies (like Dagger Hilt) are cached locally.
    
- SDKs and tools are installed offline.
    
- Gradle won’t try to fetch new libraries.
    
- You can continue development offline unless you add new dependencies later.