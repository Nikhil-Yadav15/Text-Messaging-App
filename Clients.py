from kivy.config import  Config
Config.set('graphics', 'minimum_width', '800')
Config.set('graphics', 'minimum_height', '600')
from kivymd.uix.menu import MDDropdownMenu
import datetime
import socket
import ast
import threading
from kivy.animation import Animation
####################
import math
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDRectangleFlatIconButton
from kivymd.uix.card import MDCard
from kivy.metrics import dp, sp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivymd.uix.textfield import MDTextField, MDTextFieldRound
SIZE = 10
# #######################################################################################################################################
Kv = '''
<MainWind>:
    id: mn
    Screen:
        name: "Opening"
        MDFloatLayout:
            md_bg_color: (0, 15/250, 50/250, 1)
            Image:
                id: aniImage
                pos_hint: {"x": 0.28, "y": 0.48}
                source: "icon.jpeg"
                size_hint: 0, 0

            
            MDProgressBar:
                id: prg_bar
                max: 10
                color: (200/250, 200/250, 200/250, 1)
                min: 0
                pos_hint: {"x": 0.36, "y": 0.48}
                size_hint: 0.25, None
                
            Label:
                id: initial
                text: "Processing..."
                size_hint: None, None
                pos_hint: {"x": 0.44, "y": 0.44}
                font_size: 20

    Screen:
        name: "Main"
        MDBoxLayout:
            orientation: "horizontal"
            size_hint: 1,1

            MDBoxLayout:
                orientation: "vertical"
                   
                size_hint: 0.7, 1
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint: 1, 0.08 
                    MDToolbar:
                        id: tool
                        specific_text_color: root.colorMith("text")
                        md_bg_color: root.colorMith("light") 
                        
                MDSeparator:
                    id: sepTool
                    color: root.colorMith("light")
                

                MDBoxLayout:
                    id: try_scroll
                    orientation: 'vertical'
                    size_hint: 1, 0.92
                    ScreenManager:
                        id: insManage
                                
                        MDScreen:
                            id: Chat
                            name: "NoChat"
                            md_bg_color: root.colorMith("light")
                            MDFloatLayout:
                                Image:
                                    size_hint: 1, 1
                                    source: "logo.png"
                                    pos_hint:{"center_x": 0.6, "y": 0.1}
                            
                            
                        Screen:
                            name: "scrg"
                            MDBoxLayout:
                                orientation: "vertical"

                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint : (1, 0.9)
                                    
                                    ScrollView:
                                        size_hint : (1, 1)
                                        effect_cls :  "ScrollEffect"
                                        do_scroll_y : True
                                        do_scroll_x : True
                                        smooth_scroll_end : 30
                                        scroll_type : ["bars", 'content']
                                        bar_width : dp(8)
                                        bar_margin : [2, 4]
                                        
                                        MDBoxLayout:
                                            id: everMSGBOX
                                            orientation: "vertical"
                                            size_hint_y : None
                                            spacing : dp(8)
                                            padding : [10, 10 , 10, 10]
                                            height : self.minimum_height + 10
                                       
                                MDGridLayout:
                                    id: everMD
                                    md_bg_color: root.colorMith("darkest")
                                    cols : 2
                                    padding : [40, 5, 10, 10]
                                    size_hint :  (1, 0.1)
                                    spacing : 50
                                    MDTextFieldRound:
                                        id: everTextField
                                        size_hint: 0.5, 0.7
                                        hint_text : "Message"
                                        foreground_color: root.colorMith("text")
                                        hint_text_color: root.colorMith("text")
                                        color_active : root.colorMith("light") 
                                        normal_color : root.colorMith("normal")
                                        multiline: True
                                    MDIconButton:
                                        id: senEver
                                        icon: "send"
                                        user_font_size: "34sp"
                                        on_press: root.addTextUser()
                                    
            MDSeparator:
                id: sep1
                color: root.colorMith("sep") #mn.colorApp["sep"]
                size_hint: None, None
                width: 2
            MDBoxLayout:
                id: ord
                orientation: 'vertical'
                md_bg_color: root.colorMith("light")
                size_hint: 0.3, 1
                MDToolbar:
                    id: outTool
                    title: "Participants"
                    specific_text_color: root.colorMith("text")
                    md_bg_color: root.colorMith("darkest") 
                    left_action_items: [["account-group"]]
                    size_hint_y: 0.078
                MDSeparator:
                    id: sep2
                    color: root.colorMith("sep") #mn.colorApp["sep"]
                MDLabel:
                    id: unReadLabel
                    text: "Unread Chats:   0"
                    color: root.colorMith("text") #mn.colorApp["text"]
                    md_bg_color: root.colorMith("dark") #mn.colorApp["dark"]
                    font_size: "25sp"
                    halign: "center"
                    size_hint: 1, 0.09
                MDSeparator:
                    id: sep3
                    color: root.colorMith("sep") #mn.colorApp["sep"]
                ScrollView:
                    size_hint: 1, 0.8
                    do_scroll_y: True
                    scroll_type:['bars', 'content']
                    bar_width: 10
                    bar_pos_y: "left"
                    effect_cls: "ScrollEffect"
                    MDGridLayout:
                        id: online_but
                        cols: 1
                        spacing: 5
                        size_hint_y: None
                        height: self.minimum_height + 2

'''

