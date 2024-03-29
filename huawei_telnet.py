import telnetlib
import time
from pprint import pprint
import re


def to_bytes(line):
    return f"{line}\n".encode("utf-8")


def send_show_command(ip, username, password,  command):
    with telnetlib.Telnet(ip) as telnet:
        telnet.read_until(b"Username:")
        telnet.write(to_bytes(username))
        telnet.read_until(b"Password:")
        telnet.write(to_bytes(password))
        '''
        index, m, output = telnet.expect([b">", b"#"])
        if index == 0:
            telnet.write(b"enable\n")
            telnet.read_until(b"Password")
            telnet.write(to_bytes(enable))
        '''          
        telnet.read_until(b">", timeout=5)
        time.sleep(3)
        telnet.read_very_eager()

        telnet.write(to_bytes(command))
        result = ""

        while True:
            index, match, output = \
                telnet.expect([b"--More--", b"#"], timeout=5)
            output = output.decode("utf-8")
            output = re.sub(" +--More--| +\x08+ +\x08+", "\n", output)
            result += output
            if index in (1, -1):
                break
            telnet.write(b" ")
            time.sleep(1)
            result.replace("\r\n", "\n")

        return result


if __name__ == "__main__":
    devices = ["10.1.0.1", "10.1.0.2", "10.1.0.3"]
    for ipv4 in devices:
        answer = \
            send_show_command(ipv4, "root", "huawei", "disp mac-ad")
        pprint(answer, width=120)
