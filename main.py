from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import subprocess

class FolderPathInput(BoxLayout):
    def __init__(self, **kwargs):
        super(FolderPathInput, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.add_widget(Label(text='Input Folder Path:'))
        self.input_path = TextInput(multiline=False)
        self.add_widget(self.input_path)
        
        self.add_widget(Label(text='Output Folder Path:'))
        self.output_path = TextInput(multiline=False)
        self.add_widget(self.output_path)
        
        self.run_button = Button(text='Run Process')
        self.run_button.bind(on_press=self.run_process)
        self.add_widget(self.run_button)

    def run_process(self, instance):
        input_path = self.input_path.text
        output_path = self.output_path.text
        subprocess.run(["python", "process.py", input_path, output_path])
        print(f'Running process with input path {input_path} and output path {output_path}')

class ReaderApp(App):
    def build(self):
        return FolderPathInput()

if __name__ == '__main__':
    ReaderApp().run()

