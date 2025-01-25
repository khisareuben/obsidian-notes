
```kotlin
class MainActivity : ComponentActivity() {  
  override fun onCreate(savedInstanceState: Bundle?) {  
    super.onCreate(savedInstanceState)  
    enableEdgeToEdge()  
    setContent {  
  
      DefaultPreview()  
  
    }  
  }  
}  
  
@Composable  
fun CustomText(text: String) {  
  Text(  
    text = text,  
    fontSize = 30.sp,  
    fontWeight = FontWeight.Bold  
  )  
}  
  
@Preview(  
  showBackground = true,  
  showSystemUi = true,  
  device = "id:pixel_4",  
  uiMode = Configuration.UI_MODE_NIGHT_YES )  
@Composable  
fun DefaultPreview() {  
  CustomText(text = "life is hard")  
}
```