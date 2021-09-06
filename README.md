# KivyGradient
KivyGradient allows you to add a gradient color to your Kivy Widget


### Example Code

```python
from kivy.app import App
from kivy.lang import Builder


kv = """
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import Gradient kivy_gradient.Gradient
RelativeLayout:
    BoxLayout
        id: box
        on_kv_post: print(get_color_from_hex("E91E63"))
        canvas:
            Rectangle:
                size: self.size
                pos: self.pos
                texture: Gradient.horizontal(get_color_from_hex("E91E63"), get_color_from_hex("FCE4EC"))
"""


class Test(App):
    def build(self):
        return Builder.load_string(kv)

    def on_stop(self):
        self.root.ids.box.export_to_png("gradient.png")
        

Test().run()
```
![gradient](https://user-images.githubusercontent.com/42192162/132244508-113ea626-371f-486f-9702-fdea0f4214a7.png)


```python
from kivy.app import App
from kivy.lang import Builder


kv = """
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import Gradient test.Gradient
RelativeLayout:
    BoxLayout
        id: box
        canvas:
            Rectangle:
                size: self.size
                pos: self.pos
                texture: 
                    Gradient.horizontal(
                    get_color_from_hex("E91E63"), 
                    get_color_from_hex("FCE4EC"), 
                    get_color_from_hex("2962FF")
                    )
"""


class Test(App):
    def build(self):
        return Builder.load_string(kv)

    def on_stop(self):
        self.root.ids.box.export_to_png("gradient.png")
        

Test().run()

```