# pip modules
import tornado.ioloop
import tornado.web

# local modules
from models.PhoneNumber import PhoneNumber
from handlers.Main import MainHandler

"""
GLOBALS
"""
G_NUMBERS = []
G_PORT = 8080


def parse_data_file():
    with open("./data/code_challenge_data_1.txt") as number_list:
        for line in number_list:
            G_NUMBERS.append(PhoneNumber(line.strip()))

    print("Total Numbers Parsed: {}".format(len(G_NUMBERS)))


def start_web_server():
    web_server = tornado.web.Application([
        (r"/api", MainHandler, dict(global_list=G_NUMBERS))
    ])
    web_server.listen(G_PORT)
    print("Web Server listening on Port {}".format(G_PORT))
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    parse_data_file()
    start_web_server()
