import requests
from urllib import request
from bs4 import BeautifulSoup
import os
import re

class downloadCore():
    title=""
    pic_url=""
    album_info=""
    str_total_episode_num=""

    def get_album_info(self,album_num):
        album_page_url="http://yueyu.zgpingshu.com/"+album_num
        #请求页面
        r=requests.get(album_page_url,timeout=5)
        r.encoding = r.apparent_encoding
        

        
        #解析数据
        soup = BeautifulSoup(r.text,"html.parser")
        self.title=soup.select_one('#categoryHeader>h1').string
        self.pic_url=soup.select_one('.pingshupic>img').get('src')
        self.detailed_info=""
        self.str_total_episode_num=""
        for info in soup.select('.pingshulist>ul>li'):
            if info.string==None:
                # info.span.a.string
                # print(info.next_element + info.span.a.string)
                self.detailed_info+=(info.next_element + info.span.a.string +'\n')
            else:
                # print(info.string)
                self.detailed_info+=(info.string + '\n')

                if re.match( "长度", info.string):
                    for i in re.findall("\\d",info.string):
                        self.str_total_episode_num+=i  

g=downloadCore()
g.get_album_info("3090")
g.title

def download(start_episode_num,end_episode_num,program,save_path,filename_prefix,filename_suffix = "回.mp3",root_url="http://www.zgpingshu.com/playdata/"):
    '''
    下载
    start_episode_num:int 起始集数
    end_episode_num:int 结束集数
    program:str 节目编号，对应网站上的节目编号
    save_path:str 保存路径
    filename_prefix: 文件前缀，多数时候为节目名
    filename_suffix:str="回.mp3"
    root_url:str="http://www.zgpingshu.com/playdata/"
    '''
    #创建目录
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    diff=end_episode_num-start_episode_num+1

    # print("开始下载:",start_episode_num,"-",max_episode_num)

    # while start_episode_num<=max_episode_num:
    for i in range(diff):
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

    