## ⚙️ Step 1: Enable R8 Shrinking and Resource Trimming

This is **non-negotiable**. Without this, unused classes, methods, and resources all stay in your `.apk`.

### ✅ What to do in `build.gradle` (app module):



```kotlin
buildTypes {
    release {
        minifyEnabled true
        shrinkResources true
        proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
    }
}
```

- `minifyEnabled`: activates **R8** code shrinking
    
- `shrinkResources`: removes unused XML layouts, drawables, etc.
    

### 🧠 Why it works:

R8 will aggressively remove dead code, and if you combine it with sensible ProGuard rules, you’ll see **10–50% reduction** depending on your library usage.

## ✂️ Step 2: Audit and Prune Dependencies

Every library adds weight—even small ones. Ask:

- Do I really need this debug-only library in release?
    
- Are some transitive dependencies bloating the build?
    

### ✅ What to do:

- Open `build.gradle` and delete unused libraries.
    
- Use `./gradlew app:dependencies` to see what's getting bundled.
    
- Prefer single-purpose libraries (like Coil over Glide if you're not doing advanced GIF decoding).
    

## 🧹 Step 3: Strip Unused Resources

Even default icons, layouts, colors, and strings can add bulk if unused.

### ✅ How:

- Run **Android Studio → Analyze → Inspect Code**
    
- Sort by unused resources and delete them.
    
- Especially check:
    
    - Drawables (especially mipmaps for old devices)
        
    - Raw assets (audio, fonts, etc.)
        
    - XML animations you don’t use
        

## 🖼️ Step 4: Compress Your Images

Images silently hog space. Convert and optimize:

### ✅ Action Plan:

- Convert PNGs to **WebP** (lossless or lossy)
    
- Use **vector drawables** for simple icons
    
- Run tools like:
    
    
    
    ```bash
    optipng your_image.png
    pngcrush your_image.png
    ```
    
- You can also use TinyPNG for a drag-and-drop solution.
    

## 🔐 Step 5: Obfuscate Aggressively with ProGuard

ProGuard helps shrink size by renaming classes, stripping metadata, and removing unused features.

### ✅ Basic Rules:

You already have:



```groovy
proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
```

Now customize `proguard-rules.pro`:



```pro
# Keep Retrofit interfaces
-keep interface com.yourapp.network.** { *; }

# Keep Room entities
-keep class com.yourapp.model.** { *; }

# Keep ViewModels
-keep class com.yourapp.viewmodel.** { *; }

# Optional: Obfuscate Coil or Retrofit if needed
-dontwarn okhttp3.**
```

You don't need hundreds of rules. Just preserve your important app architecture and let R8 strip the rest.

## 🧪 Step 6: Analyze the Final `.apk`

To see what's still inside:

### ✅ Use:

- **Android Studio** → Build → Analyze APK
    
- Or command-line:
    
    
    
    ```bash
    ./gradlew assembleRelease
    ./apktool d app-release.apk
    ```
    

This lets you inspect:

- Which classes take up the most space
    
- Which drawables/fonts are still bundled
    
- Whether Kotlin or Compose internals are bloating things