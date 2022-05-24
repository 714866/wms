from modular import mapper
from modular.common.SqlChangeFormat import SqlChangeFormat


class OAMessage(object):

    def __init__(self):
        self.cursor = mapper.connect_sqlserve()