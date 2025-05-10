

Jetpack Compose apps tend to be larger due to the additional dependencies and runtime components they bring in. But there are ways to trim down the size:

1. **Enable ProGuard & R8** – Minify your app by enabling `minifyEnabled true` and `shrinkResources true` in your `build.gradle` file. This removes unused code and resources.
    
2. **Use Only Necessary Dependencies** – Avoid unnecessary libraries. Some Compose dependencies, like `ui-tooling`, should be used only in debug builds (`debugImplementation` instead of `implementation`).
    
3. **Optimize Image Assets** – Use vector drawables instead of large PNGs or JPEGs. Also, consider WebP format for better compression.
    
4. **Reduce Font & Resource Usage** – If you're using custom fonts or large resource files, ensure they are optimized.
    
5. **Use App Bundles Instead of APKs** – `.aab` files allow Play Store to deliver optimized versions of your app based on the user's device.
    
6. **Remove Unused Compose Features** – Some Compose components bring in extra dependencies. If you're not using animations or certain UI elements, exclude them.
    

You can check out more details here and here. If you want, I can help you analyze your specific setup to see where the bulk of the size is coming from!