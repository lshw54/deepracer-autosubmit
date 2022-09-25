import os
from configparser import ConfigParser

# set path
basedir = os.path.abspath('.') + '/'
config = ConfigParser(interpolation=None)
config.read(basedir + 'config.ini')


class Config():
    # auth info
    accountid = config.get('AUTH', 'IAM-ID')
    account = config.get('AUTH', 'ACCOUNT')
    password = config.get('AUTH', 'PASSWORD')
    # deepracer model
    league_url = config.get('LEAGUE', 'URL')
    md_name = config.get('LEAGUE', 'MODEL')
    # driver prefix
    arn = config.get('PREFIX', 'ARN')
    league_name = config.get('PREFIX', 'LEAGUENAME')
    #binary_prefix = config.get('PREFIX', 'BINARY')
    #cd_prefix = config.get('PREFIX', 'CHROMEDRIVER')
