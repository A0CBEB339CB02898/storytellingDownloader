import threading
import time
class distributor():

  def __init__(self,start_episode_num,end_episode_num):
    self.start_episode_num=start_episode_num
    self.end_episode_num=end_episode_num

    self.should_download_episode_num=start_episode_num

    self.lock=threading.Lock()

  def get_should_download_episode(self,is_thread_get):
    #加锁
    self.lock.acquire()
    try :
      if self.should_download_episode_num<=self.end_episode_num:
        return self.should_download_episode_num
      else:
        return None
    finally :
      if is_thread_get==True:
        self.should_download_episode_num=self.should_download_episode_num+1
      else:
        pass
      #修改完成，释放锁
      self.lock.release()
  
def print_result(dis:distributor,thr):
  is_thread_get=True
  while is_thread_get:
    should_download_episode=dis.get_should_download_episode()
    if should_download_episode==None:
      is_thread_get=False
    print(str(should_download_episode)+" 线程"+thr)
  

# if __name__ == "__main__":
#     dis=distributor(20,30)
#     # dis.get_should_download_episode()
#     # print_result(dis,"1")
#     threading1=threading.Thread(target=print_result,args=(dis,"1"))
#     threading2=threading.Thread(target=print_result,args=(dis,"2"))
#     threading3=threading.Thread(target=print_result,args=(dis,"3"))
#     threading4=threading.Thread(target=print_result,args=(dis,"4"))
#     th = [threading1, threading2,threading3,threading4]
#     for t in th:
#         # t.setDaemon(True)
#         t.start()
#         # t.join()