class MainWind(ScreenManager):
    def __init__(self, **kwargs):
        super(MainWind, self).__init__(**kwargs)
        self.color = {"light": (0,15/250,50/250, 1), "normal": [0,15/250,70/250, 1],"dark": (0,15/250,45/250, 1), "darkest": [0,15/250,40/250, 1], "text": (1,1,1,1), "sep":(80/250, 80/250, 80/250, 1), "user": (10/250,115/250,190/250, 1),"sender":(0,57/250,80/250, 1) }
        self.ids.insManage.current = "NoChat"
        ########### NETWROK ##########
        self.newMsg = True
        self.incoming = ""
        self.datatype = ""
        self.newdata = ""
        self.sendId = True
        self.dict_identity = 0
        self.olderlist = []
        self.begin_sending = False
        self.clientsList = {}
        self.sender = ""
        self.knowSender = True
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ########### NETWROK ##########
        self.WindowWidth = Window.size[0]
        self.btnDict = {}
        self.sendBtnDict = {}
        self.inputDict = {}
        self.msgBoxDict = {}
        self.stp_send = False
        self.stp_recv = False
        self.once = True
        self.KnowIdOnce = True
        self.MYID = ""
        self.unRead = []
        menu = [{"viewclass": "DropMenu"}]
        self.menu = MDDropdownMenu(items=menu, width_mult=dp(4))
        self.themeSelect = 0
    def colorMith(self, mt):
        try:
            self.color = {"light": (0,15/250,50/250, 1), "normal": [0,15/250,70/250, 1],"dark": (0,15/250,45/250, 1), "darkest": [0,15/250,40/250, 1], "text": (1,1,1,1), "sep":(80/250, 80/250, 80/250, 1), "user": (10/250,115/250,190/250, 1),"sender":(0,57/250,80/250, 1) }
            return self.color[mt]
        except:
            pass
    def askName(self):
        self.pop = Popup()
        self.pop.title = "Enter Your Name"
        self.pop.size_hint = (0.5, 0.6)
        self.pop.auto_dismiss = False
        self.pop.title_size = 20
        self.pop.open()
        self.pop.background_color = (0, 105/250, 120/250, 1)
        self.pop.separator_color = (0 / 255, 200 / 255, 1, 1)
        ######################
        self.flt = FloatLayout()
        self.flt.input = MDTextField(hint_text="Enter Name",
                                     icon_right = "rename-box",
                                     icon_right_color = (0.8, 0.8, 1, 1),
                                     required=True,
                                     max_text_length=20,
                                     font_size=20,
                                     mode = "rectangle",
                                     line_color_normal = (0.8, 60/255, 60/255, 1),
                                     line_color_focus = (0.8, 60/255, 60/255, 1),
                                     size_hint=(0.6, 0.6),
                                     pos_hint={"x": 0.2, "y": 0.7},
                                     on_text_validate = lambda dt: [self.change()])
        ##
        self.flt.ip = MDTextField(hint_text="Enter Server IP",
                                     required=True,
                                  icon_right="server-security",
                                  icon_right_color=(0.8, 0.8, 1, 1),
                                     max_text_length=15, helper_text = "Integer input only",
                                     font_size=20,
                                     mode="rectangle",
                                     line_color_normal=(0.8, 60 / 255, 60 / 255, 1),
                                     line_color_focus=(0.8, 60 / 255, 60 / 255, 1),
                                     size_hint=(0.6, 0.4),
                                     pos_hint={"x": 0.2, "y": 0.5},on_text_validate = lambda dt: [self.change()])
        self.flt.port = MDTextField(hint_text="Enter Server Port",
                                  required=True,
                                  max_text_length=10,
                                    icon_right="serial-port",
                                    icon_right_color=(0.8, 0.8, 1, 1),
                                    helper_text="Integer input only",
                                  font_size=20,
                                  mode="rectangle",
                                  line_color_normal=(0.8, 60 / 255, 60 / 255, 1),
                                  line_color_focus=(0.8, 60 / 255, 60 / 255, 1),
                                  size_hint=(0.6, 0.4),
                                  pos_hint={"x": 0.2, "y": 0.3}, on_text_validate = lambda dt: [self.change()])

        self.unable = MDLabel(text = "Entered Ip or Port is Wrong!",font_style = "Subtitle1", font_size = "50sp", halign = "center", size_hint=(0.8, 0.3), pos_hint={"x": 0.07, "y": 0.77})
        self.flt.add_widget(self.flt.input)
        self.flt.add_widget(self.flt.ip)
        self.flt.add_widget(self.flt.port)
        self.flt.button = MDFillRoundFlatButton(text="Confirm",
                                                size_hint=(0.12, 0.14),
                                                font_size=17,
                                                text_color=(0 / 255, 7 / 255, 15 / 255, 1),
                                                md_bg_color=(0 / 255, 200 / 255, 186 / 255, 1),
                                                padding=10,
                                                elevation=20,
                                                pos_hint={"x": 0.4, "y": 0.1},
                                                on_press = lambda dt: [self.change()])

        self.flt.add_widget(self.flt.button)
        self.pop.content = self.flt
    def change(self):
        if self.flt.input.text and self.flt.ip.text and self.flt.port.text:
            self.join()


    def display_online(self, Incdict):
        if self.KnowIdOnce == True:
            self.MYID = list(Incdict.keys())[::-1][0]
            self.KnowIdOnce = False
        for i in Incdict.keys():
            if i != self.MYID and i not in self.olderlist:
                self.btn = MDRectangleFlatIconButton(icon = "account-circle", text=Incdict[i], icon_color = self.color["text"], theme_text_color = "Custom", text_color =self.color["text"], line_color = self.color["text"], font_size = "40sp",size_hint_y = None, height=50)
                self.btn.size_hint_x = 1
                self.ids["btn" + str(i)] = self.btn
                self.btnDict[self.ids["btn" + str(i)]] = "btn" + str(i)
                self.btn.bind(on_press = lambda dt: self.identify_btn(1))
                self.ids.online_but.add_widget(self.btn)
                self.addScreen(i)

        self.olderlist = list(Incdict.keys())
        if len(self.clientsList.keys()) >= 3 and self.once == True:
            self.everyone_But = MDRectangleFlatIconButton(text= "Everyone", font_size="45sp",icon = "account-circle", icon_color = self.color["text"], theme_text_color = "Custom", text_color =self.color["text"],line_color = self.color["text"], height=50)
            self.everyone_But.size_hint = (1, None)
            self.everyone_But.bind(on_press = lambda dt: self.identify_btn(2))
            self.ids.ord.add_widget(self.everyone_But)
            self.once = False
        if len(self.clientsList.keys()) == 1:
            self.ids.online_but.add_widget(Label())



    def identify_btn(self, typ):
        if typ != 2:
            for i in self.btnDict.keys():
                if i.state == "down":
                    self.ids.insManage.transition = NoTransition()
                    self.ids.insManage.current = "scr" + self.btnDict[i][3:]
                    self.ids.tool.title = self.clientsList[int(self.btnDict[i][3:])]
                    self.ids.tool.md_bg_color = self.color["darkest"]
                    self.ids.sepTool.color = self.color["sep"]

                    if int(self.btnDict[i][3:]) in self.unRead:
                        i.icon = "account-circle"
                        i.icon_color = self.color["text"]
                        self.unRead.remove(int(self.btnDict[i][3:]))
                    break

        else:
            self.ids.insManage.transition = NoTransition()
            self.ids.insManage.current = "scrg"
            self.ids.tool.title = "Everyone"
            self.ids.tool.md_bg_color = self.color["darkest"]
            self.ids.sepTool.color = self.color["sep"]
            if "g" in self.unRead:
                self.everyone_But.icon = "account-circle"
                self.everyone_But.icon_color = self.color["text"]
                self.unRead.remove("g")

        self.ids.unReadLabel.text = "Unread Chats:   " + str(len(self.unRead))

    def addScreen(self, key):
        self.scr = Screen(name = f"scr{key}")
        self.scr_box = MDBoxLayout(orientation = "vertical")
