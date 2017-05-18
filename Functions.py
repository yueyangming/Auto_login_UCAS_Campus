import requests
from urllib.parse import quote
URL = 'http://210.77.16.21'

def Make_Cookies(jid):
    # Make Cookies with given Jid
    Cookies = {
        'EPORTAL_AUTO_LAND': '',
        'EPORTAL_COOKIE_USERNAME': '',
        'EPORTAL_COOKIE_PASSWORD': '',
        'EPORTAL_COOKIE_SERVER': '',
        'EPORTAL_COOKIE_SERVER_NAME': '',
        'EPORTAL_COOKIE_DOMAIN': '',
        'EPORTAL_COOKIE_SAVEPASSWORD': 'false',
        'EPORTAL_COOKIE_OPERATORPWD': '',
        # 'JSESSIONID': jid
    }
    return Cookies

def Init():
    # Make fake headers, set sessions, and make Cookies.
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    session = requests.session()
    session.headers.update(headers)
    response = session.get(URL)
    r_url = response.url
    jid = session.cookies['JSESSIONID']
    querystring = r_url[38:]
    querystring = quote(quote((querystring)))
    Cookies = Make_Cookies(jid)

    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Referer': URL + '/eportal/index.jsp?' + r_url[38:],
               'DNT': '1',
               'Origin': URL,
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    session.headers.update(headers)
    Cookie_object = requests.cookies.cookiejar_from_dict(Cookies, cookiejar=None, overwrite=True)

    return session, querystring, Cookie_object

def login(userid,password, session,Cookie_object):
    # Login in with given userid and password
    data_string = 'userId=' + userid + '&password=' + password + '&service=&queryString=' + querystring + '&operatorPwd=&validcode='

    login_url = URL + '/eportal/InterFace.do?method=login'
    login_response = session.post(login_url, data=data_string, cookies=Cookie_object)

    null = ''  # for some condition there will be a null here.
    result_dict = eval(login_response.text)
    result = 'success' == result_dict['result']

    return result, result_dict