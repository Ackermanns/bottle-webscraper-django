from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time


def get_Liquorland_products(selector_num, website, tablename, litres, entry_id, store_id):
    """This function will be set to work with standard liquorland website format to get store details for the database"""
    #load webpage
    driver = webdriver.Chrome(executable_path='chromedriver_win32/chromedriver.exe')
    driver.get(website)
    #click "I am ages 18 or over" button
    driver.find_element_by_xpath("/html/body/div[1]/header/div[2]/input[1]").click()

    #select region
    driver.find_element_by_xpath("/html/body/div[1]/main/form/fieldset/div[1]/span").click()
    driver.find_element_by_xpath('/html/body//div[contains(@class,"jcf-select-drop-content")]//span[@data-index="10"]').click()
    
    #select branch
    driver.find_element_by_xpath("/html/body/div[1]/main/form/fieldset/div[2]/span").click()
    driver.find_element_by_xpath(f'/html/body//div[contains(@class,"jcf-select-drop-content")]//span[@data-index="{selector_num}"]').click()
    
    #click "enter your local store" button
    driver.find_element_by_xpath("html/body/div/main/form/fieldset/input[3]").click()
    
    driver.get(website) #reload
    
    #get data
    try: #get old price
        old_price = driver.find_element_by_xpath("//span[@class = 'msrp']").get_attribute('outerHTML')
        old_price = old_price.replace('<span class="msrp">$', '')
        old_price = old_price.replace('</span>', '')
    except:
        old_price = -1 #no sale price
    print(old_price)
    try: #get current price
        current_price = driver.find_element_by_xpath("//span[@id = 'ctl00_ctl00_NestedMaster_PageContent_ctl00_BuyProductDialog1_OurPrice']").get_attribute('outerHTML')
        current_price = current_price.replace('<span id="ctl00_ctl00_NestedMaster_PageContent_ctl00_BuyProductDialog1_OurPrice">$', '')
        current_price = current_price.replace('</span>', '')
    except: #something went wrong
        current_price = -1
    print(current_price)
    
    #insert into db
    query = f'INSERT INTO {tablename} VALUES({store_id}, {entry_id}, "{old_price}", "{current_price}", "{litres}", "{website}")\n'
    
    #write to file
    f = open("temp/loadLiquorlandProducts.txt", "a+")
    f.write(query)
    f.close()    
    
    
    driver.quit()   

def load_liquorland_product(website, tablename, litres):
    """For each dropdown select option in canterbury launch a new instance of the webdriver (also to clear cashe)"""
    #get_Liquorland_products(website, tablename, litres, entry_id, store_id):
    #21 selections
    get_Liquorland_products(1, website, tablename, litres, 14, 2001)
    get_Liquorland_products(2, website, tablename, litres, 15, 2002)
    get_Liquorland_products(3, website, tablename, litres, 16, 2003)
    get_Liquorland_products(4, website, tablename, litres, 17, 2004)
    get_Liquorland_products(5, website, tablename, litres, 18, 2005)
    get_Liquorland_products(6, website, tablename, litres, 19, 2006)
    get_Liquorland_products(7, website, tablename, litres, 20, 2007)
    get_Liquorland_products(8, website, tablename, litres, 21, 2008)
    get_Liquorland_products(9, website, tablename, litres, 22, 2009)
    get_Liquorland_products(10, website, tablename, litres, 23, 2010)
    get_Liquorland_products(11, website, tablename, litres, 24, 2011)
    get_Liquorland_products(12, website, tablename, litres, 25, 2012)
    get_Liquorland_products(13, website, tablename, litres, 26, 2013)
    get_Liquorland_products(14, website, tablename, litres, 27, 2014)
    get_Liquorland_products(15, website, tablename, litres, 28, 2015)
    get_Liquorland_products(16, website, tablename, litres, 29, 2016)
    get_Liquorland_products(17, website, tablename, litres, 30, 2017)
    get_Liquorland_products(18, website, tablename, litres, 31, 2018)
    get_Liquorland_products(19, website, tablename, litres, 32, 2019)
    get_Liquorland_products(20, website, tablename, litres, 33, 2020)
    get_Liquorland_products(21, website, tablename, litres, 34, 2021)


def load_Liquorland_products():
    """Load products here"""
    #get_products(website, tablename, litres):
    load_liquorland_product("https://www.shop.liquorland.co.nz/splash.aspx?ReturnUrl=%2fJagermeister-1L-P108332.aspx", "jagermeister", "1Litre")
    load_liquorland_product("https://www.shop.liquorland.co.nz/splash.aspx?ReturnUrl=%2fbaileys-irish-cream-1l-p106680.aspx", "baileys_irish_cream", "1Litre")
    load_liquorland_product("https://www.shop.liquorland.co.nz/splash.aspx?ReturnUrl=%2fkraken-black-spiced-rum-700ml-p107825.aspx", "kraken_black", "700ml")
    load_liquorland_product("https://www.shop.liquorland.co.nz/splash.aspx?ReturnUrl=%2fJim-Beam-Bourbon-1L-P111425.aspx", "jim_beam", "1Litre")
    load_liquorland_product("https://www.shop.liquorland.co.nz/splash.aspx?ReturnUrl=%2fJack-Daniels-1L-P105816.aspx", "jack_daniels", "1Litre")
    load_liquorland_product("https://www.shop.liquorland.co.nz/splash.aspx?ReturnUrl=%2fallan-scott-sauvignon-blanc-750ml-p111073.aspx", "allan_scott_SB", "750ml")
    load_liquorland_product("https://www.shop.liquorland.co.nz/splash.aspx?ReturnUrl=%2fBabydoll-Sauvignon-Blanc-750ml-P114225.aspx", "babydoll_SB", "750ml")
    load_liquorland_product("https://www.shop.liquorland.co.nz/splash.aspx?ReturnUrl=%2fdashwood-pinot-noir-750ml-p110936.aspx", "dashwood_PN", "750ml")
    load_liquorland_product("https://www.shop.liquorland.co.nz/splash.aspx?ReturnUrl=%2fbombay-sapphire-gin-1l-p111428.aspx", "bombay_sapphire", "1Litre")
    load_liquorland_product("https://www.shop.liquorland.co.nz/splash.aspx?ReturnUrl=%2fel-jimador-blanco-tequila-750ml-p105764.aspx", "el_jimador_blanco", "750ml")
    load_liquorland_product("https://www.shop.liquorland.co.nz/splash.aspx?ReturnUrl=%2fSmirnoff-Vodka-1L-P108626.aspx", "smirnoff_red_no21", "1Litre")
    load_liquorland_product("https://www.shop.liquorland.co.nz/splash.aspx?ReturnUrl=%2fFinlandia-Vodka-1L-P106803.aspx", "finlandia", "1Litre")
    load_liquorland_product("https://www.shop.liquorland.co.nz/splash.aspx?ReturnUrl=%2fEspolon-Blanco-Tequila-700ml-P112482.aspx", "espolon_blanco", "700ml")
