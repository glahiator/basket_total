from selenium import webdriver  
import emoji

ok = emoji.emojize(":check_mark:")
warn = emoji.emojize(":red_exclamation_mark:")
info = emoji.emojize(":information:") 

def get_browser_options() :
    _options = webdriver.ChromeOptions()
    _options.binary_location = r"C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
    _options.add_argument('--ignore-certificate-errors-spki-list')
    _options.add_argument('--ignore-ssl-errors')
    _options.add_argument('log-level=3')
    _options.add_argument("--disable-blink-features=AutomationControlled")

    _options.add_argument("enable-automation")
    _options.add_argument("--headless")
    # _options.add_argument("--window-size=1920,1080")
    _options.add_argument("--no-sandbox")
    _options.add_argument("--disable-extensions")
    _options.add_argument("--dns-prefetch-disable")
    _options.add_argument("--disable-gpu")
    _options.add_argument("--force-device-scale-factor=1")
    _options.page_load_strategy = "normal"
    return _options

if __name__ == "__main__":
    pass

