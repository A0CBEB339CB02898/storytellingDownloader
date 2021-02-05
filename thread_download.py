from downloadCore import downloadCore
import threading
class thread_download():
    def __init__(self,var_option_start_int,var_option_end_int,var_album_num_str,var_save_path_str,var_filename_prefix_str):
        self.var_option_start_int=var_option_start_int
        self.var_option_end_int=var_option_end_int
        self.var_album_num_str=var_album_num_str
        self.var_save_path_str=var_save_path_str
        self.var_filename_prefix_str=var_filename_prefix_str
        # self.thread_it()
    #多线程下载
    #todo 一条主线程分发任务 4条线程下载文件 反馈进度条与文件大小等数据
    def thread_it(self):
        dowloader=downloadCore()
        # 线程1
        thread1 = threading.Thread(target=dowloader.download,args=(self.var_option_start_int,self.var_option_end_int,self.var_album_num_str,self.var_save_path_str,self.var_filename_prefix_str))
        thread1.setDaemon(True) 
        thread1.start()
        print("线程1启动")

        # thread1.join()
        # print("线程1关闭")