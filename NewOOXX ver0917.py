import tkinter as tk
from os import path
from unicodedata import name
import DB_use as dbu

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading
from time import sleep 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading
import time
# 引用私密金鑰
# path/to/serviceAccount.json 請用自己存放的路徑
cred = credentials.Certificate('ggdog-72aa5-firebase-adminsdk-uatst-9f83c733a5.json')
# 初始化firebase，注意不能重複初始化
#firebase_admin.initialize_app(cred)

db = firestore.client()
# 主檔案解壓後的絕對路徑
print('__file__=',__file__)
# 主檔案解壓後所在目錄的絕對路徑
parentPath = path.dirname(__file__)
print('parentPath=',parentPath)

toolPath = path.dirname(path.join(parentPath,'.'))
print('toolPath=',toolPath)

your_player = {"player":"","name":""}
opp_player = ""
# def name_now():
#     whos_turn = dbu.quickstart_get_collection("game","room1","whos_turn")
#     return dbu.quickstart_get_collection("player_online",whos_turn,"name")

def orig():
    dbu.quickstart_uppade("player_online","player1","name","")
    dbu.quickstart_uppade("player_online","player2","name","")   

def judge_win():
    win_mode = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for i in win_mode:
        #print(dbu.quickstart_get_collection("game",f"block{i[0]+1}","control"),)
        if dbu.quickstart_get_collection("game",f"block{i[0]+1}","control") == dbu.quickstart_get_collection("game",f"block{i[1]+1}","control") == dbu.quickstart_get_collection("game",f"block{i[2]+1}","control") == "O":
            # print("get it!")
            # if dbu.quickstart_get_collection("game",f"block{i[0]+1}","control") == "O":
            print("___")
            print(i)
            print("player1 win!!")
            return True
            # if dbu.quickstart_get_collection("game",f"block{i[0]+1}","control") == "X":
            #     print("player2 win!!")
        if dbu.quickstart_get_collection("game",f"block{i[0]+1}","control") == dbu.quickstart_get_collection("game",f"block{i[1]+1}","control") == dbu.quickstart_get_collection("game",f"block{i[2]+1}","control") == "X":
            print("___")
            print(i)
            print("player2 win!!")
            return True
    return False
def listen_for_changes():
    #delete_done = threading.Event()
    def on_snapshot(col_snapshot, changes, read_time):
        print(u'Callback received query snapshot.')
        print(u'Current cities in California: ')
        for change in changes:
            print("check")
            if change.type.name == 'MODIFIED':
                print("GGGG")
                print(f'Modified player: {change.document.id}')
                #delete_done.set()
    col_query = db.collection(u'player_online').where(u'block', u'==', u'open')
    query_watch = col_query.on_snapshot(on_snapshot)
    #delete_done.wait(timeout=30)
    query_watch.unsubscribe()

class OOXXapp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("OOXX game")
        self.geometry("500x600")
        self.resizable(1,1)
        self.config(bg = 'white')
        self.attributes("-alpha",1)
        self._frame = None
        self.clear()
        self.switch_frame(StartPage)
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
    def clear(self):
        dbu.quickstart_uppade("game","room1","whos_turn","player1")

class StartPage(tk.Frame):
    def __init__(self, master):
        #self.orig()
        tk.Frame.__init__(self, master)
        tk.Label(text="曾嘎曾嘎ＯＯＸＸ",font= ('微軟正黑體',36),width=12,height=1,bg = 'white').pack(side="top", fill="x", pady=5)
        tk.Label(text="主選單",font= ('微軟正黑體',24),width=16,height=1,bg = 'skyblue').pack()
        self.sys_message = tk.Label(text="請輸入你的暱稱：",font= ('微軟正黑體',16),width=20,height=2,bg = 'white')
        self.sys_message.pack()
        self.entry_name = tk.Entry(self)
        self.entry_name.pack()
        self.bnt_confirm =tk.Button(self, text="確認",bg = "gray",
                  command=lambda: self.login())
        self.bnt_confirm.pack()     
        self.btn_start = tk.Button(self, text="開始遊戲",command=lambda:[self.sys_message.forget(),self.start(), master.switch_frame(GamePage)])#.pack(side="top", fill="x", pady=5)
        self.col_query = db.collection(u'player_online').where(u'block', u'==', u'open')
        self.query_watch = self.col_query.on_snapshot(self.on_snapshot)
    def login(self):
        if self.entry_name.get() == "":
            print("請輸入暱稱來開始遊戲！")
            self.sys_message.config(text="請輸入暱稱來開始遊戲！")
        else:
            global your_player,opp_player
            print(dbu.quickstart_get_collection('player_online',"player1","name"))
            if dbu.quickstart_get_collection('player_online',"player1","name") == "":   
                your_player["player","name"] = "player1",self.entry_name.get()
                dbu.quickstart_uppade("player_online","player1","name",self.entry_name.get())
                your_player["player"] = "player1"
                your_player["name"] = self.entry_name.get()
                self.bnt_confirm.forget()
                self.entry_name.forget()
                self.sys_message.config(text=your_player["name"]+" 登入為玩家一\n等待匹配對手中...") 
                opp_player = "player2"
                             
            else:   
                your_player["player","name"] = "player2",self.entry_name.get()
                dbu.quickstart_add_data_one('player_online',"player2","name",self.entry_name.get())
                your_player["player"] = "player2"
                your_player["name"] = self.entry_name.get()
                self.bnt_confirm.forget()
                self.entry_name.forget()
                self.btn_start.pack()
                self.sys_message.config(text=your_player["name"]+"+ 登入為玩家二\n玩家一為:"+dbu.quickstart_get_collection('player_online',"player1","name"))     
                opp_player = "player1"         
    def start(self):
        self.query_watch.unsubscribe()
    def on_snapshot(self,col_snapshot, changes, read_time):
        print(u'Callback received query snapshot.')
        print(u'Current cities in California: ')
        for change in changes:
            print("check")
            if change.type.name == 'MODIFIED':
                print("GGGG")
                print(f'Modified player: {change.document.id}')
                self.btn_start.pack()
                self.sys_message.config(text=your_player["name"]+"+ 登入為玩家一\n玩家二為:"+dbu.quickstart_get_collection('player_online',"player2","name"))                    

