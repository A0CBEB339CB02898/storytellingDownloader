import requests
from urllib import request
from bs4 import BeautifulSoup
import os
import re

import threading

class downloadCore():
    title=""
    author=""
    pic_url=""
    detailed_info=""
    str_total_episode_num=""
    album_num=""


    download_data_block=0
    data_block_size=0
    file_size=0

    def __init__(self,is_finish):
        self.is_finish=is_finish
    #获取专辑信息
    def get_album_info(self,album_page_url):
        # album_page_url="http://yueyu.zgpingshu.com/"+album_num#测试时注释 #已舍弃
        #请求页面
        r=requests.get(album_page_url,timeout=5)#测试时注释
        r.encoding = r.apparent_encoding#测试时注释
        

        # #测试用
        # path = 'C:/Users/Orion/Desktop/private/代码/storytellingSpider/1.html'
        # htmlfile = open(path, 'r', encoding='utf-8')
        # htmlhandle = htmlfile.read()
        # soup = BeautifulSoup(htmlhandle,"html.parser")

        # #解析数据
        try:
            url_split=re.split(r'/',album_page_url)
            self.album_num=url_split[len(url_split)-2]

            soup = BeautifulSoup(r.text,"html.parser") #测试时注释

            self.title=soup.select_one('#categoryHeader>h1').get_text()
            
            self.pic_url=soup.select_one('.pingshupic>img').get('src')
            
            self.detailed_info=""
            self.str_total_episode_num=""

            for info in soup.select('.pingshulist>ul>li'):
                if info.string==None:
                    # info.span.a.string
                    try:
                        if info.span.a.string!='':
                            self.author=info.span.a.string
                        elif info.a.string!='':
                            self.author=info.a.string
                    except AttributeError as e:
                        self.author=re.split(r'([评书])',self.title)[0]

                    self.detailed_info+=(info.next_element + self.author +'\n')
                else:
                    # print(info.string)
                    self.detailed_info+=(info.string + '\n')

                    if re.match( "长度", info.string):
                        for i in re.findall("\\d",info.string): #用正则表达式匹配所有数字
                            self.str_total_episode_num+=i 
        except:
            self.title=""


    #获取下载文件大小
    def get_file_size(self,url):
        try:
            file_size = int(requests.head(url, allow_redirects=True).headers['Content-Length']) # 获取下载文件大小
            return file_size
        except:
            return None
    
    #回调函数 反馈下载进度
    def cbk(self,a,b,c):  
        '''''回调函数 
        @a:已经下载的数据块 
        @b:数据块的大小 
        @c:远程文件的大小 
        '''  
        self.download_data_block=a
        self.data_block_size=b
        self.file_size=c
        
        # print("file_size"+str(self.file_size))
        # print("data_block_size"+str(self.data_block_size))
        # print("download_data_block"+str(self.download_data_block))
        per=100.0*a*b/c  
        if per>100:  
            per=100
        # print(per)

    #下载
    def download(self,start_episode_num,end_episode_num,program,save_path,filename_prefix,filename_suffix = "回.mp3",root_url="http://www.zgpingshu.com/playdata/"):
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
            url=url.replace('.flv','.mp3')

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
            request.urlretrieve(url,save_path+filename,self.cbk)
            start_episode_num=start_episode_num+1


    #下载器状态
    def set_is_finish(self,is_finish):
        self.is_finish=is_finish

    def get_is_finish(self):
        return self.is_finish



# if __name__ == "__main__":
    # g=downloadCore(False)
    # g.get_album_info("http://bjjt.zgpingshu.com/1250/")
    # # g.get_album_info("http://yueyu.zgpingshu.com/3082/")
    # g.title
    # g.author
    # g.detailed_info
    # g.pic_url
    # g.str_total_episode_num
