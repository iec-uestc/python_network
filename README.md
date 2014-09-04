python_network
==============
version：1.0

python 3.3 环境下写的一个简单爬虫类，实现了模拟GET POST 请求，以及简单的cookie管理（搜索，显示）

类名：NetSpider
引用：import NetSpider
初始化：a = NetSpider()

属性：
  MainUrl:
  Host: postheaders字段，主机地址
  Refer: postheaders字段，前连接地址
  Accept: postheaders字段，“text/html, application/xhtml+xml, */*”等
  ContentType: postheaders字段，请求内容类型，“application/json”等
  UserAgent: postheaders字段，浏览器相关，“Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64;”等
  CookieList: Cookie列表
  PostHeaders: postheaders，可统一更新此字典，也可单独更新某一值，见上
  
方法：
  GetResFromRequest(self,method,requrl,encodemethod = 'gbk',postdict = {''},reqdata = '')
  param：
    method：“GET”或“POST”
    requrl：需要请求的网址
    encodemethod：编码方式
    postdict：post内容（表单）
    reqdata：post数据（非application/x-www-form-urlencoded等表单数据，例如json等）
  return：
    成功：返回得到的网页（html）
    失败：返回错误
    
  SearchCookie(self,searchkey)
  param：
    searchkey：需要搜索的cookie.name
  return:
    成功：返回搜索的cookie.value
    失败：返回“nothing find”
  
  ShowCurrentCookie(self)
  return：
    返回当前cookie列表中的所有cookie
