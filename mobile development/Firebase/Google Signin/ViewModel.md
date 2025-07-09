
you can us the google auth client or you can choose to use the ViewModel

```kotlin
  
import android.app.Application  
import androidx.lifecycle.AndroidViewModel  
import androidx.lifecycle.ViewModel  
import androidx.lifecycle.viewModelScope  
import kotlinx.coroutines.flow.MutableStateFlow  
import kotlinx.coroutines.flow.StateFlow  
import kotlinx.coroutines.flow.asStateFlow  
import kotlinx.coroutines.launch  
  
class GoogleAuthViewModel(  
    private val googleAuthClient: GoogleAuthClient  
) : ViewModel() {  
  
    private val _signInState = MutableStateFlow<SignInResult>(SignInResult.Idle)  
    val signInState: StateFlow<SignInResult> = _signInState.asStateFlow()  
  
    fun signIn() {  
        viewModelScope.launch {  
            _signInState.value = SignInResult.Loading  
            try {  
                val success = googleAuthClient.signIn()  
                _signInState.value = if (success) SignInResult.Success else SignInResult.Failure("Google Sign-In failed")  
            } catch (e: Exception) {  
                _signInState.value = SignInResult.Failure(e.message ?: "Unknown error")  
            }  
        }  
    }  
  
    fun resetState() {  
        _signInState.value = SignInResult.Idle  
    }  
  
    fun signOut() {  
        viewModelScope.launch {  
            googleAuthClient.signOut()  
        }  
    }  
}  
  
// Represents the state of the sign-in process  
sealed class SignInResult {  
    object Idle : SignInResult()  
    object Loading : SignInResult()  
    object Success : SignInResult()  
    data class Failure(val message: String) : SignInResult()  
}

```