class ErrorHandler(Exception):
    def __init__(self , scanner):
        self.scanner = scanner

    def error(self, msg, place):
        line_number, char_number = self.scanner.get_place(place)
        print("Error at line %d character %d: %s"
              % (line_number, char_number, msg))

    def report_error(self, error_string, ignored_string, place):
        self.error("Unexpected %s was found. Ignoring %s." % (error_string, ignored_string), place)
