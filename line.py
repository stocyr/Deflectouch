from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.graphics.texture import Texture
from kivy.core.image import Image


class MyPaintWidget(Widget):
    def on_touch_down(self, touch):
        texture = Image('5x5.png').texture
        with self.canvas:
            Line(points=(0, 0, touch.x, touch.y), texture=texture)


class MyPaintApp(App):
    def build(self):
        return MyPaintWidget()


if __name__ == '__main__':
    MyPaintApp().run()