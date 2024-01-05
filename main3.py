import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.button import Button

class FileChooserApp(App):

    selected_folder = None

    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Create a FileChooserIconView
        file_chooser = FileChooserIconView()
        file_chooser.dirselect = True # Allow folder selection instead of file selection
        file_chooser.bind(selection=self.on_selection)

        # Label to display selected file path
        pickFolder = Button(text='Seleccionar carpeta', size_hint_y=None, height=50)
        pickFolder.bind(on_press=self.onPickFolder)

        layout.add_widget(file_chooser)
        layout.add_widget(pickFolder)

        return layout

    def on_selection(self, instance, selection):
        if selection:
            self.selected_folder = selection[0]

            print('Selected folder:', self.selected_folder)

    def onPickFolder(self, instance):
        if self.selected_folder:
            image_files = [f for f in os.listdir(self.selected_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            print('Image files in the selected folder:', image_files)

if __name__ == '__main__':
    FileChooserApp().run()