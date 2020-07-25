
class Returns():
    def __init__(self, result, message):
        self.__result = result
        self.__message = message

    def response(self):
        return {"success":self.__result, "message": self.__message }