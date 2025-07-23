

## 1. **Use App Bundles (.aab) Instead of APKs**

- **Why it works**: App Bundles allow Google Play to serve device-specific APKs, stripping unused resources.
    
- **Result**: Often cuts size by **20–40%** for installed apps.
    
- ✅ Enable in `build.gradle`:
    
    
    
    ```groovy
    android {
        bundle {
            language {
                enableSplit = true
            }
            density {
                enableSplit = true
            }
            abi {
                enableSplit = true
            }
        }
    }
    ```
    

## 🧽 2. **Enable Code Shrinking with R8**

- **Why it works**: Removes unused code/classes and obfuscates others.
    
- ✅ In `build.gradle`:
    
    
    
    ```groovy
    buildTypes {
        release {
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    ```
    
- Start with default rules, then refine based on what you actually use.
    
- Works especially well if your app uses libraries like Retrofit, Coil, Firebase, etc.
    

## 🧩 3. **Remove Unused Resources**

- Delete unused drawables, layouts, and raw assets.
    
- ✅ Use the **Lint** tool or Android Studio’s "Analyze → Inspect Code" to spot dead resources.
    

## 📦 4. **Limit Bundled Libraries**

Some common culprits:

- Coil brings in OkHttp and ImageDecoder—disable GIFs if unused.
    
- Firebase SDKs can balloon size—choose only the specific modules you need.
    
- Avoid large UI kits or debug libraries in release builds.
    

## 🔥 5. **Compress Images Efficiently**

- Convert PNGs to WebP or use vector drawables.
    
- Run `pngcrush` or `optipng` over all assets.
    
- ✅ For image-heavy apps, consider **Cloudinary** or similar services to offload weight.
    

## 📁 Bonus Tip: Check `.apk` Contents Directly

Use the Android command-line:



```bash
apk analyzer your_app.apk
```

Or inside Android Studio: Build → Analyze APK Helps you pinpoint **which files are eating space**.

## 🧠 Real Talk

Even small Compose apps hit 30+ MB if R8 isn’t enabled or resources aren’t cleaned. Big apps like Kotatsu are lean because they:

- Split assets intelligently,
    
- Avoid wasteful libraries,
    
- Use R8 aggressively,
    
- Offload heavy media (like images or audio).