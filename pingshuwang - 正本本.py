import requests
from urllib import request
import os
import threading
from tqdm import tqdm,trange

# filename_suffix = "回.mp3"

# root_url="http://www.zgpingshu.com/playdata/"



def download(start_episode_num,max_episode_num,program,save_path,filename_prefix,filename_suffix = "回.mp3",root_url="http://www.zgpingshu.com/playdata/"):
    '''
    下载
    start_episode_num:int 起始集数
    max_episode_num:int 结束集数
    program:str 节目编号，对应网站上的节目编号
    save_path:str 保存路径
    filename_prefix: 文件前缀，多数时候为节目名
    filename_suffix:str="回.mp3"
    root_url:str="http://www.zgpingshu.com/playdata/"
    '''
    #创建目录
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    diff=max_episode_num-start_episode_num+1

    # print("开始下载:",start_episode_num,"-",max_episode_num)

    # while start_episode_num<=max_episode_num:
    for i in tqdm(range(diff)):
        episode = start_episode_num
        

        #第一集的路径与其他不同
        if episode==1:
            url=root_url+program
        else:
            url=root_url+program+'/'+str(episode)+".html"

        r=requests.post(url)
        url=r.json()['urlpath']
        #结尾转换
        # url=url.replace('.flv','.mp3')

        #计算文件名
        if start_episode_num<10:
            episode_name="00"+str(episode)
        elif 10<=start_episode_num<100:
            episode_name="0"+str(episode)
        elif start_episode_num>=100:
            episode_name=str(episode)

        #定义文件名
        filename = filename_prefix + episode_name + filename_suffix

        #下载
        request.urlretrieve(url,save_path+filename)
        start_episode_num=start_episode_num+1

def distribute(min,max,copies=4):
    '''
    多线程分发
    min:较小数
    max:较大数
    cooies:份数
    :return list
    '''
    if max<min:
        temp=max
        max=min
        min=temp
    diff=int(((max-min)+1)/copies)
    i=0
    res=[]
    while i<copies-1:
        res.append(min+(i+1)*diff)
        i=i+1
    return res

def thr(start_episode_num,max_episode_num,program,save_path,filename_prefix):
    '''
    多线程
    '''
    print("开始下载:",start_episode_num,"-",max_episode_num)
    dis=distribute(start_episode_num,max_episode_num)
    # 线程1
    thread1 = threading.Thread(target=download,args=(start_episode_num,dis[0],program,save_path,filename_prefix,))
    thread1.start()
    # print("线程1启动")
    # 线程2
    thread2 = threading.Thread(target=download,args=(dis[0]+1,dis[1],program,save_path,filename_prefix,))
    thread2.start()
    # print("线程2启动")

    # 线程3
    thread3 = threading.Thread(target=download,args=(dis[1]+1,dis[2],program,save_path,filename_prefix,))
    thread3.start()
    # print("线程3启动")

    # 线程4
    thread4 = threading.Thread(target=download,args=(dis[2]+1,max_episode_num,program,save_path,filename_prefix,))
    thread4.start()
    # print("线程4启动")
    thread1.join()
    # print("线程1关闭")
    thread2.join()
    # print("线程2关闭")
    thread3.join()
    # print("线程3关闭")
    thread4.join()
    # print("线程4关闭")
    print("所有线程关闭")
    print("下载完成:",start_episode_num,"-",max_episode_num)

if __name__ == "__main__":
    #起始集数
    start_episode_num=1
    #最大集数
    max_episode_num=10
    #节目编号
    program="3084"
    # 保存路径
    save_path='D:/protect/文档/Python/听书/粤语评书杨家将(138回版)/'
    # # 保存前缀
    filename_prefix="粤语评书杨家将(138回版)"   

    thr(start_episode_num,max_episode_num,program,save_path,filename_prefix)