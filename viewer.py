# viewer.py
import os
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView

class ImageViewer(BoxLayout):
    def __init__(self, **kwargs):
        super(ImageViewer, self).__init__(orientation='vertical', **kwargs)
        self.selected_folder = None
        self.image_files = []

        self.folderPickerLayout = BoxLayout(orientation='vertical')

        # Creating a FileChooserIconView
        self.file_chooser = FileChooserIconView()
        self.file_chooser.dirselect = True
        self.file_chooser.bind(selection=self.on_selection)

        # Label to display selected file path
        pickFolderBtn = Button(text='Seleccionar carpeta', size_hint_y=None, height=50)
        pickFolderBtn.bind(on_press=self.on_pick_folder)

        self.folderPickerLayout.add_widget(self.file_chooser)
        self.folderPickerLayout.add_widget(pickFolderBtn)

        self.add_widget(self.folderPickerLayout)

    def on_selection(self, instance, selection):
        if selection:
            self.selected_folder = selection[0]
            print('Selected folder:', self.selected_folder)

    def on_pick_folder(self, instance):
        if self.selected_folder:
            self.image_files = [f for f in os.listdir(self.selected_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

            if self.image_files:
                self.show_image_viewer()
            else:
                print('No image files found in the selected folder.')

    def show_image_viewer(self):
        # Remove folder selector widgets
        self.remove_widget(self.folderPickerLayout)

        # Create image viewer layout
        image_viewer_layout = BoxLayout(orientation='vertical')

        # Adding the image
        self.image = Image(source=os.path.join(self.selected_folder, self.image_files[0]))
        image_viewer_layout.add_widget(self.image)

        # Adding the button bar
        button_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        btnDelete = Button(text='Marcar para eliminar')
        btnDelete.bind(on_press=self.mark_for_deleting)
        btnKeep = Button(text='Conservar')
        btnKeep.bind(on_press=self.mark_for_keeping)
        btnFavourite = Button(text='Marcar como favorita')
        btnFavourite.bind(on_press=self.mark_as_favourite)

        button_bar.add_widget(btnDelete)
        button_bar.add_widget(btnKeep)
        button_bar.add_widget(btnFavourite)

        image_viewer_layout.add_widget(button_bar)

        self.add_widget(image_viewer_layout)

    def mark_for_deleting(self, instance):
        print('The button <%s> is being pressed' % instance.text)

    def mark_for_keeping(self, instance):
        print('The button <%s> is being pressed' % instance.text)

    def mark_as_favourite(self, instance):
        print('The button <%s> is being pressed' % instance.text)