##################################################################################################################################################
        ######### Containing Scroll #############
        self.containScroll = MDBoxLayout(orientation = "vertical", size_hint = (1, 0.9))
        ######### Containing Scroll #############
        ######## SCROLLVIEW ############
        self.scroll = ScrollView(effect_cls = "ScrollEffect")
        self.scroll.size_hint = (1, 1)
        self.scroll.do_scroll_y = True
        self.scroll.do_scroll_x = True
        self.scroll.smooth_scroll_end = 30
        self.scroll.scroll_type = ["bars", 'content']
        self.scroll.bar_width = dp(8)
        self.scroll.bar_margin = [2, 4]
        ######## SCROLLVIEW ############
        ######## Messages ##############
        self.msgBox = MDBoxLayout()
        self.msgBox.orientation = "vertical"
        self.msgBox.size_hint_y = None
        self.msgBox.spacing = dp(5)
        self.msgBox.padding = [10, 0 , 0, 0]
        self.msgBox.height = self.msgBox.minimum_height + 10
        self.ids["msgBox" + str(key)] = self.msgBox
        self.msgBoxDict["msgBox" + str(key)] = self.ids["msgBox" + str(key)]
        self.scroll.add_widget(self.msgBox)
        self.containScroll.add_widget(self.scroll)
        ######## Messages ##############
        ######## Input #################
        self.inpBox = MDGridLayout()
        self.inpBox.md_bg_color = self.color["darkest"]
        self.inpBox.cols = 2
        self.inpBox.padding = [40, 5, 10, 10]
        self.inpBox.size_hint = (1, 0.1)
        self.inpBox.spacing = 50
        ###############
        self.inpBox.inp = MDTextFieldRound(hint_text = "Message", foreground_color = self.color["text"], color_active = self.color["light"], normal_color = self.color["normal"])
        self.inpBox.inp.size_hint = (0.5, 0.4)
        self.inpBox.inp.hint_text_color = self.color["text"]
        self.inpBox.inp.multiline = True
        ################
        ######### Input ##########
        ####### Send #######
        self.inpBox.sen = MDIconButton(icon = "send", user_font_size = "34sp", on_press = lambda dt: [self.addTextUser()])
        ####### Send #######
        self.inpBox.add_widget(self.inpBox.inp)
        self.ids["inpBox" + str(key)] = self.inpBox.inp
        self.inputDict["inpBox" + str(key)] = self.ids["inpBox" + str(key)]
        ####
        self.inpBox.add_widget(self.inpBox.sen)
        self.ids["inpSend" + str(key)] = self.inpBox.sen
        self.sendBtnDict[self.ids["inpSend" + str(key)]] = "inpSend" + str(key)

        ######## BoxLayout #################
        self.scr_box.add_widget(self.containScroll)
        self.scr_box.add_widget(self.inpBox)
        ###################################
        self.scr.add_widget(self.scr_box)
        self.ids.insManage.add_widget(self.scr)
