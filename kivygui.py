'''***********************************************************
This is the GUI to the Diversity application written by 
Patrick Gourley to run diversity calculations on survey
monkey csv inputs.
***********************************************************'''

#Imports
import os
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
import cvsimport
import outputter
from xlwt import *
import getpass
import itertools
from datetime import datetime
import datetime
from time import sleep
import math


#Classes
class CustomDropDown(DropDown):
    pass

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    
class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

'''***********************************************************
The main screen class
***********************************************************'''
class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    mainlabel = ObjectProperty(None)
    most_least_label = ObjectProperty(None)
    num_label = ObjectProperty(None)
    dd_btn = ObjectProperty(None)
    upload = ObjectProperty(None)
    top_layout = ObjectProperty(None)
    time_text = ObjectProperty(None)
    filepath = []
    filename = []
    number = 0
    output = []
    location = []
    options = 0
    big_or_small = True
    wb = Workbook()
    pb = ProgressBar()
    a = 0
 
    '''***********************************************************
    The function to create a dropdown menu of numbers ranging
    from 5 - however many participants are in the survey
    ***********************************************************'''    
    def drop_down(self):
        self.drop_down = CustomDropDown()
        dropdown = DropDown()
        notes = [i for i in range(1,(self.number)+1)]
        for note in notes:
            self.options+=1
            btn = Button(text='%r' % note, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: (dropdown.select(btn.text), Root.groupSize(self, int(btn.text))))
            dropdown.add_widget(btn)
        self.dd_btn.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(self.dd_btn, 'text', x))
        self.dd_btn.text = (str(self.number) + " (Default)")
    
    '''********************
    Close the popup widget
    ********************'''        
    def dismiss_popup(self):
        self._popup.dismiss()
    '''***********************
    Open the load file widget
    ***********************'''      
    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    '''********************
    Load the selected file
    ********************'''      
    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.a = cvsimport.get_num_people(filename[0])
            l = list(filename[0])
            nameofile = ''
            for i in reversed(l):
                if i == '/':
                    break
                else:
                    nameofile += (i)          
            self.mainlabel.text = ("File: " + nameofile[::-1] + "  | Sample Size: " + str(self.a))
            self.mainlabel.font_size = '16sp'
        self.dismiss_popup()
        self.filepath.append(filename[0])
        self.groupSize(self.a)
        self.drop_down()
        self.upload.disabled = True      
        
    '''********************
    Estimate running time
    ********************'''        
    def estimate(self, n, r):
        f = math.factorial
        return f(n) // f(r) // f(n-r)        

    '''******************************
    Return the number of participants
    ******************************'''      
    def groupSize(self, number):
        self.number = int(number)
        self.num_label.text = ("Calculate for groups size of: " + str(number))
        total_time = (self.estimate(self.a, self.number))     
        self.time_text.text = ("Estimated Time: " + str(datetime.timedelta(seconds=(0.000652945187375 * total_time))))
        
    '''****************************
    Toggle most/least diverse first
    ****************************'''      
    def toggle_order(self):
        if self.big_or_small == True:
            self.big_or_small = False
            self.most_least_label.text = ("Currently Set To Least Diverse First")
        elif self.big_or_small == False:
            self.big_or_small = True
            self.most_least_label.text = ("Currently Set To Most Diverse First")
    
    '''*************************************************
    Run the outputter function to create the excel file
    **************************************************'''          
    def get_print(self, filepath, big_or_small, number):     
        self.output = ((cvsimport.get_num_people(self.filepath[0], self.number, self.big_or_small)))
        outputter.get_print(self.output, self.big_or_small, self.number, self.filepath) 
        
        

class KivyGui(App):
    pass

if __name__ == '__main__':
    KivyGui().run() 
