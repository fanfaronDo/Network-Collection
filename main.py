from pprint import pprint
from pythonping import ping
from file_handler import FileHandler
from switch import Switch


def check_connect(ip):
    return ping(ip, timeout=1, count=4).stats_packets_returned > 0


def main():
    while True:
        ip_address = input("input ip address switch: ")
        if check_connect(ip_address):
            print("ip is alive")
            break
        else:
            print("ip is not alive")
            print("input other ip address")

    username = input("Username: ")
    print("Password:", end=" ")
    password = input()
    print("password enable: ", end=" ")
    password_enable = input()
    commands = FileHandler("commands").read_from_file()
    try:
        with Switch(ip_address, username, password, password_enable) as sw:
            sw.login()
            sw.send_command(commands=commands)
            result = sw.commands_result()
    except:
        print("not connect")
        return

    file_name = "result.txt"
    FileHandler(file_name).write_in_file(result)
    print("Done...")


if __name__ == '__main__':
    main()



