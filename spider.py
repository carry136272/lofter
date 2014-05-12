import urllib,urllib2,re
import os

def getHtml(url):
    headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
            'Connection':'keep-alive',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'en-US,en;q=0.5',
            'Host':'***.lofter.com',
            'Referer':url+'/'}
    request=urllib2.Request(url,headers=headers)
    fsock=urllib2.urlopen(request)
    html=fsock.read()
    fsock.close()
    return html

def getNextPage(html):
    nextPage=re.search('<a href="\?page=(.*?)" class="nxt">.*?</a>',html)
    return nextPage.group(1)

def getTopic(html):
    list_topic=re.findall('<div class="imgwrapper"><a href="(.*?)">.*?</a></div>',html)
    return list_topic

def getSrc(html):
    list_src=re.findall('<img src="(.*?)" alt="" style=""/>',html)
    return list_src

if __name__=='__main__':
    indexPage=1
    dir='./***/'
    list_saved=[]
    for root,subdirs,files in os.walk(dir):
        for file in files:
            list_saved.append(file)
    while 1:
        url='http://***.lofter.com'+'/?page='+str(indexPage)
        html=getHtml(url)
        if getNextPage(html):
            listTopic=getTopic(html)
            for i in range(0,len(listTopic)):
                print listTopic[i]
                listSrc=getSrc(getHtml(listTopic[i]))
                if listSrc:
                    for x in range(0,len(listSrc)):
                        imgName=listSrc[x].split('/')[-1]
                        if imgName not in list_saved:
                            urllib.urlretrieve(listSrc[x],dir+imgName)
            indexPage+=1
        else:
            break
