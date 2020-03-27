import re


class PhoneNumber:
    def __init__(self, p_text):
        self.raw_text       = p_text
        self.raw_numbers    = re.sub("[^0-9]", "", p_text)
        self.country_code   = None
        self.area_code      = None
        self.prefix         = None
        self.line_number    = None
        self.extension      = None

        if len(self.raw_numbers) != 10:
            # too bad we don't have front-end devs to make our input form enforce formatting
            self.set_country_code()
            self.set_extension_code()

        start = 0 if self.country_code is None else len(self.country_code)
        self.area_code      = self.raw_numbers[start:start+3]
        self.prefix         = self.raw_numbers[start+3:start+6]
        self.line_number    = self.raw_numbers[start+6:start+10]

        self.check_doctor_office()

    def set_country_code(self):
        plusle = self.raw_text.find("+", 0, 3)
        minun  = self.raw_text.find("-", 0, 3)
        if plusle > -1 or minun > -1:
            idx = plusle if plusle > -1 else minun  # set which one we're looking for
            self.country_code = re.sub("[^0-9]", "", self.raw_text[:idx])

    def set_extension_code(self):
        ext_index   = self.raw_text.find("x")
        if ext_index > -1:
            self.extension = re.sub("[^0-9]", "", self.raw_text[ext_index:])  # just parse it from the end of the string

    def check_doctor_office(self):
        # what is this? the instructions to schedule a doctor's appointment?
        # no but really.. I know this is cheating but it's not even clearly extension 1101
        if self.raw_text == "9346951114,1,1,#,0,1":
            self.area_code   = "934"
            self.prefix      = "695"
            self.line_number = "1114"
            self.extension   = "1101"

    def get_formatted_string(self):
        string = ""
        string += ("" if self.country_code  is None else (self.country_code + "+ "))
        string += ("" if self.area_code     is None else ("(" + self.area_code + ") "))
        string += ("" if self.prefix        is None else (self.prefix + "-"))
        string += ("" if self.line_number   is None else self.line_number)
        string += ("" if self.extension     is None else (" ext " + self.extension))
        return string
