from selenium.webdriver.common.by import By


class SetLanguageLocators:
    lang_menu = (By.XPATH, "//a[@id='dropdownLangauge']")
    russian_lang = (By.XPATH, "//a[@id='ru']")
    farsi_lang = (By.XPATH, "//a[@id='fa']")
    german_lang = (By.XPATH, "//a[@id='de']")
    vietnamese_lang = (By.XPATH, "//a[@id='vi']")
    french_lang = (By.XPATH, "//a[@id='fr']")
    turkish_lang = (By.XPATH, "//a[@id='tr']")
    arabic_lang = (By.XPATH, "//a[@id='ar']")
    spanish_lang = (By.XPATH, "//a[@id='es']")
    english_lang = (By.XPATH, "//a[@id='en']")


class SetCurrencyLocators:
    currency_menu = (By.CSS_SELECTOR, "#dropdownCurrency")
    usd = (By.XPATH, "//a[text()='USD']")
    gbp = (By.XPATH, "//a[text()='GBP']")
    sar = (By.XPATH, "//a[text()='SAR']")
    eur = (By.XPATH, "//a[text()='EUR']")
    pkr = (By.XPATH, "//a[text()='PKR']")
    kwd = (By.XPATH, "//a[text()='KWD']")
    egp = (By.XPATH, "//a[text()='EGP']")
    jpy = (By.XPATH, "//a[text()='JPY']")
    inr = (By.XPATH, "//a[text()='INR']")
    cny = (By.XPATH, "//a[text()='CNY']")
    rub = (By.XPATH, "//a[text()='RUB']")
    vietnam_dong = (By.XPATH, "//a[@class='dropdown-item text-center'][contains(text(),'Vietnam')]")


class LogInLocators:
    user_account_menu = (By.XPATH, "//div[contains(@class,'dropdown-login')]"
                          )
    login_link = (By.XPATH, "//a[contains(@href,'/login')][.//span[normalize-space()='Login']]")
    logout_link = (By.LINK_TEXT, "Logout")
    account_menu_button = (By.XPATH, "//button[.//span[normalize-space()='Demo User']]")
    account_link = (By.LINK_TEXT, "Account")
    sign_up_link = (By.XPATH, "//a[.//span[normalize-space()='Signup'] or .//span[normalize-space()='Sign Up']]")
    email_input = (By.ID, "email")
    password_input = (By.ID, "password")
    login_button = (By.CSS_SELECTOR, "button.btn.w-full[type='submit']")
    invalid_data_msg = (By.XPATH, "//*[contains(text(),'Invalid Credentials')]")


class HeaderNavLocators:
    home_page_link = (By.LINK_TEXT, "Home")
    blog_link = (By.LINK_TEXT, "Blog")
    offers_link = (By.LINK_TEXT, "Offers")
    company_menu = (By.LINK_TEXT, "Company")
    about_us_link = (By.LINK_TEXT, "About us")
    contact_us_link = (By.LINK_TEXT, "Contact Us")
    terms_and_conditions_link = (By.LINK_TEXT, "Company")
    privacy_policy_link = (By.LINK_TEXT, "Privacy Policy")


class SearchHotelsFormLocators:
    destination_input = (By.CSS_SELECTOR, 'input[placeholder="Search By City"]')
    checkin_input = (By.CSS_SELECTOR, 'input[placeholder="Check-in Date"]')
    checkout_input = (By.CSS_SELECTOR, 'input[placeholder="Check-out Date"]')
    adults_select = (By.NAME, 'adults')
    children_select = (By.NAME, 'children')
    rooms_select = (By.NAME, 'rooms')
    nationality_select = (By.CSS_SELECTOR, 'input[placeholder="Search country..."]')
    search_btn = (By.XPATH, "//button[contains(normalize-space(.), 'Search Hotels')]")


class SearchFlightsFormLocators:
    from_input = (By.CSS_SELECTOR, 'input[placeholder="Departure City or Airport"]')
    to_input = (By.CSS_SELECTOR, 'input[placeholder="Arrival City or Airport"]')
    departure_date = (By.CSS_SELECTOR, 'input[placeholder="Departure Date"]')
    return_date = (By.CSS_SELECTOR, 'input[placeholder="Return Date"]')
    adults = (By.NAME, 'adults')
    children = (By.NAME, 'children')
    infants = (By.NAME, 'infants')
    search_btn = (By.CSS_SELECTOR, 'button[type="submit"]')


class SearchToursFormLocators:
    destination_input = (By.CSS_SELECTOR, 'input[placeholder="Search By City"]')
    destination_hidden = (By.NAME, 'destination')
    start_date = (By.NAME, 'start_date')
    duration = (By.NAME, 'duration')
    tour_type_dropdown = (By.XPATH, "//div[contains(@class,'input-dropdown') and .//input[@name='tour_type']]//div[contains(@class,'input cursor-pointer')]")
    tour_type_option = (By.XPATH, "//div[contains(@class,'input-dropdown-item') and contains(normalize-space(.), '{0}')]")
    adults = (By.NAME, 'adults')
    children = (By.NAME, 'children')
    travelers = (By.NAME, 'travelers')
    search_btn = (By.XPATH, "//button[@type='submit' and contains(normalize-space(.), 'Search Tours')]")


class SearchTransferLocators:
    pick_up_loc = (By.CSS_SELECTOR, 'input[placeholder="City or Airport"]')
    drop_off_loc = (By.CSS_SELECTOR, 'input[placeholder="Same As Pick-up"]')
    pickup_date = (By.NAME, 'pickup_date')
    pickup_time = (By.NAME, 'pickup_time')
    return_date = (By.NAME, 'return_date')
    return_time = (By.NAME, 'return_time')
    search_btn = (By.CSS_SELECTOR, 'button[type="submit"]')


class SearchTabsLocators:
    hotels_tab = (By.XPATH, "//a[@data-name='hotels']")
    flights_tab = (By.XPATH, "//a[@data-name='flights']")
    tours_tab = (By.XPATH, "//a[@data-name='tours']")
    transfer_tab = (By.XPATH, "//a[@data-name='cars']")
    visa_tab = (By.XPATH, "//a[@data-name='visa']")


class SearchResultsLocators:
    search_title = (By.XPATH, "//h1")
    change_search_btn = (By.XPATH, "//button[@data-target='#change-search']")


class UserAccountLocators:
    welcome_msg = (By.XPATH, "//span[normalize-space()='Demo User']")
    bookings_tab = (By.LINK_TEXT, "Bookings")
    my_profile_tab = (By.LINK_TEXT, "My profile")
    wishlist_tab = (By.LINK_TEXT, "Wishlist")
    newsletter_tab = (By.LINK_TEXT, "Newsletter")
