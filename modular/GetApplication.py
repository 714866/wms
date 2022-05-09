# from modular.glo import set_value
# from modular.wspxxlJob.xxlJob import SourceXXlJob
from configparser import ConfigParser
import os


print(os.path.abspath(os.path.dirname(__file__)))
cp = ConfigParser()
cp.read(os.path.abspath(os.path.dirname(__file__))+'/config/application.conf')

def get_value(key):
    return cp.get('wsp_url','url')