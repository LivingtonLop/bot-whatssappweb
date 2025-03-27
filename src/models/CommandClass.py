from selenium import webdriver
from src.models.ActionClass import ActionClass
from src.models.WhatsappWebClass import WhatsAppWebClass

class CommandClass:

    def __init__(self, driver:webdriver.Chrome,actions:ActionClass,entity:WhatsAppWebClass,config):
        self.driver = driver
        self.actions = actions
        self.entity = entity
        self.config = config
        self.wait_times = config["wait_times"]

    def close_session(self):
        selector_open = self.entity.get_xpath(category="buttons",key="settings")
        selector_close_session = self.entity.get_xpath(category="buttons",key="close_session")
        selector_confirm = self.entity.get_xpath(category="buttons",key="confirm_close_session")
        
        self.actions.open_settings(selector= selector_open,timeout=self.wait_times["load_labels"])
        self.actions.close_session(selector= selector_close_session,timeout=self.wait_times["load_labels"])
        self.actions.confirm_close_session(selector= selector_confirm,timeout=self.wait_times["load_labels"])

    