from modular import mapper


class WspPsr(object):
    def __init__(self):
        self.cursor = mapper.connect_DB()