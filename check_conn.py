# encoding=utf-8
import os
import socket
import threading
import sys

reload(sys)
sys.setdefaultencoding('utf8')
socket.setdefaulttimeout(40)


class BaseCheck:
    # 云图/所有设备需要的域名/ip
    list_all = ('x.sangfor.com.cn:443', 'device.sangfor.com.cn:443', 'device.scloud.sangfor.com.cn:443',
                'remote0.sangfor.com.cn:443', 'remote1.sangfor.com.cn:443', '219.135.99.249:5000')
    # 不同设备需要的域名
    list_sip = list_all + (
        'auth.sangfor.com.cn:443', 'clt.sangfor.com.cn:443', 'clt1.sangfor.com.cn:443', 'notify.sangfor.com.cn:443',
        'upd.sangfor.com.cn:443', 'intelligence.sangfor.com.cn:443', 'tamper.sangfor.com.cn:443',
        'analysis.sangfor.com.cn:443')
    list_edr = list_all + (
        'u.soc.sangfor.com.cn:7443', 'auth.sangfor.com.cn:443', 'clt.sangfor.com.cn:443', 'clt1.sangfor.com.cn:443',
        'notify.sangfor.com.cn:443', 'upd.sangfor.com.cn:443', 'intelligence.sangfor.com.cn:443',
        'tamper.sangfor.com.cn:443', 'analysis.sangfor.com.cn:443')
    list_af = list_all + (
        'auth.sangfor.com.cn:443', 'clt.sangfor.com.cn:443', 'clt1.sangfor.com.cn:443', 'notify.sangfor.com.cn:443',
        'upd.sangfor.com.cn:443', 'intelligence.sangfor.com.cn:443', 'tamper.sangfor.com.cn:443',
        'analysis.sangfor.com.cn:443', 'saas1.sangfor.com.cn:443', 'cloud.sangfor.com:443')

    def run(self, list_x):
        pass

    def check_yuntu(self):
        self.run(BaseCheck.list_all)

    def check_af(self):
        self.run(BaseCheck.list_af)

    def check_sip(self):
        self.run(BaseCheck.list_sip)

    def check_edr(self):
        self.run(BaseCheck.list_edr)


class PingCheck(BaseCheck):

    def run(self, list_x):
        list_cmd = []
        for x in list_x:
            ip, port = x.split(':')
            list_cmd.append("echo -e ping {}".format(ip))
            list_cmd.append(
                'ping -c4 {0} | grep -q "ttl" && echo -e "\033[32m {0} passed\033[0m" || echo -e "\033[31m {0} failded\033[0m" &'.format(
                    ip))
        list_cmd.append('wait && echo -e "***all check finished***\n"')
        os.system("\n".join(list_cmd))


class SocketCheck(BaseCheck):

    def check_port(self, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            ret = s.connect_ex((ip, port))
            return ret == 0
        except:
            return False
        finally:
            s.close()

    def do(self, list_x):
        for x in list_x:
            ip, port = x.split(':')
            ret = self.check_port(ip, int(port))
            cmd = 'echo -e "\033[32m {0} passed\033[0m"' if ret else 'echo -e "\033[31m {0} failded\033[0m"'
            cmd = cmd.format(x)
            os.system(cmd)

    def run(self, list_x):
        num_thread = 4
        for num in range(num_thread):
            item = [x for i, x in enumerate(list_x) if i % num_thread == num]
            threading.Thread(target=self.do, args=(item,)).start()
        os.system('echo -e "***all check finished***\n"')


def main():
    num1 = str(input(u"1.端口测试\n2.Ping测试\n:"))
    bean_ckeck = None
    if num1 == '1':
        bean_ckeck = SocketCheck()
    elif num1 == '2':
        bean_ckeck = PingCheck()
    if bean_ckeck:
        num2 = str(input(u"1.SIP设备\n2.EDR设备\n3.AF设备\n4.云图(设备跳转/接入)\n:"))
        if num2 == '1':
            bean_ckeck.check_sip()
        elif num2 == '2':
            bean_ckeck.check_edr()
        elif num2 == '3':
            bean_ckeck.check_af()
        elif num2 == '4':
            bean_ckeck.check_yuntu()


if __name__ == '__main__':
    main()
