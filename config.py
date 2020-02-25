selectors = {
    "login_user": "//input[@name='session_key']",
    "login_password": "//input[@name='session_password']",
    "login_submit": "//button[@class='sign-in-form__submit-btn']",
    "connect": "//button[text()='Connect']",
    "connect_confirm": "//span[text()='Send now']",
    "page_loaded": "//div[@class='authentication-outlet']",
    "search_actions": ".search-result__actions",
    "search_link": ".search-result__info a',
    "aria_label": "aria-label",
    "pagination_button": ".artdeco-pagination__indicator button"

}

urls = {
    "base": "https://www.linkedin.com",
    "in": "/in",
    "search": "/search/results/people/?keywords={}&origin=SWITCH_SEARCH_VERTICAL",
    "connect": "/voyager/api/growth/normInvitations"
}
