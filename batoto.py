#!/usr/bin/python3

# This is a basic example of how to save images from bato.to using selenium with Firefox (on linux)
#
# You'll need the gekodriver from here:  https://github.com/mozilla/geckodriver/releases

import os
import cloudscraper
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


chapters = [
    "https://bato.to/chapter/1730317",
    "https://bato.to/chapter/1732242"
]  # List or chapters to get.  (These are just random examples.)


def main():
    firefoxOptions = Options()
    firefoxOptions.add_argument("-headless")  # No Firefox GUI window displayed
    dest_folder = os.path.join(os.getcwd(), "_Batoto")
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    print("Saving to: " + str(dest_folder))
    for chapter in chapters:
        browser = webdriver.Firefox(executable_path="/home/USERNAME/bin/geckodriver", options=firefoxOptions, service_log_path=os.devnull)  # os.devnull = No log file created
        browser.get(chapter)
        title = str(browser.title)
        if "- Chapter " in title:
            title = title.replace("- Chapter ", "c")  # I prefer 'c##' to '- Chapter ##'
        print(str(title))
        images = browser.find_elements_by_tag_name('img')
        scraper = cloudscraper.create_scraper()
        loop = 1
        for image in images:
            if "logo-batoto.png" in image.get_attribute('src'):
                pass  # Skip the logo image
            else:
                r = scraper.get(image.get_attribute('src'), headers={'referer': "https://bato.to/"})
                if r.status_code == 200:
                    extension = image.get_attribute('src').split(".")
                    extension = extension[len(extension) - 1]
                    extension = extension.split("?")
                    extension = extension[0]
                    extension = "." + extension
                    if extension == ".jpeg":
                        extension = ".jpg"
                    dest_filename = title + " " + str(loop).zfill(3)
                    outfile = os.path.join(dest_folder, dest_filename + extension)
                    print("     Downloading \'" + image.get_attribute('src') + "\' as \'" + str(dest_filename) + str(extension) + "\'")
                    try:
                        with open(outfile, 'wb') as f:
                            f.write(r.content)
                    except Exception as e:
                        print("!!!!! Failed to download file = " + str(e))
                else:
                    print("!!!!! Failed to download file = (status code = " + str(r.status_code) + ")")
                loop = loop + 1
        browser.quit()
        print("     Done")


if __name__ == "__main__":
    main()
