

### Does Firebase Automatically Link Data to an Account?

**No, not automatically.** Firebase Authentication and Firebase Database (Realtime Database or Firestore) are **separate services**. While Firebase Auth gives each user a unique ID (`uid`), **you must manually structure your database to associate data with that UID**.

### 🔐 How to Link User Data to Their Account

When a user signs up or logs in, Firebase gives you access to their `uid`:



```kotlin
val user = FirebaseAuth.getInstance().currentUser
val uid = user?.uid
```

You then use this UID to store and retrieve their data:



```kotlin
val database = FirebaseDatabase.getInstance().reference
database.child("users").child(uid).setValue(userData)
```

This way:

- The data is **tied to the user’s UID**
    
- When the user reinstalls the app and logs in again, you can fetch their data using the same UID
    

📘 Example from Stack Overflow:



```kotlin
val user = FirebaseAuth.getInstance().currentUser
val ref = FirebaseDatabase.getInstance().getReference("users").child(user.uid)
ref.setValue(UserProfile(...))
```

### 🔄 What Happens When the App Is Reinstalled?

If the user logs in again:

- Firebase Auth recognizes them and returns the same `uid`
    
- You can retrieve their data from `/users/{uid}` in your database
    

So yes — **as long as you save data under the user's UID**, it will persist across reinstalls and devices.

### 🔐 Bonus: Secure the Data

Use Firebase Realtime Database rules to ensure only the authenticated user can access their data:



```json
{
  "rules": {
    "users": {
      "$uid": {
        ".read": "$uid === auth.uid",
        ".write": "$uid === auth.uid"
      }
    }
  }
}
```

### 🧠 TL;DR

- Firebase **does not automatically** link Auth and Database — you must do it using the user's `uid`.
    
- Store data under `/users/{uid}` to persist it across sessions and devices.
    
- Use security rules to protect user data.