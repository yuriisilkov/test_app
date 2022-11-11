class LoginPage:

    logo = "//div[@class='login_logo']"
    error_hint = "//div[@class='error-message-container error']"
    username_input = "//input[@id='user-name']"
    password_input = "//input[@id='password']"
    login_button = "//input[@id='login-button']"


class MainPage:

    logo = "//div[@class='app_logo']"
    content_tittle_of_items = "//div[@class='inventory_item_name']"
    content_descriptions_of_items = "//div[@class='inventory_item_desc']"
    content_prices_of_items = "//div[@class='inventory_item_price']"
    contents_of_items = "//div[@class='inventory_item']"
    menu_button = "//button[@id='react-burger-menu-btn']"
    logout_button = "//a[@id='logout_sidebar_link']"
