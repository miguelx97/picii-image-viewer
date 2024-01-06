# main.py
from kivy.app import App
from app.viewer import ImageViewer

class ImageViewerApp(App):
    def build(self):
        return ImageViewer()

if __name__ == '__main__':
    ImageViewerApp().run()