####################################################################################################################################

    def addTextUser(self):
        self.lineBreak = 0
        self.toDisplay = 0
        for i in self.sendBtnDict.keys():
            if i.state == "down":
                self.toDisplay = self.sendBtnDict[i][7:]
                break
        else:
            self.toDisplay = "g"

        self.indMessage = self.inputDict["inpBox" + self.toDisplay].text if self.toDisplay != "g" else self.ids.everTextField.text
        ##################
        self.cardUser = MDCard(radius = [0, 20 , 20, 20],md_bg_color = self.color["user"], spacing = sp(2), padding = [8, 0 , 0, 0], size_hint = (None, None))
        self.lbIncardUser = MDLabel(text = self.indMessage, theme_text_color =  "Custom", text_color = self.color["text"], font_size = "10sp")
        for i in self.lbIncardUser.text:
            if i == "\n":
                self.lineBreak += 1

        ######################################################
        if int(len(self.indMessage)*4) + ((self.WindowWidth * 0.3)/6) > (self.WindowWidth/4 + self.WindowWidth/8):
            if int(len(self.indMessage)) * 4 <= sp(4000):
                self.cardUser.height = dp(self.lbIncardUser.font_size * 3 + 40 * math.ceil(
                    (int(len(self.indMessage)) * 3) / (
                            self.WindowWidth / 6 + self.WindowWidth / 8)))
                self.cardUser.width = dp((self.WindowWidth / 4 + self.WindowWidth / 8))
            elif  sp(4000) < int(len(self.indMessage)) * 4 <= sp(4800) :
                self.cardUser.height = dp(self.lbIncardUser.font_size * 3 + 40 * math.ceil(
                    (int(len(self.indMessage)) * 4) / (
                            self.WindowWidth / 6 + self.WindowWidth / 8)))
                self.cardUser.width = dp((self.WindowWidth / 4 + self.WindowWidth / 8))

            else:
                self.cardUser.height = dp(self.lbIncardUser.font_size * 3 + 50 * math.ceil(
                    (int(len(self.indMessage)) * 4) / (
                            self.WindowWidth / 6 + self.WindowWidth / 8)))
                self.cardUser.width = dp((self.WindowWidth / 4 + self.WindowWidth / 8))
        else:
            if len(self.indMessage) == 1:
                self.cardUser.width = dp(((self.WindowWidth * 0.3)/6))
                self.cardUser.height = dp(self.lbIncardUser.font_size*3)
            else:
                self.cardUser.width = dp(((self.WindowWidth * 0.3)/6) + (int(len(self.indMessage))*4))
                self.cardUser.height = dp(self.lbIncardUser.font_size*3)

        self.cardUser.add_widget(self.lbIncardUser)
        ######################################################
        self.cardUser.height += dp(self.lineBreak*self.lbIncardUser.font_size)
        if str(self.toDisplay) != "g":
            self.msgBoxDict["msgBox" + str(self.toDisplay)].add_widget(self.cardUser)
            self.msgBoxDict["msgBox" + str(self.toDisplay)].add_widget(MDLabel(text = f'{datetime.datetime.now().strftime("%I:%M%p")}', theme_text_color =  "Custom", text_color = self.color["text"]))
            self.msgBoxDict["msgBox" + str(self.toDisplay)].height += dp(self.cardUser.height + 20)
            self.user_text = str(self.toDisplay) + str(self.indMessage)
            self.inputDict["inpBox" + self.toDisplay].text = ""
        else:
            self.ids.everMSGBOX.add_widget(self.cardUser)
            self.ids.everMSGBOX.add_widget(MDLabel(text = f'{datetime.datetime.now().strftime("%I:%M%p")}', theme_text_color =  "Custom", text_color = self.color["text"]))
            self.ids.everMSGBOX.height += dp(self.cardUser.height + 20)
            self.user_text = str(self.toDisplay) + str(self.ids.everTextField.text)
            self.ids.everTextField.text = ""

    def addTextSender(self, sender, message, typ):
        self.lineBreakSender = 0
        for i in message:
            if i== "\n":
                self.lineBreakSender += 1
        self.takeObj = MDBoxLayout(orientation = "horizontal", md_bg_color = (0.4, 0.1, 0.1, 1), size_hint = (1, None))
        self.cardSender = MDCard(radius=[20, 0, 20, 20], spacing = 3, padding=[8, 0, 8, 8], size_hint=(None, None), pos_hint = {"right": 1}
                             , md_bg_color = self.color["sender"])

        self.lbIncardSender = MDLabel(text=message, font_size=sp(20), theme_text_color =  "Custom", text_color = self.color["text"])
        self.lbIncardSender.height = dp(self.lbIncardSender.texture_size[1])

        if int(len(message) * 4) + ((self.WindowWidth * 0.3) / 6) > (self.WindowWidth / 4 + self.WindowWidth / 8):
            if int(len(message)) * 4 <= sp(4000):
                self.cardSender.height = dp(self.lbIncardSender.font_size * 3 + 43 * math.ceil((int(len(message)) * 3) / (self.WindowWidth / 6 + self.WindowWidth / 8)))
                self.cardSender.width = dp((self.WindowWidth / 4 + self.WindowWidth / 8))
            elif sp(4000) < int(len(message)) * 4 <= sp(4800):
                self.cardSender.height = dp(self.lbIncardSender.font_size * 3 + 43 * math.ceil((int(len(message)) * 4) / (self.WindowWidth / 6 + self.WindowWidth / 8)))
                self.cardSender.width = dp((self.WindowWidth / 4 + self.WindowWidth / 8))

            else:
                self.cardSender.height = dp(self.lbIncardSender.font_size * 3 + 50 * math.ceil(
                    (int(len(message)) * 4) / (
                            self.WindowWidth / 6 + self.WindowWidth / 8)))
                self.cardSender.width = dp((self.WindowWidth / 4 + self.WindowWidth / 8))
        else:
            if len(message) == 1:
                self.cardSender.width = dp(((self.WindowWidth * 0.3) / 6))
                self.cardSender.height = dp(self.lbIncardSender.font_size * 3)
            else:
                self.cardSender.width = dp(((self.WindowWidth * 0.3) / 6) + (int(len(message)) * 4.5))
                self.cardSender.height = dp(self.lbIncardSender.font_size * 3)

        self.cardSender.add_widget(self.lbIncardSender)
        self.cardSender.height += dp(self.lineBreakSender*self.lbIncardSender.font_size)

        if str(typ) != "g":
            self.msgBoxDict["msgBox" + str(sender)].add_widget(self.cardSender)
            self.msgBoxDict["msgBox" + str(sender)].add_widget(MDLabel(text=f'{datetime.datetime.now().strftime("%I:%M%p")}', halign = "right", theme_text_color =  "Custom", text_color = self.color["text"]))
            self.msgBoxDict["msgBox" + str(sender)].height += dp(self.cardSender.height + 20)
            if int(sender) not in self.unRead:
                if str(typ) != "g":
                    if self.ids.insManage.current != "scr" + str(sender):
                        self.unRead.append(int(sender))
                        for i in self.btnDict.keys():
                            if self.btnDict[i] != "scr" + str(sender):
                                i.icon = "message-text"
                                i.icon_color = (0, 1, 0, 1)
                                break

        else:
            self.takeObj.height = self.cardSender.height
            self.takeObj.add_widget(MDLabel(text=f'Sender: {self.clientsList[int(sender)]}', font_size="90sp", halign="center", valign="center"))
            self.takeObj.add_widget(self.cardSender)
            self.ids.everMSGBOX.add_widget(self.takeObj)
            self.ids.everMSGBOX.add_widget(MDLabel(text=f'{datetime.datetime.now().strftime("%I:%M%p")}', halign = "right",theme_text_color =  "Custom", text_color = self.color["text"]))
            self.ids.everMSGBOX.height += dp(self.cardSender.height + 25)
            if "g" not in self.unRead:
                if self.ids.insManage.current != "scrg":
                    self.unRead.append("g")
                    self.everyone_But.icon = "message-text"
                    self.everyone_But.icon_color = (0, 1, 0, 1)

        self.ids.unReadLabel.text = "Unread Chats:   " + str(len(self.unRead))

