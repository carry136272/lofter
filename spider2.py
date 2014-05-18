import urllib,urllib2,re
import os,MySQLdb,string

def getHtml(url):
    headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
            'Connection':'keep-alive',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'en-US,en;q=0.5'}
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

def getDate(html):
    imageDate=re.findall('<a href=".*?">(.*?)</a>.*?<span class="hotcount">.*?',html)
    return imageDate[0]

if __name__=='__main__':
    author=()
    conn=MySQLdb.connect(host='localhost',user='jiraiya',passwd='jiraiya',db='lofter',port=3306)
    cur=conn.cursor()
    cur.execute('select link from image')
    links=cur.fetchall()
    list_links=[]
    for index in xrange(cur.rowcount):
        list_links.append(links[index][0])
    cur.execute('select * from author')
    author=cur.fetchall()
    for i in xrange(cur.rowcount):
        authorId=author[i][0]
        authorName=author[i][1]
        authorHost=author[i][2]
        indexPage=1
        while 1:
            if getTopic(getHtml(authorHost+'/?page='+str(indexPage))):
                html=getHtml(authorHost+'/?page='+str(indexPage))
                list_topic=getTopic(html)
                for topic in list_topic:
                    list_src=getSrc(getHtml(topic))
                    imageDate=getDate(getHtml(topic))
                    for src in list_src:
                        if src not in list_links:
                            cur.execute('insert into image(authorid,link,imageDate) values(%d,"%s","%s")'%(int(authorId),src,imageDate))
                            print authorId,src
                indexPage+=1
            else:
                break
    cur.close()
    conn.close()
