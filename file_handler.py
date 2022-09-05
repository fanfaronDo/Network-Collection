from excepton import ListIsEmptyException


class FileHandler:

    """ Work with file """

    def __init__(self, file_name):
        self.__file_name = file_name

    def read_from_file(self) -> list:
        with open(self.__file_name, "r", encoding="utf-8") as file:
            return [str(f).strip() for f in file.readlines()]

    def write_in_file(self, text: list):
        self.__validations(text)

        with open(self.__file_name, "w", encoding="utf-8") as file:
            for command in text:
                file.write(command)
                file.write("\n\n")

    @staticmethod
    def __validations(text: list):
        if not text:
            raise ListIsEmptyException("response is empty")
