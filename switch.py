from telnetlib import Telnet
from excepton import ConnectException


class Switch(Telnet):
    cr = b"\n"

    def __init__(self, ip_address, login, password, password_enable):
        super().__init__(host=ip_address, port=23, timeout=10)
        self.__ip_address = ip_address
        self.__login = Switch.encode_string_to_binary(login)
        self.__password = Switch.encode_string_to_binary(password)
        self.__password_enable = Switch.encode_string_to_binary(password_enable)
        self.__result_cash_command = []

    def login(self):
        if self.expect([b"[Uu]sername:"], timeout=2)[0] < 0:
            self.write(self.__login + self.cr)

        self.read_until(b"assword:", timeout=5)
        self.write(self.__password + self.cr)

        if self.expect([b"#"], timeout=2)[0] < 0:
            self.write(b"enable" + self.cr)
            if self.expect([b"[Pp]assword:"], timeout=2)[0] >= 0:
                self.write(self.__password_enable + self.cr)

        if self.expect([b"[>#]"], timeout=2)[0] < 0:
            raise ConnectException("username or password not correct")

    def send_command(self, commands: list):
        self.write(b"terminal length 0" + self.cr)
        self.read_until(b"#", timeout=5)

        for command in commands:
            self.write(Switch.encode_string_to_binary(command) + self.cr)
            self.__result_cash_command.append(
                Switch.decode_bytes_to_string(self.read_until(b"#", timeout=5)))

    def commands_result(self):
        return self.__result_cash_command

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @staticmethod
    def encode_string_to_binary(data: str):
        return data.encode('ascii')

    @staticmethod
    def decode_bytes_to_string(data: bytes):
        return data.decode('utf-8')