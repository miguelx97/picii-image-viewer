# viewer.py
import os
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from app.folderpicker import FolderPicker

class ImageViewer(BoxLayout):
    def __init__(self, **kwargs):
        super(ImageViewer, self).__init__(orientation='horizontal', **kwargs)
        self.selected_folder = None
        self.image_files = []
        self.current_image_index = 0

        # Creating a FolderPicker
        self.folder_picker_layout = FolderPicker(on_folder_selected=self.on_folder_selected)
        self.add_widget(self.folder_picker_layout)

    def on_folder_selected(self, folder_path):
        self.selected_folder = folder_path
        print('Selected folder:', self.selected_folder)

        self.image_files = [f for f in os.listdir(self.selected_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if self.image_files:
            self.show_image_viewer()
        else:
            print('No image files found in the selected folder.')

    def reset_gallery_colors(self):
        # gallery_layout = self.children[0].children[0]  # Assuming the structure remains the same
        for index, image_button in enumerate(self.gallery_layout.children):
            image_button.background_color = (1, 1, 1, 1)  # Reset to default color

        # Highlight the currently displayed image in a different color
        self.gallery_layout.children[len(self.gallery_layout.children) - self.current_image_index - 1].background_color = (1, 1, 2, 1)

    def show_image_viewer(self):

        def abbreviate_name(name, max_length=25):
            if len(name) <= max_length:
                return name
            else:
                # Extract the file extension
                base_name, extension = os.path.splitext(name)
                
                # Abbreviate and append the extension
                abbreviated_name = base_name[:max_length - len(extension)] + "..." + extension
                return abbreviated_name
            
        # Remove folder picker widget
        self.remove_widget(self.folder_picker_layout)

        # Create a ScrollView to make the gallery_layout scrollable
        scroll_view = ScrollView(size_hint_x=None, width=200)
        self.gallery_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        
        for index, image_file in enumerate(self.image_files):
            # Check if the current image index matches the position in the list
            is_current_image = index == self.current_image_index

            # Set background color based on whether it's the current image
            button_background_color = (1, 1, 2, 1) if is_current_image else (1, 1, 1, 1)

            image = Button(text= abbreviate_name(image_file), size_hint_y=None, height=40, halign='left', text_size=(180, None), background_color=button_background_color)
            image.bind(on_press=self.on_image_selected)
            self.gallery_layout.add_widget(image)

        self.gallery_layout.bind(minimum_height= self.gallery_layout.setter('height'))

        scroll_view.add_widget(self.gallery_layout)

        # Create image viewer layout        
        image_viewer_layout = BoxLayout(orientation='vertical')

        # Adding the image
        self.image = Image(source=os.path.join(self.selected_folder, self.image_files[self.current_image_index]))
        image_viewer_layout.add_widget(self.image)

        # Adding the button bar
        button_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        btnDelete = Button(text='Marcar para eliminar', background_color=(1, 0, 0, 1))
        btnBack = Button(text='Atras', size_hint_x=0.5)
        btnForward = Button(text='Siguiente', size_hint_x=0.5)
        btnFavourite = Button(text='Marcar como favorita', background_color=(0, 1, 0, 1))
        
        btnDelete.bind(on_press=self.mark_for_deleting)
        btnBack.bind(on_press=self.go_back)
        btnForward.bind(on_press=self.go_forward)
        btnFavourite.bind(on_press=self.mark_as_favourite)

        button_bar.add_widget(btnDelete)
        button_bar.add_widget(btnBack)
        button_bar.add_widget(btnForward)
        button_bar.add_widget(btnFavourite)

        image_viewer_layout.add_widget(button_bar)

        self.add_widget(scroll_view)
        self.add_widget(image_viewer_layout)

    def mark_for_deleting(self, instance):
        print('The button <%s> is being pressed' % instance.text)

    def go_back(self, instance):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.image.source = os.path.join(self.selected_folder, self.image_files[self.current_image_index])
            self.reset_gallery_colors()

    def go_forward(self, instance):
        if self.current_image_index < len(self.image_files)-1:
            self.current_image_index += 1
            self.image.source = os.path.join(self.selected_folder, self.image_files[self.current_image_index])
            self.reset_gallery_colors()
        

    def mark_as_favourite(self, instance):
        print('The button <%s> is being pressed' % instance.text)


    def on_image_selected(self, instance):
        # Get the index of the image selected
        index = len(self.gallery_layout.children) - self.gallery_layout.children.index(instance) - 1

        # Update the image viewer with the selected image
        self.current_image_index = index
        self.image.source = os.path.join(self.selected_folder, self.image_files[self.current_image_index])

        # Reset the colors of the gallery images
        self.reset_gallery_colors()
