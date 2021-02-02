from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askdirectory

import io
from PIL import Image, ImageTk
from urllib.request import urlopen

from downloadCore import downloadCore
import time

import requests
class GUI():
    window = Tk()  # 创建顶层窗口
    downlader=downloadCore()
    var_album_num_text=""
    is_all_episode = StringVar()
    var_option_start = StringVar()
    var_option_end = StringVar()

    frame1 = Frame(window,height = 450,width = 600)
    frame2 = Frame(window,height = 450,width = 600)
    def __init__(self):
        self.init_Window()
        self.first_interface()
        # self.window.mainloop()

    def init_Window(self):#初始化窗口
        self.window.title('粤语评书下载器')
        screen_width = self.window.winfo_screenwidth()  # 屏幕尺寸
        screen_height = self.window.winfo_screenheight()
        window_width, window_height = 600, 450
        x, y = (screen_width - window_width) / 2, (screen_height - window_height) / 3
        size = '%dx%d+%d+%d' % (window_width, window_height, x, y)
        self.window.geometry(size)  # 初始化窗口大小
        self.window.resizable(False, False)  # 窗口长宽不可变
        # window.maxsize(600, 450)
        # window.minsize(300, 240)

    def first_interface(self):
        #第一页界面
        # print("打开第一个页面")

        self.frame1.pack(side='left')
        label_album_num = Label(self.frame1, text='请输入作品编号', cursor='xterm',font=("微软雅黑", 12))
        self.var_album_num_text = StringVar()
        entry_album_num = Entry(self.frame1, relief=RAISED, fg='gray', bd=2, width=58,textvariable=self.var_album_num_text, cursor='xterm')
        button_to_2step=Button(self.frame1, text='下一步',command=self.second_interface,height=1, width=15, relief=RAISED, bd=4, activebackground='gray',
                      activeforeground='white', cursor='hand2',font=("微软雅黑", 12))
        
        #界面布局
        label_album_num.place(relx=0.12, rely=0.12, anchor=CENTER)
        entry_album_num.place(relx=0.56, rely=0.12, anchor=CENTER)
        button_to_2step.place(relx=0.80, rely=0.30, anchor=CENTER)


    def second_interface(self):
        #清空页面
        self.frame1.destroy()
        #请求专辑信息
        self.downlader.get_album_info(self.var_album_num_text.get())

        #第二页界面
        # self.frame2.grid(row=0,column=0,rowspan=3,columnspan=4)
        self.frame2.pack(padx=20, pady=20,fill=BOTH)

        img_url=self.downlader.pic_url

        # image_bytes = urlopen(img_url).read() #这个太慢了
        #图片label
        image_bytes =requests.get(img_url).content
        data_stream = io.BytesIO(image_bytes)
        pil_image = Image.open(data_stream)
        #缩小图片
        w,h=pil_image.size
        pil_image=pil_image.resize((int(w/2), int(h/2)), Image.ANTIALIAS)
       
        tk_image=ImageTk.PhotoImage(pil_image) 

        label_album_pic = Label(self.frame2, image=tk_image, cursor='xterm')
         #置入图片
        label_album_pic.image=tk_image
        #布局
        label_album_pic.grid(row=0,column=0)


        #标题与信息
        label_album_title = Label(self.frame2, text=self.downlader.title, cursor='xterm',font=("微软雅黑", 18))
        label_album_info = Label(self.frame2, text=self.downlader.detailed_info, cursor='xterm',anchor='w',font=("微软雅黑", 10))
        # label_cut_off = Label(self.frame2, text="——————————————————————————————————————————————————————————————————————————", cursor='xterm',anchor='w',font=("微软雅黑", 10))
        #界面布局
        label_album_title.grid(row=0,column=1,rowspan=2,padx=10,pady=10,sticky = N)
        label_album_info.grid(row=0,column=1,padx=10,sticky = S)
        # label_cut_off.grid(row=1,column=1,padx=10,sticky = S)
        #集数选项卡label
        label_start_episode=Label(self.frame2, text="请选择开始的集数", cursor='xterm',font=("微软雅黑", 12))
        label_end_episode=Label(self.frame2, text="请选择结束的集数", cursor='xterm',font=("微软雅黑", 12))
        #界面布局
        label_start_episode.grid(row=2,column=0,sticky = E)
        label_end_episode.grid(row=3,column=0,sticky = E)

        #集数选项卡start
        episode_options = [1]
        #总集数注入option
        for i in range(int(self.downlader.str_total_episode_num)):
            if i==0:
                pass
            else:
                episode_options.append(i+1)

        self.var_option_start.set(episode_options[0])
        option_start = OptionMenu(self.frame2, self.var_option_start, *episode_options,command=self.select_part_episode,font=("微软雅黑", 10))
        #界面布局
        option_start.grid(row=2,column=1,padx=10,sticky = W)

        #集数选项卡end
        self.var_option_end.set(episode_options[len(episode_options)-1])
        option_end = OptionMenu(self.frame2, self.var_option_end, *episode_options,command=self.select_part_episode,font=("微软雅黑", 10))
        #界面布局
        option_end.grid(row=3,column=1,padx=10,sticky = W)

        #全部集数复选框
        check=Checkbutton(self.frame2, text = "下载全部", variable = self.is_all_episode,onvalue = 'T', offvalue = 'F',command=self.select_all_episode,font=("微软雅黑", 12))
        check.select()
        #界面布局
        check.grid(row=3,column=2,sticky = S)
        
        #下载按钮
        button_to_3step=Button(self.frame2, text='确定',command=self.third_interface,height=1, width=15, relief=RAISED, bd=4, activebackground='gray',
                activeforeground='white', cursor='hand2',font=("微软雅黑", 12))
        button_to_3step.grid(row=4,column=2)

    #更新复选框与option框的状态
    def select_all_episode(self):
        self.var_option_start.set(1)
        self.var_option_end.set(self.downlader.str_total_episode_num)
    def select_part_episode(self,episode):
        self.is_all_episode.set('F')
        

    def third_interface(self):
        print(self.is_all_episode.get())
        print(self.var_option_start.get())
        print(self.var_option_end.get())
        




g=GUI()
# g.var_album_num_text
