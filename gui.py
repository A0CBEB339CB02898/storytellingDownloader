from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askdirectory
import tkinter.messagebox 

import io
from PIL import Image, ImageTk
from urllib.request import urlopen
import threading

# from thread_download import thread_download
from downloadCore import downloadCore
from distributor import distributor
import time

import requests
class GUI(): 
    def __init__(self):
        # self.init_Window()
        # self.first_interface()
        self.window = Tk()  # 创建顶层窗口
        self.window.protocol('WM_DELETE_WINDOW', self.customized_window_destory_function)#自定义结束窗口的操作 
        
        self.infoGetter=downloadCore(False)
        self.var_album_num_text=""
        self.is_all_episode = StringVar()
        self.var_option_start = StringVar()
        self.var_option_end = StringVar()
        # var_save_path = StringVar()
        self.var_filename_prefix = StringVar()
        self.var_save_path = StringVar()
           
        self.frame1 = Frame(self.window,height = 530,width = 600)
        self.frame2 = Frame(self.window,height = 530,width = 600)
        self.frame3 = Frame(self.window,height = 530,width = 600)
        # self.third_interface()

    def init_Window(self):#初始化窗口
        self.window.title('粤语评书下载器')
        screen_width = self.window.winfo_screenwidth()  # 屏幕尺寸
        screen_height = self.window.winfo_screenheight()
        window_width, window_height = 600, 530
        x, y = (screen_width - window_width) / 2, (screen_height - window_height) / 3
        size = '%dx%d+%d+%d' % (window_width, window_height, x, y)
        self.window.geometry(size)  # 初始化窗口大小
        # self.window.resizable(False, False)  # 窗口长宽不可变
        # window.maxsize(600, 450)
        # window.minsize(300, 240)
    
    #自定义关闭窗口函数
    def customized_window_destory_function(self):
        if 'self.thread_main_downloader' in vars():
            #似乎是无效的 但是没影响功能
            print("主下载线程对象关闭")
            self.thread_main_downloader.join()
        #关闭窗口停止标识
        self.main_stop_flag=True
        self.frame1.destroy()
        self.frame2.destroy()
        self.frame3.destroy()
        self.window.destroy()
        print("窗口关闭")

    def first_interface(self):
        #第一页界面
        # print("打开第一个页面")
        self.frame1.pack(side='left')
        label_album_num = Label(self.frame1, text='请输入作品编号', cursor='xterm',font=("微软雅黑", 12))
        self.var_album_num_text = StringVar()
        entry_album_num = Entry(self.frame1, relief=SOLID, fg='black', bd=1,width=40,textvariable=self.var_album_num_text, cursor='xterm',font=("微软雅黑", 12))
        button_to_2step=Button(self.frame1, text='下一步',command=self.first_2_second_is_legal_input,height=1, width=15, relief=RAISED, bd=4, activebackground='gray',
                      activeforeground='white', cursor='hand2',font=("微软雅黑", 12))
        
        #界面布局
        label_album_num.place(relx=0.12, rely=0.12, anchor=CENTER)
        entry_album_num.place(relx=0.56, rely=0.12, anchor=CENTER)
        button_to_2step.place(relx=0.80, rely=0.30, anchor=CENTER)

    #窗口跳转前的数据输入合法性检验
    def first_2_second_is_legal_input(self):
        if(self.var_album_num_text.get()==""):
            tkinter.messagebox.showerror('错误','请输入作品编号！')
            self.first_interface()
        else:
            try:
                #请求专辑信息
                self.infoGetter.get_album_info(self.var_album_num_text.get())

                self.second_interface()
            except AttributeError as entry_album_num_error:
                tkinter.messagebox.showerror('错误','未获取到专辑信息')
                print(entry_album_num_error)
            except requests.exceptions.ReadTimeout as time_out_error:
                tkinter.messagebox.showerror('错误','连接超时')
                print(time_out_error)
            
    def second_interface(self):

        #清空页面
        self.frame1.destroy()


        #第二页界面
        # self.frame2.grid(row=0,column=0,rowspan=3,columnspan=4)
        self.frame2.pack(padx=20, pady=30,fill=BOTH)

        img_url=self.infoGetter.pic_url

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
        label_album_title = Label(self.frame2, text=self.infoGetter.title, cursor='xterm',font=("微软雅黑", 18))
        label_album_info = Label(self.frame2, text=self.infoGetter.detailed_info, cursor='xterm',anchor='w',font=("微软雅黑", 10))
        label_cut_off = Label(self.frame2, text="—————————————————————————————————————", cursor='xterm',anchor='w',font=("微软雅黑", 10))
        #界面布局
        label_album_title.grid(row=0,column=1,columnspan=2,padx=10,pady=10,sticky = N)
        label_album_info.grid(row=0,column=1,columnspan=2,padx=10,sticky = S)
        label_cut_off.grid(row=1,column=0,columnspan=3,sticky = S)
        #集数选项卡label
        label_start_episode=Label(self.frame2, text="请选择开始的集数", cursor='xterm',font=("微软雅黑", 12))
        label_end_episode=Label(self.frame2, text="请选择结束的集数", cursor='xterm',font=("微软雅黑", 12))
        #界面布局
        label_start_episode.grid(row=2,column=0,pady=10,sticky = W)
        label_end_episode.grid(row=3,column=0,sticky = W)

        #集数选项卡start
        episode_options = [1]
        #总集数注入option
        for i in range(int(self.infoGetter.str_total_episode_num)):
            if i==0:
                pass
            else:
                episode_options.append(i+1)

        self.var_option_start.set(episode_options[0])
        option_start = OptionMenu(self.frame2, self.var_option_start, *episode_options,command=self.select_part_episode)
        #界面布局
        option_start.grid(row=2,column=1,padx=10,sticky = W)

        #集数选项卡end
        self.var_option_end.set(episode_options[len(episode_options)-1])
        option_end = OptionMenu(self.frame2, self.var_option_end, *episode_options,command=self.select_part_episode)
        #界面布局
        option_end.grid(row=3,column=1,padx=10,sticky = W)

        #全部集数复选框
        check=Checkbutton(self.frame2, text = "下载全部", variable = self.is_all_episode,onvalue = 'T', offvalue = 'F',command=self.select_all_episode,font=("微软雅黑", 12))
        check.select()
        #界面布局
        check.grid(row=2,column=2,sticky = S)
        

        #保存路径相关label
        label_filename_prefix=Label(self.frame2, text="文件前缀", cursor='xterm',font=("微软雅黑", 12))
        label_file_save_path=Label(self.frame2, text="保存路径", cursor='xterm',font=("微软雅黑", 12))
        #界面布局
        label_filename_prefix.grid(row=4,column=0,pady=10,sticky = W)
        label_file_save_path.grid(row=5,column=0,sticky = W)
        
        #保存路径相关entry
        self.var_filename_prefix.set(self.var_filename_prefix_handle(self.infoGetter.title,self.infoGetter.author))
        entry_filename_prefix = Entry(self.frame2, relief=SOLID, fg='black', bd=1,width=49,textvariable=self.var_filename_prefix, cursor='xterm',font=("微软雅黑", 12))
        entry_file_save_path = Entry(self.frame2, relief=SOLID, fg='black', bd=1,width=38,textvariable=self.var_save_path, cursor='xterm',font=("微软雅黑", 12))

        #界面布局
        entry_filename_prefix.grid(row=4,column=0,columnspan=3,pady=10,sticky = E)
        entry_file_save_path.grid(row=5,column=0,columnspan=3,padx=100,sticky = E)

        #选择路径按钮
        button_choice = Button(self.frame2, relief=RAISED, text='打开', bd=4, width=10, height=1, command=self.select_path, activeforeground='white', cursor='hand2',font=("微软雅黑", 9))
        #界面布局
        button_choice.grid(row=5,column=2,pady=3,sticky = E)

        #下载按钮
        self.button_to_3step=Button(self.frame2, text='下一步',command=self.second_2_third_is_legal_input,height=1, width=15, relief=RAISED, bd=4, activebackground='gray',
                activeforeground='white', cursor='hand2',font=("微软雅黑", 12))
        #界面布局
        self.button_to_3step.grid(row=6,pady=20,column=2,sticky = E)

    #更新复选框与option框的状态
    def select_all_episode(self):
        self.var_option_start.set(1)
        self.var_option_end.set(self.infoGetter.str_total_episode_num)
    def select_part_episode(self,episode):
        self.is_all_episode.set('F')
    def select_path(self):
        path_ = askdirectory()
        #path:选择的路径/文件前缀文件夹
        self.var_save_path.set(path_+"/"+self.var_filename_prefix_handle(self.infoGetter.title,self.infoGetter.author)+"/")

    #文件前缀处理
    def var_filename_prefix_handle(self,title,author):
        # return title.replace("粤语评书","")+"-"+author
        self.var_filename_prefix.set(title)
        return title
    
    #窗口跳转前的数据合法性检验
    def second_2_third_is_legal_input(self):
        if self.var_save_path.get()=="":
            tkinter.messagebox.showerror('错误','请选择保存路径')
        elif self.var_save_path.get()=="":
            tkinter.messagebox.showerror('错误','请输入文件保存前缀')
        else:
            self.third_interface()

    def third_interface(self):
        #清空页面
        self.frame2.destroy()

        #第三页界面
        self.frame3.pack(padx=20, pady=20,fill=BOTH)

        # 下载进度(标签，进度条，进度条里的已下载大小和总大小，下载速度，剩余时间)
        progress_label = Label(self.frame3, text='下载进度', cursor='xterm',font=("微软雅黑", 12))
        progress_label.grid(row=0,column=0,pady=20,columnspan=2,sticky = W)

        # 进度条大小
        self.progress_bar_width=90
        self.progress_bar_height=20



        #进度条1
        label_cavas1=Label(self.frame3, text='线程1', cursor='xterm',font=("微软雅黑", 9))
        label_cavas1.grid(row=1,column=0)
        self.canvas1 = Canvas(self.frame3, width=self.progress_bar_width, height=self.progress_bar_height, bg="white")
        self.canvas1.grid(row=1,column=1,padx=2)
        # 进度条填充
        self.out_rec1 = self.canvas1.create_rectangle(0, 0, self.progress_bar_width, self.progress_bar_height, outline="white", width=1)
        self.fill_rec1 = self.canvas1.create_rectangle(0, 0, 0, 0, outline="", width=0, fill="green")

        # 进度条2
        label_cavas2=Label(self.frame3, text='线程2', cursor='xterm',font=("微软雅黑", 9))
        label_cavas2.grid(row=1,column=2)
        self.canvas2 = Canvas(self.frame3, width=self.progress_bar_width, height=self.progress_bar_height, bg="white")
        self.canvas2.grid(row=1,column=3,padx=2)
        # 进度条填充
        out_rec2 = self.canvas2.create_rectangle(0, 0, self.progress_bar_width, self.progress_bar_height, outline="white", width=1)
        self.fill_rec2 = self.canvas2.create_rectangle(0, 0, 0, 0, outline="", width=0, fill="green")

        # 进度条3
        label_cavas3=Label(self.frame3, text='线程3', cursor='xterm',font=("微软雅黑", 9))
        label_cavas3.grid(row=1,column=4)
        self.canvas3 = Canvas(self.frame3, width=self.progress_bar_width, height=self.progress_bar_height, bg="white")
        self.canvas3.grid(row=1,column=5,padx=2)
        # 进度条填充
        out_rec3 = self.canvas3.create_rectangle(0, 0, self.progress_bar_width, self.progress_bar_height, outline="white", width=1)
        self.fill_rec3 = self.canvas3.create_rectangle(0, 0, 0, 0, outline="", width=0, fill="green")

        # 进度条4
        label_cavas4=Label(self.frame3, text='线程4', cursor='xterm',font=("微软雅黑", 9))
        label_cavas4.grid(row=1,column=6)
        self.canvas4 = Canvas(self.frame3, width=self.progress_bar_width, height=self.progress_bar_height, bg="white")
        self.canvas4.grid(row=1,column=7,padx=2)
        # 进度条填充
        out_rec4 = self.canvas4.create_rectangle(0, 0, self.progress_bar_width, self.progress_bar_height, outline="white", width=1)
        self.fill_rec4 = self.canvas4.create_rectangle(0, 0, 0, 0, outline="", width=0, fill="green")

        #总进度条
        label_cavas_total=Label(self.frame3, text='总进度', cursor='xterm',font=("微软雅黑", 9))
        label_cavas_total.grid(row=2,column=0,pady=30)
        self.canvas_total = Canvas(self.frame3, width=self.progress_bar_width*4, height=self.progress_bar_height, bg="white")
        self.canvas_total.grid(row=2,column=1,columnspan=7,pady=30,padx=10,sticky = W)
        # 进度条填充
        out_rec_total = self.canvas_total.create_rectangle(0, 0, self.progress_bar_width*4, self.progress_bar_height, outline="white", width=1)
        self.fill_rec_total = self.canvas_total.create_rectangle(0, 0, 0, 0, outline="", width=0, fill="green")

        #下载集数进度label
        self.var_finish_episode_text  = StringVar()
        # self.var_finish_episode_text.set("20/100")
        finish_episode = Label(self.frame3, textvariable=self.var_finish_episode_text, cursor='xterm',)
        finish_episode.grid(row=2,column=7,sticky=W)
        

        # 可滚动的多行文本区域
        self.scrolled_text = ScrolledText(self.frame3, relief=GROOVE, bd=4, height=12, width=55, cursor='xterm',font=("微软雅黑", 11))
        self.scrolled_text.grid(row=3,column=0,columnspan=8)

        #暂停开始按钮
        self.button_start_pause=Button(self.frame3, text='开始',command=self.start_download,height=1, width=10, relief=RAISED, bd=4, activebackground='gray',
                activeforeground='white', cursor='hand2',font=("微软雅黑", 12))
        #界面布局
        self.button_start_pause.grid(row=4,column=6,pady=10,columnspan=3)
        
        self.window.mainloop()

    #已经开始下载时点解开始下载按钮展示对话框    
    def show_already_start(self):
        tkinter.messagebox.showinfo('提示','下载已开始')

    def start_download(self):
        #暂停开始按钮
        self.button_start_pause=Button(self.frame3, text='下载中...',command=self.show_already_start,height=1, width=10, relief=RAISED, bd=4, activebackground='gray',
                activeforeground='white', cursor='hand2',font=("微软雅黑", 12))
        #界面布局
        self.button_start_pause.grid(row=4,column=6,pady=10,columnspan=3)

        self.thread_main_downloader=threading.Thread(target=self.main_downloader,args=())
        self.thread_main_downloader.setDaemon(True)
        # '开始下载' + self.infoGetter.title.get()+self.var_option_start.get()+"至"+self.var_option_end.get()+"回"
        self.scrolled_text.insert(INSERT, "开始下载:{} {} 至 {} 回".format(self.infoGetter.title,self.var_option_start.get(),self.var_option_end.get()) + '\n')
        self.thread_main_downloader.start()
        
    def main_downloader(self):
        #关闭窗口停止标识
        self.main_stop_flag=False
        dowloader1=downloadCore(False)
        dowloader2=downloadCore(False)
        dowloader3=downloadCore(False)
        dowloader4=downloadCore(False)
        dis=distributor(int(self.var_option_start.get()),int(self.var_option_end.get()))
        self.download_finish_episode_int=0
        thread_main_schedule= threading.Thread(target=self.change_main_schedule,args=())

        thread_schedule1= threading.Thread(target=self.change_schedule,args=(self.canvas1,self.fill_rec1,dowloader1))
        thread_schedule2= threading.Thread(target=self.change_schedule,args=(self.canvas2,self.fill_rec2,dowloader2))
        thread_schedule3= threading.Thread(target=self.change_schedule,args=(self.canvas3,self.fill_rec3,dowloader3))
        thread_schedule4= threading.Thread(target=self.change_schedule,args=(self.canvas4,self.fill_rec4,dowloader4))


        thread_download1 = threading.Thread(name="thread_download1",target=self.assistant_downloader,args=(dowloader1,dis,"thread_download1"))
        thread_download2 = threading.Thread(name="thread_download2",target=self.assistant_downloader,args=(dowloader2,dis,"thread_download2"))
        thread_download3 = threading.Thread(name="thread_download3",target=self.assistant_downloader,args=(dowloader3,dis,"thread_download3"))
        thread_download4 = threading.Thread(name="thread_download4",target=self.assistant_downloader,args=(dowloader4,dis,"thread_download4"))
        

        th_download = [thread_download1,thread_download2,thread_download3,thread_download4]
        th_schedule =[thread_schedule1,thread_schedule2,thread_schedule3,thread_schedule4]
        
        th =th_schedule + th_download
        th.append(thread_main_schedule)
        for t in th:
            t.setDaemon(True)
            print(t.name+" start")
            t.start()
            # t.join()
            # print(t.name+"join")

        #主线程监控
        while True:
            if dis.get_should_download_episode(False)==None \
                and dowloader1.get_is_finish() \
                and dowloader2.get_is_finish() \
                and dowloader3.get_is_finish() \
                and dowloader4.get_is_finish():

                self.scrolled_text.insert(INSERT, "所有任务下载完成" + '\n')
                self.scrolled_text.see(END)
                break
        

    def assistant_downloader(self,dowloader:downloadCore,dis:distributor,thr_name):
        flag=True
        while flag:
            should_download_episode_num=dis.get_should_download_episode(True)#获取本线程的下载任务
            if should_download_episode_num==None:
                flag=False
                break
            

            print(thr_name+" downloading "+str(should_download_episode_num))

            self.scrolled_text.insert(INSERT, '正在下载 ' + str(should_download_episode_num) +"..."+ '\n')

            dowloader.download(should_download_episode_num,should_download_episode_num,self.var_album_num_text.get(),self.var_save_path.get(),self.var_filename_prefix.get())
            #关闭窗口停止标识
            if self.main_stop_flag==True:
                break
            self.download_finish_episode_int=self.download_finish_episode_int+1#主进度条标记
            self.scrolled_text.insert(INSERT, "{}{}回.mp3 下载完成".format(self.var_filename_prefix.get(),should_download_episode_num) + '\n')
            self.scrolled_text.see(END)
        #下载器下载完成标识
        dowloader.set_is_finish(True)
        print(thr_name+" stop")


    # 小进度条实现方法
    def change_schedule(self,canvas:Canvas,fill_rec,downloader:downloadCore):
        print("进度条start")
        while downloader.get_is_finish()==False:
            now_size = downloader.data_block_size*downloader.download_data_block
            total_size = downloader.file_size
            while now_size < total_size or (now_size==0 and total_size==0):
                now_size=downloader.download_data_block*downloader.data_block_size
                total_size=downloader.file_size
                # print(now_size)
                # print(total_size)
                if now_size==total_size and total_size!=0:
                    break
                #关闭窗口停止标识
                if self.main_stop_flag==True:
                    return

                if now_size==0&total_size==0:
                    # canvas.delete("t1")
                    # canvas.coords(out_rec1, (0, 0, 90, 20))
                    # self.frame3.update()
                    continue
                else:
                    try:
                        # 文件大小进度
                        time.sleep(0.01)
                        canvas.delete("t1")
                        size_text = '%.2f' % (now_size / 1024 / 1024) + '/' + '%.2f' % (total_size / 1024 / 1024) + 'MB'
                        canvas.create_text(45, 10, text=size_text, tags="t1")

                        # 进度条更新
                        canvas.coords(fill_rec, \
                                (0, 0, 5 + (now_size / total_size) * self.progress_bar_width, \
                                self.progress_bar_height))
                        self.frame3.update()

                        # if round(now_size / total_size * 100, 2) == 100.00:
                        #     time_text = "%02d:%02d:%02d" % (0,0,0)
                        #     remain_time.set(time_text)
                        #     speed.set("完成")
                        #     button_start['text'] = "开始"

                    except ZeroDivisionError as z:
                        self.scrolled_text.insert(INSERT, '出错啦：' + str(z) + '\n')
                    # button_start['text'] = "重新开始"
            canvas.delete("t1")
            canvas.coords(fill_rec, (0, 0, 0, 0))
        print("进度条stop")
        
            # 小进度条实现方法
    
    #大进度条实现方法
    def change_main_schedule(self):
        print("主进度条start")
        need_download_total_episode=int(self.var_option_end.get())-int(self.var_option_start.get())+1
        
        while self.download_finish_episode_int<need_download_total_episode:

            #关闭窗口停止标识
            if self.main_stop_flag==True:
                return

            # 文件大小进度
            time.sleep(0.01)

            # 进度条更新
            self.canvas_total.coords(self.fill_rec_total, \
                (0, 0, 5 + (self.download_finish_episode_int / need_download_total_episode) * self.progress_bar_width*4, \
                    self.progress_bar_height))
            self.var_finish_episode_text.set(str(self.download_finish_episode_int)+"/"+ str(need_download_total_episode))
            self.frame3.update()


        self.canvas_total.coords(self.fill_rec_total, \
            (0, 0, self.progress_bar_width*4, \
                self.progress_bar_height))
        self.var_finish_episode_text.set("下载完成")
        print("主进度条stop")


# if __name__ == "__main__":
#     g=GUI()
#     g.first_interface()


g=GUI()
g.init_Window()
g.first_interface()

