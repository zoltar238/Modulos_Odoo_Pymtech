import configparser

# Read the configuration file
config = configparser.ConfigParser()
config.read("./res/watchdog.conf")
email = config['email']['sender']
key = config['email']['key']