####################################### NETWORK  #######################################################################
    def join(self):
        try:
            self.client.connect((self.flt.ip.text, int(self.flt.port.text)))
            welcome = self.client.recv(100).decode("utf-8")
            self.pop.dismiss()
            self.ids.prg_bar.value += 2
            self.current = "Main"
            self.client.sendall(self.flt.input.text.encode("utf-8"))
            self.strThread()
        except:
            try:
                self.flt.add_widget(self.unable)
            except:
                pass
            print("Unable to connect with Server :(\n")

    def recv(self):
        try:
            while True:
                self.data = self.client.recv(SIZE + 7)
                if self.newMsg:
                    self.datatype = str(self.data.decode("utf-8")[SIZE: SIZE + 1])
                    self.msglen = int(self.data.decode("utf-8")[:SIZE])
                    self.newMsg = False

                if self.datatype == "n":
                    self.newdata += self.data.decode("utf-8")
                    self.sliceValue = int(self.newdata.find("n")) + 1

                    if len(self.newdata[self.sliceValue:]) == int(self.msglen):
                        self.clientsList = ast.literal_eval(self.newdata[SIZE + 1:])
                        self.display_online(self.clientsList)
                        self.newMsg = True
                        self.newdata = ""
                        self.datatype = ""

                elif self.datatype == "l":
                    for i in self.btnDict.keys():
                        if self.btnDict[i] == "btn" + str(self.msglen):
                            self.ids.online_but.remove_widget(i)
                            del self.btnDict[i]
                            if self.ids.insManage.current == "scr" + str(self.msglen):
                                self.ids.insManage.current = "NoChat"
                                self.ids.tool.md_bg_color = self.color["light"]
                                self.ids.sepTool.color = self.color["light"]
                                self.ids.tool.title = ""
                            break
                    self.newMsg = True
                    self.datatype = ""

                elif self.datatype == "r":
                    self.fndindex = self.data.decode("utf-8").find("r")
                    self.incoming += self.data.decode("utf-8")
                    if self.knowSender:
                        self.sender = int(str(self.data.decode("utf-8"))[self.fndindex+1: self.fndindex +2])
                        self.knowSender = False

                    if len(self.incoming[int(self.incoming.index("r"))+2:]) == self.msglen:
                        self.addTextSender(self.sender, self.incoming[SIZE + 2:], 0)
                        self.sender = ""
                        self.newMsg = True
                        self.incoming = ""
                        self.datatype = ""
                        self.knowSender = True

                elif self.datatype == "g":
                    self.fndindex = self.data.decode("utf-8").find("g")
                    self.incoming += self.data.decode("utf-8")
                    if self.knowSender:
                        self.sender = int(str(self.data.decode("utf-8"))[self.fndindex + 1: self.fndindex + 2])
                        self.knowSender = False

                    if len(self.incoming[int(self.incoming.index("g"))+2:]) == self.msglen:
                        self.addTextSender(self.sender, self.incoming[SIZE + 2:], "g")
                        self.sender = ""
                        self.newMsg = True
                        self.incoming = ""
                        self.datatype = ""
                        self.knowSender = True

                if self.stp_recv:
                    break
        except:
            pass

    def send(self):

        self.user_text = ""
        while True:
            if self.user_text:
                if self.user_text[:1].isnumeric():
                    self.clientsList_keys = list(self.clientsList.keys())
                    self.clientsList_values = list(self.clientsList.values())
                    msg = str(f"{self.user_text[:1]}{len(self.user_text) - 1:<{SIZE}}" + "r" + str(self.clientsList_keys[int(self.clientsList_values.index(self.flt.input.text))]) + self.user_text[1:])
                    self.client.send(msg.encode("utf-8"))
                    self.user_text = ""
                    msg = ""

                elif self.user_text[:1] == "g":
                    self.clientsList_keys = list(self.clientsList.keys())
                    self.clientsList_values = list(self.clientsList.values())
                    msg1 = str(f"{str('~')}{len(self.user_text) - 1:<{SIZE}}" + "g" + str(self.clientsList_keys[int(self.clientsList_values.index(self.flt.input.text))]) + self.user_text[1:])
                    self.client.send(msg1.encode("utf-8"))
                    self.user_text = ""
                    msg1 = ""

            if self.stp_send:
                break


    def strThread(self):
        self.trd1 = threading.Thread(target = self.recv)
        self.trd2 = threading.Thread(target=self.send)
        self.trd1.start()
        self.trd2.start()

    def stpTrd(self):
        for i in self.clientsList.keys():
            if self.clientsList[i] == self.flt.input.text:
                self.client.send(str(f"{str('`')}{5:<{SIZE}}" + "l" + str(i) + "leave").encode("utf-8"))
                break
        self.client.close()
        self.stp_send = True
        self.stp_recv = True
        try:
            self.trd1.join()
            self.trd2.join()
        except:
            pass

