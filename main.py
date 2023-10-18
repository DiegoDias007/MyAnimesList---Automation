from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from time import sleep

def site_login(page):
    try:
        page.click("a.btn-login")
        page.fill("input#loginUserName", "Your Username")
        page.fill("input#login-password", "Your Password")
        page.click("input.inputButton")
        return page
    except Exception as exc:
        print(f"An exception ocurred: {str(exc)}")

def extract_text(anime, selector):
    try:
        text = anime.css_first(selector).text(strip=True)
        if text != "N/A":
            return text
        return 0
    except AttributeError as err:
        print(f"An error ocurred while extracting text: {err}")
        return 0

def save_anime_list(page, identifier):
    page.click(f'span.ga-click[data-ga-click-param="aid:{identifier}"]')
    page.wait_for_load_state()
    
    frame = page.frame_locator("iframe#fancybox-frame")

    submit_button = frame.locator("input.inputButton.main_submit[type=button][value=Submit]").nth(1) 
    submit_button.click()
    
    sleep(2)

    page.click("a#fancybox-close")

    sleep(2)
    
def get_data(html, page):
    page = site_login(page)
    animes = html.css("div.js-anime-category-producer")
    sleep(10)
    for anime in animes:
        grade = extract_text(anime, "div.scormem-item.score")
        if float(grade) >= 7.7:
            attributes = anime.css_first("span.ga-click").attributes
            anime_identifier = attributes["data-ga-click-param"].replace("aid:", "")
            save_anime_list(page, anime_identifier)
        
def parse_html(page):
    html = HTMLParser(page.content())
    return html

def main():
    with sync_playwright() as pw:
        url = "https://myanimelist.net/anime/season"
        
        browser = pw.chromium.launch()
        page = browser.new_page()
         
        page.goto(url)
        html = parse_html(page)
        get_data(html, page)
        
        browser.close()

if __name__ == "__main__":
    main()
