from os import path, listdir
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from app.folderpicker import FolderPicker
from app.models.action import Action
import app.models.color as color
from app.services.persistence import Persistence

class ImageViewer(BoxLayout):
    def __init__(self, **kwargs):
        super(ImageViewer, self).__init__(orientation='horizontal', **kwargs)
        Window.maximize()

        self.actions = {}
        self.selected_folder:str = None
        self.image_files:list[str] = []
        self.current_image_index:int = 0

        # Creating a FolderPicker
        self.folder_picker_layout = FolderPicker(on_folder_selected=self.on_folder_selected)
        self.add_widget(self.folder_picker_layout)
        Window.bind(on_key_down=self.keyboard_on_key_down)

    def on_folder_selected(self, folder_path):
        self.selected_folder = folder_path
        print('Selected folder:', self.selected_folder)

        self.image_files = [f for f in listdir(self.selected_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        self.persistence = Persistence('.picii.pkl', self.selected_folder)

        if self.image_files:
            self.show_image_viewer()
            self.load_persisted_actions()
        else:
            print('No image files found in the selected folder.')

    def load_persisted_actions(self):
        db_actions = self.persistence.load()
        if not db_actions:
            return
        self.actions = db_actions
        print('Loaded actions:', self.actions)
        for index, image in enumerate(self.image_files):
            if image in self.actions:
                if self.actions[image] == Action.DELETE.value:
                    # change the image color to red
                    self.gallery_layout.children[len(self.gallery_layout.children) - index - 1].background_color = color.BTN_DELETE
                elif self.actions[image] == Action.FAVOURITE.value:
                    # change the image color to green
                    self.gallery_layout.children[len(self.gallery_layout.children) - index - 1].background_color = color.BTN_FAVOURITE

    def show_image_viewer(self):

        def abbreviate_name(name, max_length=22):
            if len(name) <= max_length:
                return name
            else:
                # Extract the file extension
                base_name, extension = path.splitext(name)
                
                # Abbreviate and append the extension
                abbreviated_name = base_name[:max_length - len(extension)] + "..." + extension
                return abbreviated_name
            
        # Remove folder picker widget
        self.remove_widget(self.folder_picker_layout)

        # Create a ScrollView to make the gallery_layout scrollable
        scroll_view = ScrollView(size_hint_x=None, width=200)
        self.gallery_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        
        for index, image_file in enumerate(self.image_files):
            image = Button(text= abbreviate_name(image_file), size_hint_y=None, height=40, halign='left', text_size=(180, None))
            image.bind(on_press=self.on_image_selected)
            self.gallery_layout.add_widget(image)
            # self.reset_gallery_colors()
            
        self.gallery_layout.children[len(self.gallery_layout.children) - self.current_image_index - 1].background_color = color.BTN_SELECTED

        self.gallery_layout.bind(minimum_height= self.gallery_layout.setter('height'))

        scroll_view.add_widget(self.gallery_layout)

        # Create image viewer layout        
        image_viewer_layout = BoxLayout(orientation='vertical')

        # Adding the image
        self.image_view = Image(source=path.join(self.selected_folder, self.image_files[self.current_image_index]))
        image_viewer_layout.add_widget(self.image_view)

        # Adding the button bar
        button_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        btnDelete = Button(text='Marcar para eliminar', background_color= color.BTN_DELETE)
        btnBack = Button(text='Atras', size_hint_x=0.5)
        btnFavourite = Button(text='Marcar como favorita', background_color= color.BTN_FAVOURITE)
        btnForward = Button(text='Siguiente', size_hint_x=0.5)
        
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

    def go_back(self, instance):
        if self.current_image_index > 0:
            self.change_image(self.current_image_index-1)         

    def go_forward(self, instance):
        if self.current_image_index < len(self.image_files)-1:
            self.change_image(self.current_image_index+1)

    def on_image_selected(self, instance):
        # Get the index of the image selected
        index = len(self.gallery_layout.children) - self.gallery_layout.children.index(instance) - 1
        self.change_image(index)

    def change_image(self, new_index:int):  
        last_image = self.image_files[self.current_image_index]
        last_image_color:color
        if last_image not in self.actions:
            last_image_color = color.BTN_DEFAULT
        else:
            last_image_color = color.BTN_DELETE if self.actions[last_image] == Action.DELETE.value else color.BTN_FAVOURITE
            
        self.gallery_layout.children[len(self.gallery_layout.children) - self.current_image_index - 1].background_color = last_image_color  
        self.current_image_index = new_index
        self.image_view.source = path.join(self.selected_folder, self.image_files[self.current_image_index])
        self.gallery_layout.children[len(self.gallery_layout.children) - self.current_image_index - 1].background_color = color.BTN_SELECTED   

    def mark_for_deleting(self, instance):
        self.add_action_to_image(self.image_files[self.current_image_index], Action.DELETE)
        self.go_forward(instance)
        self.persistence.save(self.actions)

    def mark_as_favourite(self, instance):
        self.add_action_to_image(self.image_files[self.current_image_index], Action.FAVOURITE)
        self.go_forward(instance)
        self.persistence.save(self.actions)

    def add_action_to_image(self, image:str, action:Action):
        if image in self.actions and self.actions[image] == action.value:
            del self.actions[image]
        else:
            self.actions[image] = action.value

    def keyboard_on_key_down(self, window, key, scancode, codepoint, modifier):
        if key in [273, 63232]:  # UP arrow key
            self.go_back(None)
        elif key in [274, 63233]:  # DOWN arrow key
            self.go_forward(None)
        elif key in [275, 63234]:  # RIGHT arrow key
            self.mark_as_favourite(None)
        elif key in [276, 63235]:  # LEFT arrow key
            self.mark_for_deleting(None)