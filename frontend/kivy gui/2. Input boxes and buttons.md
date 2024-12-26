
### First lets start with the basic overall code

This should get you started with kivy

```python
import kivy
from kivy.app import App
from kivy.uix.label import Label
  
class MyApp(App):
  def build(self):
    return Label(text="Hello, World!")

if __name__ == "__main__":
  MyApp().run()
```


### Now making boxes and buttons


```python
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

  

class MyGridLayout(GridLayout):
  # initialize infinite keywords
  def __init__(self, **kwargs):
    # call gird layout constructor
    super(MyGridLayout, self).__init__(**kwargs)

    # set columns
    self.cols = 2
    
    # add widgets
    self.add_widget(Label(text="Name: "))
    # add input box
    self.name = TextInput(multiline=False)
    self.add_widget(self.name)

    # add widgets
    self.add_widget(Label(text="Favorite Pizza: "))
    # add input box
    self.pizza = TextInput(multiline=False)
    self.add_widget(self.pizza)

     # add widgets
    self.add_widget(Label(text="Favorite color: "))
    # add input box
    self.color = TextInput(multiline=False)
    self.add_widget(self.color)

    # create a submit button
    self.submit = Button(text="Submit", font_size=32)
    # bind the button
    self.submit.bind(on_press=self.press)
    self.add_widget(self.submit)

  # button event, called when submit is pressed
  def press(self, instance):
    # it takes the input from the input boxes
    name = self.name.text
    pizza = self.pizza.text
    color = self.color.text

    self.add_widget(Label(text=f"hello {name}, your favorite pizza is {pizza} and your favorite color is {color}"))

    # clear the input boxes
    self.name.text = ""
    self.pizza.text = ""
    self.color.text = ""

  
class MyApp(App):
  def build(self):
    return MyGridLayout()
  

if __name__ == "__main__":
  MyApp().run()
```