####################################### NETWORK  #######################################################################

Builder.load_string(Kv)
class GUI(MDApp):

    def build(self):
        self.akName = True
        self.title = "Zesting"
        self.icon = "icon.jpeg"
        self.title_text_color = (0.4, 0.2, 0.2, 1)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.accent_palette = "Gray"
        Window.maximize()
        self.a = Clock.schedule_interval(lambda dt: self.updateValue(), 1)
        return MainWind()

    def on_stop(self):
        self.root.stpTrd()

    def on_start(self):
        animation = Animation(size_hint = (0.5, 0.5), t = "out_bounce")
        animation += Animation(size_hint = (0.4, 0.4), t = "out_expo")
        animation.start(self.root.ids.aniImage)

    def updateValue(self):
        if self.root.ids.prg_bar.value <= 6:
            if self.root.ids.prg_bar.value == 0:
                self.root.ids.initial.text = "Connecting."
            elif self.root.ids.prg_bar.value == 4:
                self.root.ids.initial.text = " Connecting.."
            elif self.root.ids.prg_bar.value == 6:
                self.root.ids.initial.text = "   Connecting...."
            self.root.ids.prg_bar.value += 2
        else:
            if self.akName:
                self.root.askName()
                Clock.unschedule(self.a)
                self.akName = False

if __name__ == "__main__":
    GUI().run()
