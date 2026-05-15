import os

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CONFIG_DIR)

DIR_FINDINGS = os.path.join(BASE_DIR, "data", "findings")
DIR_SAVED_FINDINGS = os.path.join(BASE_DIR, "data", "findings_saved")
DIR_LOGS = os.path.join(BASE_DIR, "minescript", "find", "data", "findings")

SETTING_PATH = os.path.join("minescript", "find", "config", "setting.json")