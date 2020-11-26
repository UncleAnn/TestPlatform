from time import sleep
from selenium.common.exceptions import NoSuchElementException
from automation.get_driver import GetDriver
from tool.logger import GetLogger
logger = GetLogger().logger


class Keyword:
    def __init__(self):
        self.driver = GetDriver.driver()

    def __del__(self):
        self.quit_driver()

    def switch_window(self, loc, data):
        """element是为调用反射加入的，不要删"""
        window_handles = self.driver.window_handles
        for h in window_handles:
            self.driver.switch_to.window(h)
            if self.driver.title == data:
                break

    def switch_iframe(self, loc, data):
        """data是为调用反射加入的，不要删"""
        iframe = self.get_element(loc)
        self.driver.switch_to.frame(iframe)

    def page_should_contain(self, element, data):
        """element是为调用反射加入的，不要删"""
        try:
            self.driver.find_element_by_xpath(f'//*[contains(., "{data}")]')
            result = True
        except NoSuchElementException:
            result = False
        assert result is True

    @staticmethod
    def wait(loc, data):
        """强制延时，element是为调用反射加入的，不要删"""
        sleep(int(data))

    def get_url(self, loc, url):
        """element是为调用反射加入的，不要删"""
        self.driver.get(url)

    # def get_element(self, element, timeout=15, poll_frequency=0.1):
    def get_element(self, loc):
        return self.driver.find_element(*loc)
        # return WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency).until(
        #     lambda x: x.find_element(*loc))

    def click_element(self, loc, data):
        """data是为调用反射加入的，不要删"""
        self.get_element(loc).click()

    def input_content(self, loc, content):
        el = self.driver.find_element(*loc)
        el.clear()
        el.send_keys(content)

    def quit_driver(self):
        self.driver.quit()