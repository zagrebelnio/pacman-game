class Error(Exception):
    def __init__(self, error_message):
        self.__message = error_message
    def getMessage(self):
        return self.__message