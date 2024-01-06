# folderpicker.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView

class FolderPicker(BoxLayout):
    def __init__(self, on_folder_selected, **kwargs):
        super(FolderPicker, self).__init__(orientation='vertical', **kwargs)
        self.selected_folder = None        

        # Creating a FileChooserIconView
        self.file_chooser = FileChooserIconView()
        self.file_chooser.dirselect = True
        self.file_chooser.bind(selection=self.on_selection)
        self.file_chooser.path = '/home/miguel/'

        # Label to display selected file path
        self.pick_folder_btn = Button(text='Seleccionar carpeta', size_hint_y=None, height=50)
        self.pick_folder_btn.bind(on_press=self.on_pick_folder)

        self.add_widget(self.file_chooser)
        self.add_widget(self.pick_folder_btn)

        self.on_folder_selected = on_folder_selected

    def on_selection(self, instance, selection):
        if selection:
            self.selected_folder = selection[0]

    def on_pick_folder(self, instance):
        if self.selected_folder:
            self.on_folder_selected(self.selected_folder)
