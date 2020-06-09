from selenium import webdriver
import os
from bs4 import BeautifulSoup as soup
import time

def get_driver(driver, url, lebel, page_no, isFirst):
    try:
        if isFirst == True:
            pass
        else:
            url = "https:" + url
        driver.get(url)
        time.sleep(5)

        old_position = 0
        new_position = 700

        for i in range(5):
            driver.execute_script("window.scrollTo(" + str(old_position) + "," + str(new_position) + ");")
            time.sleep(2)

            driver.execute_script("window.scrollTo(" + str(new_position) + "," + str(old_position) + ");")
            time.sleep(1)
            driver.execute_script("window.scrollTo(" + str(old_position) + "," + str(new_position) + ");")
            old_position = new_position
            new_position = new_position + 700
            time.sleep(4)

        driver.execute_script("window.scrollTo(" + str(new_position) + "," + str(0) + ");")

        page_soup = soup(driver.page_source, "html.parser")
        #print(page_soup)

        with open("txt_file_"+lebel+"_"+str(page_no)+".txt", "w", encoding="utf-8") as f:
            f.write("url: "+url +"\n\n"+str(page_soup))

        return {"page_soup": page_soup, "driver": driver}

    except Exception as e:
        print("error_05: " +str(e))
        pass


def scrap_url():
    try:
        root_dir = os.path.dirname(os.path.abspath(__file__))
        page_no = 0
        lebel = "0"

        driver = webdriver.Chrome(executable_path = root_dir+"\\chromedriver.exe")

        driver.maximize_window()

        #driver = webdriver.Firefox(executable_path = root_dir+"\\geckodriver.exe")
        main_url = "https://www.daraz.com.bd"
        isFirst =True
        driver_dict = get_driver(driver, main_url, lebel, page_no, isFirst)

        isFirst =False
        lebel = "1"

        driver = driver_dict["driver"]
        page_soup = driver_dict["page_soup"]

        root_ul = page_soup.find("ul", {"class": "lzd-site-menu-root"})
        root_lst = root_ul.findAll("li", {"class": "lzd-site-menu-root-item"})

        for i in range(len(root_lst)):
            try:
                sub_menu = page_soup.find("ul", {"class": "lzd-site-menu-sub Level_1_Category_No"+str(i+1)})
                sub_menu_lst_1 = sub_menu.findAll("li", {"class": "lzd-site-menu-sub-item"})
                sub_menu_lst_2 = sub_menu.findAll("li", {"class": "sub-item-remove-arrow"})

                sub_menu_lst = sub_menu_lst_1 + sub_menu_lst_2

                for grand_sub_menu in sub_menu_lst:
                    try:
                        sub_menu_url = grand_sub_menu.find("a")["href"]
                        print(sub_menu_url)

                        page_no = page_no + 1
                        lebel = "2"
                        driver_dict = get_driver(driver, sub_menu_url, lebel, page_no, isFirst)

                        driver = driver_dict["driver"]
                        page_soup = driver_dict["page_soup"]

                        grand_item = grand_sub_menu.find("ul", {"class": "lzd-site-menu-grand"})
                        grand_item_lst = grand_item.findAll("li", {"class": "lzd-site-menu-grand-item"})

                        for grand_li in grand_item_lst:
                            try:
                                grand_item_url = grand_li.find("a")["href"]
                                print(grand_item_url)

                                page_no = page_no + 1
                                lebel = "3"
                                driver_dict = get_driver(driver, grand_item_url, lebel, page_no, isFirst)

                                driver = driver_dict["driver"]
                                page_soup = driver_dict["page_soup"]

                            except Exception as e:
                                print("error_04: " +str(e))
                                pass

                    except Exception as e:
                        print("error_03: " +str(e))
                        pass

            except Exception as e:
                print("error_02: " +str(e))
                pass

    except Exception as e:
        print("error_01: " +str(e))
        pass


if __name__ == '__main__':
    scrap_url()

