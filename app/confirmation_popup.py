
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class ConfirmationPopup(ModalView):
    def __init__(self, message, yes_label, callback_yes, **kwargs):
        super(ConfirmationPopup, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (300, 140)
        layout = BoxLayout(orientation='vertical')

        label = Label(text=message, halign='center')
        layout.add_widget(label)

        def accept(instance):
            callback_yes()
            self.dismiss()

        button_layout = BoxLayout(spacing=10)
        btn_yes = Button(text=yes_label, on_press=accept, size_hint_y=None, height=50)
        btn_no = Button(text='Cancelar', on_press=self.dismiss, size_hint_y=None, height=50)
        button_layout.add_widget(btn_no)
        button_layout.add_widget(btn_yes)

        layout.add_widget(button_layout)
        self.add_widget(layout)