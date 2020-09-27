import os
from configparser import ConfigParser

# set path
basedir = os.path.abspath('.') + '/'
config = ConfigParser()
config.read(basedir + 'config.ini')


class Config():
    # auth info
    login_type = config.get('AUTH', 'TYPE')
    accountid = config.get('AUTH', 'IAM-ID')
    account = config.get('AUTH', 'ACCOUNT')
    password = config.get('AUTH', 'PASSWORD')
    # driver prefix
    #binary_prefix = config.get('PREFIX', 'BINARY')
    cd_prefix = config.get('PREFIX', 'CHROMEDRIVER')
    # deepracer model
    md_name = config.get('MODEL', 'MODEL')
