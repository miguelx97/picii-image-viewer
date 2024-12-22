import asyncio
from functools import partial
from os import path, listdir, remove, makedirs
from shutil import move
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from app.confirmation_popup import ConfirmationPopup
from app.folderpicker import FolderPicker
from app.models.action import Action
import app.models.color as color
from app.services.persistence import Persistence
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious, ActionButton, ActionGroup
from PIL import Image as PILImage
from PIL.ExifTags import TAGS
import sys

class ImageViewer(BoxLayout):
    def __init__(self, **kwargs):
        super(ImageViewer, self).__init__(orientation='vertical', **kwargs)
        Window.maximize()
        Window.bind(on_key_down=self.keyboard_on_key_down)
        arguments = sys.argv

        self.actions = {}
        self.selected_folder:str = None
        self.image_files:list[str] = []
        self.filtered_images:list[str] = []
        self.current_image_index:int = 0

        # Create ActionBar
        action_bar = ActionBar()
        action_view = ActionView()
        action_previous = ActionPrevious(title='Picii', with_previous=False, app_icon='assets/icon.png', app_icon_width=32, app_icon_height=32)

        action_group_filter = ActionGroup(text='Filtrar Imágenes', mode='spinner')
        action_filter_delete = ActionButton(text='Para eliminar')
        action_filter_favourite = ActionButton(text='Favoritas')
        action_filter_all = ActionButton(text='Todas')

        def show_images(action:Action=None):
            self.load_images_gallery(action)
            self.image_view.source = path.join(self.selected_folder, self.get_images()[self.current_image_index])

        action_filter_delete.bind(on_press=lambda x: show_images(Action.DELETE))
        action_filter_favourite.bind(on_press=lambda x: show_images(Action.FAVOURITE))
        action_filter_all.bind(on_press=lambda x: show_images())

        action_group_filter.add_widget(action_filter_delete)
        action_group_filter.add_widget(action_filter_favourite)
        action_group_filter.add_widget(action_filter_all)

        action_group_actions = ActionGroup(text='Acciones')
        action_action_delete = ActionButton(text='Eliminar imágenes marcadas')
        action_action_favourite = ActionButton(text='Separar imágenes favoritas')

        action_action_delete.bind(on_press=self.delete_marked_images)
        action_action_favourite.bind(on_press=self.separate_favourite_images)

        action_group_actions.add_widget(action_action_delete)
        action_group_actions.add_widget(action_action_favourite)
        
        action_view.add_widget(action_group_actions)
        action_view.add_widget(action_group_filter)
        action_view.add_widget(action_previous)
        action_bar.add_widget(action_view)

        self.app_layout = BoxLayout(orientation='horizontal')        

        self.add_widget(action_bar)
        self.add_widget(self.app_layout)

        # Creating a FolderPicker
        if len(arguments) > 1:
            self.on_folder_selected(arguments[1])
        else:
            self.folder_picker_layout = FolderPicker(on_folder_selected=self.on_folder_selected, arguments=arguments)
            self.app_layout.add_widget(self.folder_picker_layout)
            # self.on_folder_selected('/home/miguel/Pictures/')
    
    def get_images(self):
        return self.filtered_images if self.filtered_images else self.image_files
    
    def nun_images_by_action(self, actionToSearch:Action):
        return len([image for image in self.actions if self.actions[image] == actionToSearch.value])
    
    def get_exif_date(self, image_path):
        try:
            image = PILImage.open(image_path)
            exif_data = image._getexif()
            if exif_data is not None:
                for tag, value in exif_data.items():
                    if TAGS.get(tag) == 'DateTimeOriginal':
                        return value  # Date the photo was taken (DateTimeOriginal)
        except Exception as e:
            print(f"Error reading EXIF data for {image_path}: {e}")
        return None

    def on_folder_selected(self, folder_path):
        self.selected_folder = folder_path
        print('Selected folder:', self.selected_folder)

        self.image_files = [f for f in listdir(self.selected_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        # Sort image paths by EXIF DateTimeOriginal
        self.image_files = sorted(self.image_files, key=lambda f: self.get_exif_date(path.join(self.selected_folder, f)) or "1900:01:01 00:00:00")

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
        self.paint_gallery_items()

    def paint_gallery_items(self):
        for index, image in enumerate(self.get_images()):
            if image in self.actions:
                if self.actions[image] == Action.DELETE.value:
                    # change the image color to red
                    self.gallery_layout.children[len(self.gallery_layout.children) - index - 1].background_color = color.BTN_DELETE
                elif self.actions[image] == Action.FAVOURITE.value:
                    # change the image color to green
                    self.gallery_layout.children[len(self.gallery_layout.children) - index - 1].background_color = color.BTN_FAVOURITE

    def show_image_viewer(self):

        # Remove folder picker widget if it exists
        if self.app_layout.children and self.app_layout.children[0] == self.folder_picker_layout:
            self.app_layout.remove_widget(self.folder_picker_layout)

        # Create a ScrollView to make the gallery_layout scrollable
        scroll_view = ScrollView(size_hint_x=None, width=200)
        self.gallery_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        
        self.load_images_gallery()

        self.gallery_layout.bind(minimum_height= self.gallery_layout.setter('height'))

        scroll_view.add_widget(self.gallery_layout)

        # Create image viewer layout        
        image_viewer_layout = BoxLayout(orientation='vertical')

        # Adding the image
        self.image_view = Image(source=path.join(self.selected_folder, self.get_images()[self.current_image_index]))

        # Adding the top bar
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        btnShowImagesToDelete = Button(text='Imagenes para eliminar')
        btnShowFavouriteImages = Button(text='Imagenes favoritas')

        top_bar.add_widget(btnShowImagesToDelete)
        top_bar.add_widget(btnShowFavouriteImages)

        # Adding the button bar
        button_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        btnDelete = Button(text='Marcar para eliminar', background_color= color.BTN_DELETE)
        btnBack = Button(text='Atras', size_hint_x=0.5)
        btnForward = Button(text='Siguiente', size_hint_x=0.5)
        btnFavourite = Button(text='Marcar como favorita', background_color= color.BTN_FAVOURITE)
        
        btnDelete.bind(on_press=self.mark_for_deleting)
        btnBack.bind(on_press=self.go_back)
        btnForward.bind(on_press=self.go_forward)
        btnFavourite.bind(on_press=self.mark_as_favourite)

        button_bar.add_widget(btnDelete)
        button_bar.add_widget(btnBack)
        button_bar.add_widget(btnForward)
        button_bar.add_widget(btnFavourite)

        # image_viewer_layout.add_widget(top_bar)
        image_viewer_layout.add_widget(self.image_view)
        image_viewer_layout.add_widget(button_bar)

        self.app_layout.add_widget(scroll_view)
        self.app_layout.add_widget(image_viewer_layout)

    def load_images_gallery(self, filter:Action=None):

        if filter == Action.DELETE and self.nun_images_by_action(Action.DELETE) == 0:
            return
        elif filter == Action.FAVOURITE and self.nun_images_by_action(Action.FAVOURITE) == 0:
            return

        self.gallery_layout.clear_widgets()
        def abbreviate_name(name, max_length=20):
            if len(name) <= max_length:
                return name
            else:
                # Extract the file extension
                base_name, extension = path.splitext(name)
                
                # Abbreviate and append the extension
                abbreviated_name = base_name[:max_length - len(extension)] + "..." + extension
                return abbreviated_name
            
        if filter == Action.DELETE:
            self.filtered_images = [image for image in self.get_images() if image in self.actions and self.actions[image] == Action.DELETE.value]
        elif filter == Action.FAVOURITE:
            self.filtered_images = [image for image in self.get_images() if image in self.actions and self.actions[image] == Action.FAVOURITE.value]
        else:
            self.filtered_images = []
            
        for image_file in self.get_images():
            image = Button(text= abbreviate_name(image_file), size_hint_y=None, height=40, halign='left', text_size=(180, None))
            image.bind(on_press=self.on_image_selected)
            self.gallery_layout.add_widget(image)
        
        self.paint_gallery_items()
        self.current_image_index = 0
        self.gallery_layout.children[len(self.gallery_layout.children) - self.current_image_index - 1].background_color = color.BTN_SELECTED

    # ACTIONS

    def go_back(self, instance):
        if self.current_image_index > 0:
            self.change_image(self.current_image_index-1)         

    def go_forward(self, instance):
        if self.current_image_index < len(self.get_images())-1:
            self.change_image(self.current_image_index+1)

    def on_image_selected(self, instance):
        # Get the index of the image selected
        index = len(self.gallery_layout.children) - self.gallery_layout.children.index(instance) - 1
        self.change_image(index)

    async def scroll_to_image_async(self, image_button):
        # Wait for the next frame before scrolling
        await asyncio.sleep(0)
        self.gallery_layout.parent.scroll_to(image_button)

    def change_image(self, new_index:int):  
        last_image = self.get_images()[self.current_image_index]
        last_image_color:color
        if last_image not in self.actions:
            last_image_color = color.BTN_DEFAULT
        else:
            last_image_color = color.BTN_DELETE if self.actions[last_image] == Action.DELETE.value else color.BTN_FAVOURITE
            
        self.gallery_layout.children[len(self.gallery_layout.children) - self.current_image_index - 1].background_color = last_image_color  
        self.current_image_index = new_index
        self.image_view.source = path.join(self.selected_folder, self.get_images()[self.current_image_index])
        self.gallery_layout.children[len(self.gallery_layout.children) - self.current_image_index - 1].background_color = color.BTN_SELECTED   
        # Scroll to the selected image
        image_button = self.gallery_layout.children[len(self.gallery_layout.children) - self.current_image_index - 2]
        self.gallery_layout.parent.scroll_to(image_button)

    def mark_for_deleting(self, instance):
        self.add_action_to_image(self.get_images()[self.current_image_index], Action.DELETE)
        self.go_forward(instance)
        self.persistence.save(self.actions)

    def mark_as_favourite(self, instance):
        self.add_action_to_image(self.get_images()[self.current_image_index], Action.FAVOURITE)
        self.go_forward(instance)
        self.persistence.save(self.actions)

    def add_action_to_image(self, image:str, action:Action):
        if image in self.actions and self.actions[image] == action.value:
            del self.actions[image]
        else:
            self.actions[image] = action.value

    def delete_marked_images(self, instance):
        count_to_delete = self.nun_images_by_action(Action.DELETE)
        if count_to_delete == 0:
            return
        confirmation_message = f'¿Eliminar {count_to_delete} imágenes?'
        confirmation_popup = ConfirmationPopup(message=confirmation_message, yes_label='Eliminar', callback_yes=self.perform_delete)
        confirmation_popup.open()

    def perform_delete(self):
        for image in self.actions:
            if self.actions[image] == Action.DELETE.value:
                print('Deleting image:', image)
                remove(path.join(self.selected_folder, image))
        self.actions = {image: action for image, action in self.actions.items() if action != Action.DELETE.value}
        self.reload_images()
        self.persistence.save(self.actions)

    def separate_favourite_images(self, instance):
        count_to_favourite = self.nun_images_by_action(Action.FAVOURITE)
        if count_to_favourite == 0:
            return
        confirmation_message = f'¿Separar {count_to_favourite} imágenes favoritas?'
        confirmation_popup = ConfirmationPopup(message=confirmation_message, yes_label='Separar', callback_yes=self.perform_separate_favourite_images)
        confirmation_popup.open()

    def perform_separate_favourite_images(self):
        fav_images_folder = path.join(self.selected_folder, "Mejores")
        makedirs(fav_images_folder, exist_ok=True)
        for image in self.actions:
            if self.actions[image] == Action.FAVOURITE.value:
                print('Separating image:', image, 'to', fav_images_folder)
                image_path = path.join(self.selected_folder, image)
                new_image_path = path.join(fav_images_folder, image)
                move(image_path, new_image_path)

        self.actions = {image: action for image, action in self.actions.items() if action != Action.FAVOURITE.value}
        self.reload_images()
        self.persistence.save(self.actions)

    def reload_images(self):
        self.image_files = [f for f in listdir(self.selected_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        self.load_images_gallery()

    # KEYBOARD EVENTS

    def keyboard_on_key_down(self, window, key, scancode, codepoint, modifier):
        if key in [273, 63232]:  # UP arrow key
            self.go_back(None)
        elif key in [274, 63233]:  # DOWN arrow key
            self.go_forward(None)
        elif key in [275, 63234]:  # RIGHT arrow key
            self.mark_as_favourite(None)
        elif key in [276, 63235]:  # LEFT arrow key
            self.mark_for_deleting(None)
