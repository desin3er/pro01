import tkinter as tk
import tkinter.ttk
import os
from tkinter.filedialog import askdirectory
import func_module as fm
######################################asjdhaskljf################################
#메인 스크린 프레임의 크기생성
def main_screen(view,h,w):
    canvas = tk.Canvas(view, height = h, width = w)
    canvas.pack()

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None  #초기 실행시 self._frame 에 None할당
        fm.Func_Class.cam_init()#camera init 초기화 프로그램 시작시 한번만
    
        fm.Func_Class.song_init()
        self.switch_frame(StartPage)#switch_fram()멤버 메소드 호출(인자는 StartPage 클래스)
        
        
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)#new_fram에 인자 클래스 객체 생성
        if self._frame is not None:#self._frame 이 None 이 아닐때
            self._frame.destroy()#_frame을 메모리에서 클리어
            fm.Func_Class.off_show()
        self._frame = new_frame#self._frame = 매개인자로 넘어온 클래스의 객체를 넘겨준다.
        self._frame.pack()#넘어온 객체를 화면에 띄운다.

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.func = fm.Func_Class()       
        self.main_frame()#main frame생성
        self.btn_frame(master)#btn 생성
        try:
            self.cam_frame()#cam 프레임 생성
        except:
            print('카메라 연결 이상')
        self.song_frame()#song 프레임 생성          
        print('Main Page Load Compelete')
###################멤버 메소드 생성##########################딜리버리히어로, 엔디소프트
    def main_frame(self):
        main_screen(self,480,800)
        self.img = tk.PhotoImage(file = 'image/main.png')
        tk.Label(self, image = self.img).place(x=0,y=0, relwidth=1, relheight=1)
        tk.Label(self, text = '100%').place(relx=0.955, rely=0.02, height = 13)

    def btn_frame(self,master):    
        self.img_cam = tk.PhotoImage(file = 'image/cam1.png')
        self.img_song = tk.PhotoImage(file = 'image/song.png')
        self.img_gear = tk.PhotoImage(file = 'image/gear2.png')
        tk.ttk.Progressbar(self,length = 25, maximum=100,value = 50 ,mode='determinate').place(relx=0.92, rely=0.02, height = 13)
        tk.Button(self, text="노래 듣기",image=self.img_song,compound = tk.LEFT,padx = 10,
                command=lambda: self.notebook.select(1)).place(relx=0.8, rely=0.25, height = 50, width = 135)
        tk.Button(self, text="사진 찍기",image=self.img_cam,compound = tk.LEFT,padx = 10,
                command=lambda: self.notebook.select(0)).place(relx=0.8, rely=0.37, height = 50, width = 135)
        tk.Button(self, text="관리자모드",image=self.img_gear,compound = tk.LEFT,padx = 10,
                command=lambda: master.switch_frame(PageOne)).place(relx=0.8, rely=0.49, height = 50, width = 135)

    def cam_frame(self):
                #############카메라 프레임###################
             
        self.notebook=tk.ttk.Notebook(self, width=400, height=350)
        self.notebook.place(relx=0.05, rely=0.1)
        frame1=tkinter.Frame(self)
        self.notebook.add(frame1, text="이미지")
        label1=tkinter.Label(frame1,text='cam')
        label1.place(relwidth = 1, relheight=1)
        
        #이미지 재생       
        def show_frame():           
            # imgtk = self.func.live_show()
            imgtk = self.func.face_search()
            label1.imgtk = imgtk
            label1.configure(image=imgtk)
            label1.after(25, show_frame)        
        show_frame() 
        
    def song_frame(self):
        rel_W,rel_H = 0.85, 0.75#스크롤 바와 리스트의 길이를 맞추는 변수
        self.status_play = 0#현재 노래 재생 상태
        frame2=tkinter.Frame(self)#프레임 2번 생성
        self.notebook.add(frame2, text="노래")#notebook에 추가
        label2=tkinter.Label(frame2, text="동요 듣기")#설명 라벨
        label2.pack()
        self.yScroll = tk.Scrollbar(frame2, orient=tk.VERTICAL)#song list box의 스크롤 생성
        self.yScroll.place(relx=0.90, rely=0.05,relheight = rel_H)   #song list box의 스크롤 생성
        list_song = tk.Listbox(frame2,yscrollcommand=self.yScroll.set)#프레임 2번에 리스트 박스 생성
        self.yScroll['command'] = list_song.yview #list box yscroll command
        
        j = 0 #리스트박스의 인덱스
        for i in self.func.file_list:            
            if i.find('.mp3') :#리스트의 아이템에서 .mp3가 들어간 파일만
                list_song.insert(j, i)#리스트에 삽입
                j += 1
        list_song.place(relx=0.05, rely=0.05,relwidth = rel_W, relheight = rel_H)#리스트 화면에 생성
        #리스트 박스의 이벤트 처리       
        def onselect(evt):
            print (self.status_play)
            if self.status_play == 0:
                w = evt.widget#이벤트의 객체 받아온다.
                index = int(w.curselection()[0])#리스트박스의 선택된 list의 인덱스 값을 가져온다.
                value = w.get(index)#리스트 박스의 인덱스에 맞는 값을 읽어 온다.
                self.func.song_play(value)
                self.status_play = 1
            else:
                self.func.song_stop()
                self.status_play = 0        
        list_song.bind('<<ListboxSelect>>', onselect)#listbox 이벤트 bind(리스트 박스 셀렉트시 이벤트 진행)


class PageOne(tk.Frame):#관리자 페이지 
    def __init__(self, master):        
        tk.Frame.__init__(self, master)
        self.main_frame()
        self.bt_frame(master)

    def main_frame(self):
        main_screen(self,480,800)
        # stk.Frame.configure(self,bg='blue')
        tk.Label(self, text="관리자모드", font=('Helvetica', 18, "bold")).place(relx=0.4, rely=0, height = 50, width = 135)

    def bt_frame(self,master):
        rel_x,rel_y = 0.05,0.08
        def view_robot(self):#로봇의 속도 
            r_speed = str(r_scale.get())           
            l_r.config(text = "로봇의 속도 : " + r_speed)
        def view_volume(self):#로봇의 속도 
            r_volume = str(v_scale.get())          
            l_v.config(text = "시스템 볼륨 : " + r_volume)
            fm.Func_Class.volume_speak(v_scale.get())

        tk.Button(self, text="메인페이지",
                  command=lambda: master.switch_frame(StartPage)).place(relx=0.85, rely=0, height = 50, width = 135)
        #로봇 속도 조정
        l_r = tk.Label(self, text = "로봇의 속도 : 0")
        l_r.place(relx = rel_x, rely = rel_y + 0.04)        
        r_scale = tk.Scale(self, variable = tkinter.IntVar, orient='horizontal', command=view_robot,showvalue=False, tickinterval=20, to=100, length=300)
        r_scale.place(relx = rel_x + 0.13, rely = rel_y + 0.04)
        #시스템 볼륨 조정
        l_v = tk.Label(self, text = "시스템 볼륨 : 0")
        l_v.place(relx = rel_x, rely = rel_y + 0.14)
        v_scale = tk.Scale(self, variable = tkinter.IntVar, orient='horizontal',command=view_volume,showvalue=False, tickinterval=20, to=100, length=300)
        v_scale.place(relx = rel_x + 0.13, rely = rel_y + 0.14)
        
if __name__ == "__main__":
    app = SampleApp()
    app.title('test입니다.')
    
    
    app.mainloop()