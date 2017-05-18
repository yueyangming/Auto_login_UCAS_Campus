### Auto_login_UCAS_Campus

这是业余时间写的一个小脚本，主要实现的功能是 在给定 用户名和密码的时候，可以自动登录到UCAS 校园网账户。主程序删掉了，留下了三个函数，希望对你们有用。

# Requirments：

Python 3.*

Package：

Requests 

## 如何使用?

session, querystring, Cookie_object = Init()
这个Init 函数主要是初始化程序，为后续的函数和主程序提供一些东西，session 是一个连到 登录服务器的会话（不太会翻译)
querystring 是在登陆时候需要的一个字符串，Cookie_object 是 一个 Cookie object。

result, result_dict = login(userid,password, session,Cookie_object)
这个函数就是主函数了，尝试登陆，并返回登陆结果（result， boolean 型， True 或者 False）， result_dict 是response 里面包含信息的一个字典。个人觉得 里面 message 这个信息很有用，有一点问题是在我这显示的是乱码，导致我在判断不同返回情况的时候是使用 message 的长度来做的。。。

至于 MakeCookie， 不用管它，是 Init 里面需要调用的一部分。

## 能用它来做什么？

# 请勿用它来做任何非法用途！

最简单的来说，就是做一个开机启动脚本，放上自己的用户名密码，做到自动开机登陆。
一个类似的用途是用在一些嵌入式设备上，比如说树莓派，让他在连上Wifi 之后自动连网。





## As a programmer, just use programming to change this world. 
