class ErrorHandler(Exception):
    def __init__(self , scanner):
        self.scanner = scanner

    def error(self, msg, place):
        line_number, char_number = self.scanner.get_place(place)
        print("Error at line %d character %d: %s"
              % (line_number, char_number, msg))

    def report_error(self, error_string, ignored_string, place):
        self.error("Unexpected %s was found. Ignoring %s." % (error_string, ignored_string), place)

    def simple_error(self, msg):
        print(msg)

    def scanner_error(self , error_string , place):
        self.error("Scanner error: %s." %error_string , place)

    def semantic_error(self , error_string , place = None):
        if place is None:
            place = self.scanner.currentIndex
        self.error("Semantic error: %s." %error_string , place)


class Scanner_error(ErrorHandler):
    """ to raise scanner errors """

class Semantic_error(ErrorHandler):
    """ to raise semnatic errors """