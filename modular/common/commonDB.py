from modular import mapper


class wmsCommonDB(object):
    def __init__(self):
        self.cursor = mapper.connect_DB('wms_mysql')


class WspCommonDB(object):
    def __init__(self):
        self.cursor = mapper.ConnectWSPdb('wsp_mysql')