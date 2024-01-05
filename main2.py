from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class Main(App):
    def build(self):
        # Creating a BoxLayout to hold the image, buttons, and label vertically
        layout = BoxLayout(orientation='vertical')

        # Adding the image
        image = Image(source='img.jpg')  # Replace 'your_image_file.png' with the actual image file
        layout.add_widget(image)

        # Adding the button bar
        button_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        btnDelete = Button(text='Marcar para eliminar')
        btnDelete.bind(on_press=self.markForDeleting)
        btnKeep = Button(text='Conservar')
        btnKeep.bind(on_press=self.markForKeeping)
        btnFavourite = Button(text='Marcar como favorita')
        btnFavourite.bind(on_press=self.markAsFavourite)


        button_bar.add_widget(btnDelete)
        button_bar.add_widget(btnKeep)
        button_bar.add_widget(btnFavourite)

        layout.add_widget(button_bar)

        return layout
    
    def markForDeleting(self, instance):
        print('The button <%s> is being pressed' % instance.text)

    def markForKeeping(self, instance):
        print('The button <%s> is being pressed' % instance.text)

    def markAsFavourite(self, instance):
        print('The button <%s> is being pressed' % instance.text)
        

if __name__ == '__main__':
    Main().run()
