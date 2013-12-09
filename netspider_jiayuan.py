#version 0.1
#get code on https://github.com/bluedazzle/python_network

import urllib.request
import optparse
import http.cookiejar
import urllib.parse
import time
import re
import os

isLogin = False
isNetCon = True
isPhotoExist = False
userurl = 100000000
gettimes = 0
failtimes = 0
photo_url = ''
photooutpath = ''
failArr = ['失败列表：']
loglists = ['']

def createLog(loglist):
    global failArr
    try:
        with open('jiayuan_spider.log','a+') as file1:
            file1.write(str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
            for it in loglist:
                file1.write(it)
                file1.write('\n')
            for it in failArr:
                file1.write(it)
                file1.write('\n')
            file1.write('\n\n\n')
            file1.close()
            print('日志保存成功...')
    except:
        print('日志保存失败')
    
def loginJiaYuan():
    global isLogin
    global loglists
    post_headers = {'Referer' : 'http://login.jiayuan.com/err.php?err_type=2&pre_url=http://www.jiayuan.com/usercp',
                          'Host': 'login.jiayuan.com',
                          'Accept' : 'text/html, application/xhtml+xml, */*',
                          'Content-Type' : 'application/x-www-form-urlencoded',
                          'Cookie' : 'registeruid=104463413; main_search:104463413=%7C%7C%7C00; REG_REF_URL=; poplogincount=1',
                          'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}
    print('登陆世纪佳缘中...')
    try :
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(opener)
        #"[step1] to get cookie "
        MainUrl = "http://login.jiayuan.com/dologin.php?pre_url=http://www.jiayuan.com/usercp"
        resp = urllib.request.urlopen(MainUrl)

        #emulate login jiayuan
        MainLoginUrl = "http://login.jiayuan.com/dologin.php?pre_url=http://www.jiayuan.com/usercp"
        postDict = {
                'channel'          : '0',
                'name'             : 'p2p_test@yeah.net',
                'password'       : '123456qq',
                'ijg_login'         : '1',
                'position'          :'0'}
        postData = urllib.parse.urlencode(postDict).encode()
        #print ("postData=",postData)
        req = urllib.request.Request(MainLoginUrl, postData)
        for key,itm in post_headers.items():
            req.add_header(key,itm)
        #print('headers has already added.')
        html = urllib.request.urlopen(req)
        #print('html has getted')
        #print(type(cj))
        #for index, cookie in enumerate(cj):
           # print( '[',index, ']',cookie)
        for cookie in cj:
            if(cookie.name == 'RAW_HASH'):
                isLogin = True
                
        time.sleep(0.2)
    except:
        print('连接失败，请检查网络连接')
        
       
def requestData(url):
    '''请求数据模块'''
    global isNetCon
    global loglists
    try:
        data = ''
        req = urllib.request.Request(url)
        req.add_header('Content-Type' ,'application/x-www-form-urlencoded')
        #html = urllib.request.urlretrieve(url,'jiayuantest.txt')
        reqs = urllib.request.urlopen(req)
        data = reqs.read().decode('utf-8')
    except urllib.error.URLError as err:
        print('网络未连接！')
        loglists.append('网络未连接！')
        isNetCon = False
        return data
    print('得到服务器数据')
    return data

def formatUserData(data):
    '''用户数据提取模块'''
    global userurl
    global failtimes
    global gettimes
    global failtimes
    global failArr
    global photo_url
    global photooutpath
    global isPhotoExist
    try:
    #user_photo
        photo_urlarr = re.findall('''<img\s*?src=["](\S*?)["]/></a>''',data)
        if(photo_urlarr):
            print('获取到照片！')
            isPhotoExist = True
            try:
                os.mkdir('userphoto')
            except FileExistsError as err:
                print(end = '')
            finally:
                photooutpath = 'userphoto' +'\\'+ str(userurl) + '.jpg'
                photo_url = photo_urlarr[0]
                urllib.request.urlretrieve(photo_url,photooutpath)
        else:
            print('此用户无照片')
    #user_name user_ID
        res = re.findall('''<title>[\u4e00-\u9fa5]+[_]{1}([\u4e00-\u9fa5]+)''',data)
        res.append(re.findall('''<title>[\u4e00-\u9fa5]+[_]{1}[\u4e00-\u9fa5]+\S*?(\d{9})''',data)[0])
    #sex
        res.append(re.findall('''查看详细信息&gt\S*?</a>([\u4e00-\u9fa5]+)''',data)[0])
    #age
        res.append(re.findall('''查看详细信息&gt\S*?</a>[\u4e00-\u9fa5]+\S*?(\d{1,3}[\u4e00-\u9fa5]+)''',data)[0])
    #constellation
        res.append(re.findall('''查看详细信息&gt\S*?</a>[\u4e00-\u9fa5]+\S*?\d{1,3}[\u4e00-\u9fa5]+\S*?([\u4e00-\u9fa5]+)''',data)[0])
    #from
        res.append(re.findall('''查看详细信息&gt\S*?</a>\S*?([\u4e00-\u9fa5]+)</h2>''',data)[0])
    #height
        res.append(re.findall('''<span class *= *['"]*\S+["']><b>([\u4e00-\u9fa5]+)[：]{1}</b>(\d{1,3}[\u4e00-\u9fa5]+)''',data)[0])
    #education back&job
        res.append(re.findall('''<span class *= *['"]*\S+160["']><b>([\u4e00-\u9fa5]+)[：]{1}</b>(\S*?)</span>''',data)[0])
        res.append(re.findall('''<span class *= *['"]*\S+160["']><b>([\u4e00-\u9fa5]+)[：]{1}</b>(\S*?)</span>''',data)[1])     
    #marriage nation
        res.append(re.findall('''<span class *= *['"]*\S+100["']><b>([\u4e00-\u9fa5]+)[：]{1}</b>([\u4e00-\u9fa5]+)''',data)[0])
        res.append(re.findall('''<span class *= *['"]*\S+100["']><b>([\u4e00-\u9fa5]+)[：]{1}</b>([\u4e00-\u9fa5]+)''',data)[1])
        res.append(re.findall('''<span class *= *['"]*\S+100["']><b>([\u4e00-\u9fa5]+)[：]{1}</b>([\u4e00-\u9fa5]+)''',data)[2])
        #res.append(re.findall('''<span class *= *['"]*\S+100["']><b>([\u4e00-\u9fa5]+)[：]{1}</b>([\u4e00-\u9fa5]+)''',data)[3])
        #salary
        res.append(re.findall('''<span class *= *['"]*\S+140["']><b>([\u4e00-\u9fa5]+)[：]{1}</b>(\S*?)</span>''',data)[0])
        res.append(re.findall('''<span class *= *['"]*\S+140["']><b>([\u4e00-\u9fa5]+)[：]{1}</b>(\S*?)</span>''',data)[1])
        #class=["]\S*?["]>\s*?<p>(.*?)</p> xuanyan
        res.append(re.findall('''class=["]internal_monolog_content["]>\s*?<p>(.*?)</p>''',data)[0])
    except:
        print('数据查询失败！')
        print('============================================')
        failArr.append(url)
        failtimes = failtimes +1
        res.clear()
    finally:
        userurl = userurl + 1
        gettimes = gettimes +1
        return res

def outputData(url,result,outfilename = 'userdata'):
    '''数据输出模块'''
    outfile = outfilename + '.csv'
    try:
        with open(outfile,'a+') as file0:
            file0.write(str(gettimes))
            file0.write(',')
            file0.write(url)
            file0.write(',')
            if(isPhotoExist):
                file0.write(photooutpath)
            else:
                file0.write('用户无照片')
            file0.write(',')
            for itm in result:
                if(str(type(itm))=='''<class 'tuple'>'''):
                    for item in itm:
                        file0.write(item)
                else:
                    file0.write(itm)
                file0.write(',')
            file0.write('\n')
            print('数据写入成功！')
            print('============================================')
            file0.close()
    except UnicodeEncodeError as err:
        print('网页编码变化，数据写入失败')
        file0.close()

dataNum = int(input('请输入抓取数据量:'))
outputFileName = input('请输入输出文件名（默认为userData）')
loginJiaYuan()
if(isLogin):
    print('登陆成功！')
    loglists.append('登陆成功！')
    if(not(outputFileName)):
        outputFileName = 'userData'
    outtmp = '数据输出文件：' + str(outputFileName) + '.csv'
    loglists.append(outtmp)
    while(gettimes<(dataNum)):
        url = 'http://www.jiayuan.com/' + str(userurl)
        print('第',(gettimes+1),'次查询：')
        #print('查询网址：',url)
        htmdata = requestData(url)
        restmp = formatUserData(htmdata)
        if(restmp):
            outputData(url,restmp,outputFileName)
        if(not(isNetCon)):
            break
        isPhotoExist = False
        time.sleep(0.2)
else:
    print('登陆失败！')
    loglists.append('登陆失败！')
print('===========================================')
print('===========================================')
if(isNetCon):
    tmp = '数据抓取完成，共进行:'+ str(gettimes) + '次数据抓取，失败:' + str(failtimes) + '次'
    print(tmp)
    loglists.append(tmp)
else:
    print('数据抓取失败，请检查网络连接。')
    loglists.append('数据抓取失败，请检查网络连接。')
for item in failArr:
        print(item)
createLog(loglists)
tm = input('按任意键退出')
