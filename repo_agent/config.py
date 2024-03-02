import yaml
import sys

try:
    CONFIG = yaml.load(open("config.yml", "r"), Loader=yaml.FullLoader)
except FileNotFoundError:
    print(
        "The file does not exist! Maybe you forgot to rename config.yml.template to config.yml and update the essential content"
    )
    sys.exit(1)  # Exits the program

