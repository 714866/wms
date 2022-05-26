from modular import mapper


class WspCommonDB(object):
    def __init__(self):
        self.cursor = mapper.connect_DB('wsp_mysql')