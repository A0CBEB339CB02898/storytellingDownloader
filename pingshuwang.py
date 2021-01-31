import requests
from urllib import request


def cbk(a,b,c):  
    '''''回调函数 
    @a:已经下载的数据块 
    @b:数据块的大小 
    @c:远程文件的大小 
    '''  
    per=100.0*a*b/c  
    if per>100:  
        per=100  
    print('%.2f%%' % per)

#起始集数
start_episode_num=1
#最大集数
max_episode_num=10
#节目编号
program="3084"
# 保存路径(手动创建)
save_path='D:/protect/文档/Python/听书/粤语评书杨家将(138回版)/'
# 保存名
filename_prefix="粤语评书杨家将(138回版)"
filename_suffix = "回.mp3"

root_url="http://www.zgpingshu.com/playdata/"

while start_episode_num<=max_episode_num:
    episode= start_episode_num
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
    elif 10<start_episode_num<100:
        episode_name="0"+str(episode)
    elif start_episode_num>100:
        episode_name=str(episode)

    #定义文件名
    filename = filename_prefix + episode_name + filename_suffix
    request.urlretrieve(url,save_path+filename,cbk)
    start_episode_num = start_episode_num + 1
print("内容下载完成")

