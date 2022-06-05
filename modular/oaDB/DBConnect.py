from modular import mapper


class OAMessage(object):

    def __init__(self):
        self.cursor = mapper.connect_sqlserve()