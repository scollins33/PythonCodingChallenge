import json
import re
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, global_list):
        self.g_list = global_list  # G_NUMBERS list from main app

    def get(self):
        valid_modes = {
            "country": 2,
            "area": 3,
            "prefix": 3,
            "line": 4,
            "extended": 0,
            "full": 0,
        }

        try:
            mode = self.get_argument("mode")
            value = self.get_argument("value")

            if mode not in valid_modes:
                raise Exception("Mode is not valid")
            if re.fullmatch("[^0-9]", value) is not None:
                raise Exception("Value is not valid")
            if len(value) > valid_modes[mode]:
                raise Exception("Value length ({}) too large for Mode length ({})".format(len(value), valid_modes[mode]))

            query_list = []

            for phoneObj in self.g_list:
                if mode == "full":
                    query_list.append(phoneObj.get_formatted_string())

                if mode == "country" and phoneObj.country_code is not None and value == phoneObj.country_code:
                    query_list.append(phoneObj.get_formatted_string())

                if mode == "area" and value in phoneObj.area_code:
                    query_list.append(phoneObj.get_formatted_string())

                if mode == "prefix" and value in phoneObj.prefix:
                    query_list.append(phoneObj.get_formatted_string())

                if mode == "line" and value in phoneObj.line_number:
                    query_list.append(phoneObj.get_formatted_string())

                if mode == "extended" and phoneObj.extension is not None:
                    query_list.append(phoneObj.get_formatted_string())

            self.set_status(200)
            self.write({
                "status": True,
                "payload": json.dumps(query_list)
            })

        except tornado.web.MissingArgumentError:
            self.set_status(400)
            self.write({
                "status": False,
                "payload": "Missing argument, must include 'mode' and 'value'"
            })

        except Exception as err:
            self.set_status(405)
            self.write({
                "status": False,
                "payload": str(err)
            })

        finally:
            self.finish()

    def post(self):
        self.set_status(501)
        self.write({
            "status": False,
            "payload": "POST not implemented, please use GET only"
        })