class Button():
    def __init__(self,frame,x,y,positon):
        self.position = positon
        self.textA = tk.StringVar()
        self.textA.set("")
        self.be_controled = False
        self.button = tk.Button(frame,bd=2,width=3,height=3,textvariable=self.textA,font = ("Helvetica","30"),command=lambda: [self.XOcontral()]).grid(row=x,column=y)
    def XOcontral(self):
        if dbu.quickstart_get_collection("game","room1","whos_turn") == your_player["player"]:
            if self.be_controled == False:
                self.be_controled = True
                if your_player["player"] == "player1":
                    self.textA.set("O")
                    #dbu.quickstart_uppade("game","room1","whos_turn","player2")
                    dbu.quickstart_uppade("game",self.position,"control","O")
                elif your_player["player"] == "player2":
                    self.textA.set("X")
                    #dbu.quickstart_uppade("game","room1","whos_turn","player1")
                    dbu.quickstart_uppade("game",self.position,"control","X")

class GamePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.textH = tk.StringVar()
        self.textH.set("的回合")
        self.sys_message = tk.Label(textvariable = self.textH,font= ('微軟正黑體',16),width=20,height=1,bg = 'white')
        self.sys_message.pack()
        self.frame = tk.Frame(self,borderwidth = 2,width=300,height=300)
        self.frame.pack()
        self.frame.pack_propagate(0)
        self.block1 = Button(self.frame,0,0,"block1")
        self.block2 = Button(self.frame,0,1,"block2")
        self.block3 = Button(self.frame,0,2,"block3")
        self.block4 = Button(self.frame,1,0,"block4")  
        self.block5 = Button(self.frame,1,1,"block5")
        self.block6 = Button(self.frame,1,2,"block6")
        self.block7 = Button(self.frame,2,0,"block7")
        self.block8 = Button(self.frame,2,1,"block8")
        self.block9 = Button(self.frame,2,2,"block9")
        self.blocks = [self.block1,self.block2,self.block3,self.block4,self.block5,self.block6,self.block7,self.block8,self.block9]
        self.clear()
        self.col_query = db.collection(u'game').where(u'listen', u'==', u'Y')
        self.query_watch = self.col_query.on_snapshot(self.on_snapshot)
    def on_snapshot(self,col_snapshot, changes, read_time):
        print(u'Callback received query snapshot.')
        print(u'Current cities in California: ')
        for change in changes:
            if change.type.name == 'MODIFIED':
                print("opp's move")
                print(f'Modified player: {change.document.id}')
                if dbu.quickstart_get_collection("game","room1","whos_turn") != your_player["player"]:
                    self.blocks[int(change.document.id[-1])-1].textA.set(dbu.quickstart_get_collection("game",change.document.id,"control"))
                    self.blocks[int(change.document.id[-1])-1].be_controled = True
                    dbu.quickstart_uppade("game","room1","whos_turn",your_player["player"])
                    print(dbu.quickstart_get_collection("game","room1","whos_turn"))
                    if judge_win():
                        for block in self.blocks:
                            block.be_controled = True
                            #self.textH.set(f"{name_now()}獲勝！！")
                    print("MM")
                    #self.textH.set(f"{name_now()}的回合")
                    
                else:
                    dbu.quickstart_uppade("game","room1","whos_turn",opp_player)
                    print(dbu.quickstart_get_collection("game","room1","whos_turn"))
                    if judge_win():
                        for block in self.blocks:
                            block.be_controled = True
                            #self.textH.set(f"{name_now()}獲勝！！")
                    #self.textH.set(f"{name_now()}的回合")
                    print("OM")
    def clear(self):
        game_blocks = db.collection("game")
        for doc in game_blocks.stream():
            game_blocks.document(doc.id).update({"control":"" })
        
        




#下次需做格子的控制權歸屬

main_OOXX_win = OOXXapp()
main_OOXX_win.mainloop( )

        


         
