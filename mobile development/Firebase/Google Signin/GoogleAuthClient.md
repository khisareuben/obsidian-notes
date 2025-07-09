
This is the implementation of the google signin button

Note: There are two ways of writing this, one is you use the `viewmodel` and the other one you don't use a view model so choose between those two but i prefer to use the one with the viewmodel as it is easier to switch to dependecy injection


```kotlin

  
import android.content.Context  
import androidx.credentials.ClearCredentialStateRequest  
import androidx.credentials.CredentialManager  
import androidx.credentials.CustomCredential  
import androidx.credentials.GetCredentialRequest  
import androidx.credentials.GetCredentialResponse  
import com.google.android.libraries.identity.googleid.GetGoogleIdOption  
import com.google.android.libraries.identity.googleid.GoogleIdTokenCredential  
import com.google.android.libraries.identity.googleid.GoogleIdTokenParsingException  
import com.google.firebase.auth.FirebaseAuth  
import com.google.firebase.auth.GoogleAuthProvider  
import kotlinx.coroutines.CancellationException  
import kotlinx.coroutines.tasks.await  
  
class GoogleAuthClient(  
    private val context: Context  
) {  
  
    // Tag used for logging/debugging  
    private val tag = "GoogleSignInClient"  
  
    // CredentialManager handles sign-in credentials (like Google ID tokens)  
    private val credentialManager = CredentialManager.create(context)  
  
    // FirebaseAuth instance to authenticate with Firebase  
    private val firebaseAuth = FirebaseAuth.getInstance()  
  
    // Checks if a user is already signed in to Firebase  
    fun isSignedIn(): Boolean {  
        if (firebaseAuth.currentUser != null) {  
            println(tag + "Already signed In")  
            return true  
        }  
        return false  
    }  
  
    // Initiates the Google sign-in process  
    suspend fun signIn(): Boolean {  
        // If already signed in, skip the process  
        if (isSignedIn()) {  
            return true  
        }  
  
        try {  
            // Build the credential request (Google sign-in options)  
            val result = buildCredentialRequest()  
  
            // Handle the result and sign in to Firebase  
            return handleSignIn(result)  
  
        } catch (e: Exception) {  
            e.printStackTrace()  
  
            // If the coroutine was cancelled, rethrow the exception  
            if (e is CancellationException) throw e  
  
            println(tag + "signIn error: ${e.message}")  
            return false  
        }  
    }  
  
    // Handles the result of the credential request  
    private suspend fun handleSignIn(result: GetCredentialResponse): Boolean {  
        val credential = result.credential  
  
        // Check if the credential is a Google ID token  
        if (  
            credential is CustomCredential &&  
            credential.type == GoogleIdTokenCredential.TYPE_GOOGLE_ID_TOKEN_CREDENTIAL  
        ) {  
            try {  
                // Parse the Google ID token credential  
                val tokenCredential = GoogleIdTokenCredential.createFrom(credential.data)  
  
                // Log some basic user info (optional)  
                println(tag + "name: ${tokenCredential.displayName}")  
                println(tag + "id: ${tokenCredential.id}")  
                println(tag + "profile picture: ${tokenCredential.profilePictureUri}")  
  
                // Create a Firebase credential using the Google ID token  
                val authCredential = GoogleAuthProvider.getCredential(  
                    tokenCredential.idToken, null  
                )  
  
                // Sign in to Firebase with the credential  
                val authResult = firebaseAuth.signInWithCredential(authCredential).await()  
  
                // Return true if the user is successfully signed in  
                return authResult.user != null  
  
            } catch (e: GoogleIdTokenParsingException) {  
                println(tag + "GoogleIdTokenParsingException: ${e.message}")  
                return false  
            }  
  
        } else {  
            // If the credential is not a Google ID token, return false  
            println(tag + "credential is not GoogleIdTokenCredential")  
            return false  
        }  
    }  
  
    // Builds the Google sign-in credential request  
    private suspend fun buildCredentialRequest(): GetCredentialResponse {  
        val request = GetCredentialRequest.Builder()  
            .addCredentialOption(  
                GetGoogleIdOption.Builder()  
                    .setFilterByAuthorizedAccounts(false) // Show all Google accounts, not just previously used ones  
                    .setServerClientId(  
                        "940428057285-anjmnnbjf34qfmel5os4ha3qrjuc8ihr.apps.googleusercontent.com"  
                    ) // Your web client ID from Google Cloud Console  
                    .setAutoSelectEnabled(false) // Don't auto-select an account  
                    .build()  
            )  
            .build()  
  
        // Launch the Google sign-in UI and return the result  
        return credentialManager.getCredential(  
            request = request,  
            context = context  
        )  
    }  
  
    // Signs out the user from both Firebase and the CredentialManager  
    suspend fun signOut() {  
        credentialManager.clearCredentialState(ClearCredentialStateRequest())  
        firebaseAuth.signOut()  
    }  
}

```