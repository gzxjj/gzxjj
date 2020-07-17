from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re,json,time
import pandas as pd
import multiprocessing as mp
from multiprocessing import Process,freeze_support
data={}
data['Index']=[]
data['Name']=[]
data['Link']=[]
data['Torrent']=[]
ID={3:'最新合集',5:'亚洲无码',7:'欧美新片',110:'网摘收藏',18:'三级写真'}
id=5
StartPage=21
EndPage=22
basepage="http://k5.7086xz.rocks/pw/"
webpage ="thread.php?fid="+str(id)+"&page="
i = 0
def Download(page):
    global i,data
    url=basepage+webpage+str(page)
    print('url is: ',url)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html=urlopen(req).read().decode('utf-8')
    soup=BeautifulSoup(html,features='lxml')
    all_href=soup.find_all('h3')
    subpageurl = [(l.get_text(),l.find('a').get('href')) for l in all_href]
    for title,sub in subpageurl:
        suburl=basepage+sub
        subreq = Request(suburl, headers={'User-Agent': 'Mozilla/5.0'})
        subhtml = urlopen(subreq).read().decode('utf-8')
        subsoup = BeautifulSoup(subhtml, features='lxml')
        sub_href = subsoup.find('div',{'class':'f14','id':'read_tpc'})
        if sub_href!=None:
            a = sub_href.find_all('a')
            for s in a:
                if("https://www" in s.get_text()):
                    torrenturl=s.get_text()
                    torrentreq=Request(torrenturl, headers={'User-Agent': 'Mozilla/5.0'})
                    torrenthtml = urlopen(torrentreq).read().decode('utf-8')
                    torrentsoup = BeautifulSoup(torrenthtml, features='lxml')
                    torrent_href = torrentsoup.find_all('a',{'class':'uk-button'})
                    if len(torrent_href)>0:
                        torrent=torrent_href[0].get('href')
                        data['Index'].append(i)
                        data['Name'].append(title)
                        data['Link'].append(suburl)
                        data['Torrent'].append(torrent)
                        print('Page= ', str(page), ' index =', i, (' ').ljust(2, ' '), title.ljust(110, ' '),suburl.ljust(70, ' '), torrent)
                        i = i + 1
    return
# with open('XP1024.txt', 'w') as outfile:
#     json.dump(data, outfile)

# DistributedJobs=[pool.apply_async(Download,args=(i,)) for i in range(StartPage,EndPage)]

if __name__ == '__main__':
    jobs=[]
    for i in range(StartPage,EndPage+1):
        p=mp.Process(target=Download,args=(i,))
        jobs.append(p)
        p.start()

    df=pd.DataFrame.from_dict(data).set_index('Index')
    print('df shape: ',df.shape)
    df.to_csv(ID[id]+' XP1024-Page'+str(StartPage)+'-to-Page'+str(EndPage)+'.csv', encoding='utf_8_sig')

