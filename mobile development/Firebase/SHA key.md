
### 🔑 What Is the SHA-1 Key?

The **SHA-1 key** is a digital fingerprint of your app's signing certificate. Firebase uses it to:

- Verify your app’s identity
    
- Enable features like **Google Sign-In**, **Phone Authentication**, **Dynamic Links**, and **App Invites**
    

### 🤖 Connecting Firebase via Android Studio vs. Firebase Console

|Method|Does it generate SHA-1?|Do you need to manually add it?|Notes|
|---|---|---|---|
|**Android Studio (Assistant Panel)**|✅ Yes (via Gradle `signingReport`)|✅ You still need to **copy-paste** it into Firebase Console|Android Studio helps you get the SHA-1, but doesn’t automatically register it in Firebase|
|**Firebase Console**|❌ No automatic generation|✅ You must **manually enter** the SHA-1|You can add multiple SHA-1s (debug, release, Google Play) manually|

📌 **Bottom line**: Android Studio helps you **generate** the SHA-1, but you still need to **add it manually** to Firebase Console under **Project Settings > Your Apps > Add Fingerprint**2.

### 🛠️ How to Get SHA-1 in Android Studio

1. Open your project in Android Studio.
    
2. Go to the **Gradle** tab (right side).
    
3. Navigate to: `Click on the Execute Gradle task Button` the icon looks like youtube icon/ play icon
    
4. Type in `signingReport` the click Enter
    
5. Look in the **Run** window for your SHA-1 (debug and release).
    

📘 Full guide: How to Get SHA-1 in Android Studio

### 🧩 Pro Tip

If you're using **Google Play App Signing**, Firebase can automatically fetch the SHA-1 from the Play Console when you link your app under **Project Settings > Integrations**