
class BadKeyException(Exception):

    def __init__(self, message: str, errors: list):
        super(BadKeyException, self).__init__(message)
        self.errors = errors
    
    def __str__(self):
        for error in self.errors:
            print ("Key error {0} encountered" %s (error))
