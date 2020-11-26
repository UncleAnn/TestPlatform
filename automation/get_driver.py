from selenium import webdriver


class GetDriver:
    instance = None

    @classmethod
    def driver(cls, browser='Chrome'):
        if not cls.instance:
            if browser.lower() == 'chrome':
                cls.instance = webdriver.Chrome()
            elif browser.lower() in ('ff', 'firefox'):
                cls.instance = webdriver.Firefox()
            else:
                raise NameError('不支持{}类型的浏览器'.format(browser))
        cls.instance.maximize_window()
        cls.instance.implicitly_wait(10)
        return cls.instance

    @classmethod
    def quit_driver(cls):
        cls.instance.quit()
        # 必须设为None
        cls.instance = None

