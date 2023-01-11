from bs4 import BeautifulSoup
from selenium import webdriver

def superliquor_store_details(primary_key, region, website): #Done
    """This function will be set to work with standard superliquor website format to get store details for the database"""
    driver = webdriver.Chrome(executable_path='chromedriver_win32/chromedriver.exe')
    driver.get(website)
    content = driver.page_source
    soup = BeautifulSoup(content, features="lxml")
    driver.quit()
    details = soup.select('.master-wrapper-page .master-wrapper-content .page-body .col-md-6')[0] #may need to specify tags in future for changes
    details = str(details)
    details = details.split("<strong>")
    address = details[1][:-16]
    phone = details[2].replace(" ", "") #remove unnecessary whitespaces
    phone = phone[11:-7]
    mail = details[3].replace(" ", "")
    mail = mail[11:-74]
    query = f"INSERT INTO stores VALUES({primary_key}, '{region}','{address}',{phone},'{mail}','{website}');\n"
    #Write to temp file
    f = open("temp/loadSuperliquorStores.txt", "a+")
    f.write(query)
    f.close()

def superliquor_store_item(primary_key, store_id, item, website):
    """collects alcohol data from a website and stores it as a query in the temp query.txt file"""
    driver = webdriver.Chrome(executable_path='chromedriver_win32/chromedriver.exe')
    driver.get(website)
    content = driver.page_source
    soup = BeautifulSoup(content, features="lxml")
    driver.quit()
    try:
        get_amount = soup.select('.master-wrapper-page .master-wrapper-content .page-title')[0]
        get_amount = str(get_amount)
        get_amount = get_amount.replace('</h1></div>','')
        get_amount = get_amount.replace(' Litre','Litre')
        get_amount = get_amount.split()
        amount = get_amount[-1]
    except:
        amount = '-1'
    #may need to specify tags in future for changes
    try: #on sale and in promo
        old_price = soup.select('.master-wrapper-page .master-wrapper-content .master-column-wrapper .overview .old-product-price')[0]
        old_price = str(old_price)
        old_price = old_price.replace('<div class="old-product-price"><span>Original price:</span> <span>$','')
        old_price = old_price.replace('</span></div>','')
        current_price = soup.select('.master-wrapper-page .master-wrapper-content .master-column-wrapper .overview .product-price')[0]
        current_price = str(current_price)
        current_price = current_price.split('"')
        current_price = current_price[5]
    except: #normal fee, no sale
        try:
            old_price = '-1'
            current_price = soup.select('.master-wrapper-page .master-wrapper-content .master-column-wrapper .overview .product-price')[0]
            current_price = str(current_price)
            current_price = current_price.split('"')
            current_price = current_price[5]
        except: #out of stock, no price or unavailable
            old_price = '-1'
            current_price = '-1'
    #create query and add to file
    #if ((old_price != '-1') and (current_price != '-1')): #we do not want dead entries to database, waste of space
    query = f"INSERT INTO {item} VALUES({primary_key}, {store_id}, {old_price}, {current_price}, '{amount}', '{website}');\n"
    print(query)
    f = open("temp/loadSuperliquorProducts.txt", "a+")
    f.write(query)
    f.close()



#====================Stores====================#
def load_superliquor_stores():
    """Webscrapes liquorland store data to be saved as queries in a text file"""
    #load store data
    superliquor_store_details(1001,'Christchurch','https://www.superliquor.co.nz/super-liquor-barrington')
    superliquor_store_details(1002,'Christchurch','https://www.superliquor.co.nz/super-liquor-belfast')
    superliquor_store_details(1003,'Christchurch','https://www.superliquor.co.nz/super-liquor-brighton')
    superliquor_store_details(1004,'Christchurch','https://www.superliquor.co.nz/super-liquor-burnside')
    superliquor_store_details(1005,'Christchurch','https://www.superliquor.co.nz/super-liquor-colombo-st-sydenham')
    superliquor_store_details(1006,'Christchurch','https://www.superliquor.co.nz/super-liquor-edgeware')
    superliquor_store_details(1007,'Christchurch','https://www.superliquor.co.nz/super-liquor-elmwood')
    superliquor_store_details(1008,'Christchurch','https://www.superliquor.co.nz/super-liquor-halswell')
    superliquor_store_details(1009,'Christchurch','https://www.superliquor.co.nz/super-liquor-hornby')
    superliquor_store_details(1010,'Christchurch','https://www.superliquor.co.nz/super-liquor-ilam')
    superliquor_store_details(1011,'Christchurch','https://www.superliquor.co.nz/super-liquor-leeston')
    superliquor_store_details(1012,'Christchurch','https://www.superliquor.co.nz/super-liquor-lincoln')
    superliquor_store_details(1013,'Christchurch','https://www.superliquor.co.nz/super-liquor-papanui')
    
#====================Liqueurs====================#
def load_superliquor_jagermeister():
    item = "jagermeister"
    superliquor_store_item(1001,1,item,'https://barrington.superliquor.co.nz/jagermeister-1-litre')
    superliquor_store_item(1002,2,item,'https://belfast.superliquor.co.nz/jagermeister-1-litre')
    superliquor_store_item(1003,3,item,'https://brighton.superliquor.co.nz/jagermeister-1-litre')
    superliquor_store_item(1004,4,item,'https://burnside.superliquor.co.nz/jagermeister-1-litre')
    superliquor_store_item(1005,5,item,'https://colombostreet.superliquor.co.nz/jagermeister-1-litre')
    superliquor_store_item(1006,6,item,'https://edgeware.superliquor.co.nz/jagermeister-1-litre')
    superliquor_store_item(1007,7,item,'https://elmwood.superliquor.co.nz/jagermeister-1-litre')
    superliquor_store_item(1008,8,item,'https://halswell.superliquor.co.nz/jagermeister-1-litre')
    superliquor_store_item(1009,9,item,'https://hornby.superliquor.co.nz/jagermeister-1-litre')
    superliquor_store_item(1010,11,item,'https://ilam.superliquor.co.nz/jagermeister-1-litre')
    superliquor_store_item(1011,11,item,'https://leeston.superliquor.co.nz/jagermeister-1-litre')
    superliquor_store_item(1012,12,item,'https://lincoln.superliquor.co.nz/jagermeister-1-litre')
    superliquor_store_item(1013,13,item,'https://papanui.superliquor.co.nz/jagermeister-1-litre')

def load_superliquor_Baileys_irish_cream():
    item = "baileys_irish_cream"
    superliquor_store_item(1001,1,item,'https://barrington.superliquor.co.nz/baileys-the-original-irish-cream-1-litre')
    superliquor_store_item(1002,2,item,'https://belfast.superliquor.co.nz/baileys-the-original-irish-cream-1-litre')
    superliquor_store_item(1003,3,item,'https://brighton.superliquor.co.nz/baileys-the-original-irish-cream-1-litre')
    superliquor_store_item(1004,4,item,'https://burnside.superliquor.co.nz/baileys-the-original-irish-cream-1-litre')
    superliquor_store_item(1005,5,item,'https://colombostreet.superliquor.co.nz/baileys-the-original-irish-cream-1-litre')
    superliquor_store_item(1006,6,item,'https://edgeware.superliquor.co.nz/baileys-the-original-irish-cream-1-litre')
    superliquor_store_item(1007,7,item,'https://elmwood.superliquor.co.nz/baileys-the-original-irish-cream-1-litre')
    superliquor_store_item(1008,8,item,'https://halswell.superliquor.co.nz/baileys-the-original-irish-cream-1-litre')
    superliquor_store_item(1009,9,item,'https://hornby.superliquor.co.nz/baileys-the-original-irish-cream-1-litre')
    superliquor_store_item(1010,11,item,'https://ilam.superliquor.co.nz/baileys-the-original-irish-cream-1-litre')
    superliquor_store_item(1011,11,item,'https://leeston.superliquor.co.nz/baileys-the-original-irish-cream-1-litre')
    superliquor_store_item(1012,12,item,'https://lincoln.superliquor.co.nz/baileys-the-original-irish-cream-1-litre')
    superliquor_store_item(1013,13,item,'https://papanui.superliquor.co.nz/baileys-the-original-irish-cream-1-litre')
    
#====================Rums====================#
def load_superliquor_captain_morgan_dark():
    item = "captain_morgan_dark"
    superliquor_store_item(1001,1,item,'https://barrington.superliquor.co.nz/captain-morgan-dark-1-litre')
    superliquor_store_item(1002,2,item,'https://belfast.superliquor.co.nz/captain-morgan-dark-1-litre')
    superliquor_store_item(1003,3,item,'https://brighton.superliquor.co.nz/captain-morgan-dark-1-litre')
    superliquor_store_item(1004,4,item,'https://burnside.superliquor.co.nz/captain-morgan-dark-1-litre')
    superliquor_store_item(1005,5,item,'https://colombostreet.superliquor.co.nz/captain-morgan-dark-1-litre')
    superliquor_store_item(1006,6,item,'https://edgeware.superliquor.co.nz/captain-morgan-dark-1-litre')
    superliquor_store_item(1007,7,item,'https://elmwood.superliquor.co.nz/captain-morgan-dark-1-litre')
    superliquor_store_item(1008,8,item,'https://halswell.superliquor.co.nz/captain-morgan-dark-1-litre')
    superliquor_store_item(1009,9,item,'https://hornby.superliquor.co.nz/captain-morgan-dark-1-litre')
    superliquor_store_item(1010,11,item,'https://ilam.superliquor.co.nz/captain-morgan-dark-1-litre')
    superliquor_store_item(1011,11,item,'https://leeston.superliquor.co.nz/captain-morgan-dark-1-litre')
    superliquor_store_item(1012,12,item,'https://lincoln.superliquor.co.nz/captain-morgan-dark-1-litre')
    superliquor_store_item(1013,13,item,'https://papanui.superliquor.co.nz/captain-morgan-dark-1-litre')
    
def load_superliquor_kraken_black():
    item = "kraken_black"
    superliquor_store_item(1001,1,item,'https://barrington.superliquor.co.nz/kraken-black-spiced-rum-700ml')
    superliquor_store_item(1002,2,item,'https://belfast.superliquor.co.nz/kraken-black-spiced-rum-700ml')
    superliquor_store_item(1003,3,item,'https://brighton.superliquor.co.nz/kraken-black-spiced-rum-700ml')
    superliquor_store_item(1004,4,item,'https://burnside.superliquor.co.nz/kraken-black-spiced-rum-700ml')
    superliquor_store_item(1005,5,item,'https://colombostreet.superliquor.co.nz/kraken-black-spiced-rum-700ml')
    superliquor_store_item(1006,6,item,'https://edgeware.superliquor.co.nz/kraken-black-spiced-rum-700ml')
    superliquor_store_item(1007,7,item,'https://elmwood.superliquor.co.nz/kraken-black-spiced-rum-700ml')
    superliquor_store_item(1008,8,item,'https://halswell.superliquor.co.nz/kraken-black-spiced-rum-700ml')
    superliquor_store_item(1009,9,item,'https://hornby.superliquor.co.nz/kraken-black-spiced-rum-700ml')
    superliquor_store_item(1010,11,item,'https://ilam.superliquor.co.nz/kraken-black-spiced-rum-700ml')
    superliquor_store_item(1011,11,item,'https://leeston.superliquor.co.nz/kraken-black-spiced-rum-700ml')
    superliquor_store_item(1012,12,item,'https://lincoln.superliquor.co.nz/kraken-black-spiced-rum-700ml')
    superliquor_store_item(1013,13,item,'https://papanui.superliquor.co.nz/kraken-black-spiced-rum-700ml')    
    
#====================Bourbons/Whiskeys====================#
def load_superliquor_jim_beam():
    item = "jim_beam"
    superliquor_store_item(1001,1,item,'https://barrington.superliquor.co.nz/jim-beam-white-label-bourbon-1-litre')
    superliquor_store_item(1002,2,item,'https://belfast.superliquor.co.nz/jim-beam-white-label-bourbon-1-litre')
    superliquor_store_item(1003,3,item,'https://brighton.superliquor.co.nz/jim-beam-white-label-bourbon-1-litre')
    superliquor_store_item(1004,4,item,'https://burnside.superliquor.co.nz/jim-beam-white-label-bourbon-1-litre')
    superliquor_store_item(1005,5,item,'https://colombostreet.superliquor.co.nz/jim-beam-white-label-bourbon-1-litre')
    superliquor_store_item(1006,6,item,'https://edgeware.superliquor.co.nz/jim-beam-white-label-bourbon-1-litre')
    superliquor_store_item(1007,7,item,'https://elmwood.superliquor.co.nz/jim-beam-white-label-bourbon-1-litre')
    superliquor_store_item(1008,8,item,'https://halswell.superliquor.co.nz/jim-beam-white-label-bourbon-1-litre')
    superliquor_store_item(1009,9,item,'https://hornby.superliquor.co.nz/jim-beam-white-label-bourbon-1-litre')
    superliquor_store_item(1010,11,item,'https://ilam.superliquor.co.nz/jim-beam-white-label-bourbon-1-litre')
    superliquor_store_item(1011,11,item,'https://leeston.superliquor.co.nz/jim-beam-white-label-bourbon-1-litre')
    superliquor_store_item(1012,12,item,'https://lincoln.superliquor.co.nz/jim-beam-white-label-bourbon-1-litre')
    superliquor_store_item(1013,13,item,'https://papanui.superliquor.co.nz/jim-beam-white-label-bourbon-1-litre')
    
def load_superliquor_jack_daniels():
    item = "jack_daniels"
    superliquor_store_item(1001,1,item,'https://barrington.superliquor.co.nz/jack-daniels-tennessee-whiskey-1-litre')
    superliquor_store_item(1002,2,item,'https://belfast.superliquor.co.nz/jack-daniels-tennessee-whiskey-1-litre')
    superliquor_store_item(1003,3,item,'https://brighton.superliquor.co.nz/jack-daniels-tennessee-whiskey-1-litre')
    superliquor_store_item(1004,4,item,'https://burnside.superliquor.co.nz/jack-daniels-tennessee-whiskey-1-litre')
    superliquor_store_item(1005,5,item,'https://colombostreet.superliquor.co.nz/jack-daniels-tennessee-whiskey-1-litre')
    superliquor_store_item(1006,6,item,'https://edgeware.superliquor.co.nz/jack-daniels-tennessee-whiskey-1-litre')
    superliquor_store_item(1007,7,item,'https://elmwood.superliquor.co.nz/jack-daniels-tennessee-whiskey-1-litre')
    superliquor_store_item(1008,8,item,'https://halswell.superliquor.co.nz/jack-daniels-tennessee-whiskey-1-litre')
    superliquor_store_item(1009,9,item,'https://hornby.superliquor.co.nz/jack-daniels-tennessee-whiskey-1-litre')
    superliquor_store_item(1010,11,item,'https://ilam.superliquor.co.nz/jack-daniels-tennessee-whiskey-1-litre')
    superliquor_store_item(1011,11,item,'https://leeston.superliquor.co.nz/jack-daniels-tennessee-whiskey-1-litre')
    superliquor_store_item(1012,12,item,'https://lincoln.superliquor.co.nz/jack-daniels-tennessee-whiskey-1-litre')
    superliquor_store_item(1013,13,item,'https://papanui.superliquor.co.nz/jack-daniels-tennessee-whiskey-1-litre')

#====================Gin====================#
def load_superliquor_bombay_sapphire():
    item = "bombay_sapphire"
    superliquor_store_item(1001,1,item,'https://barrington.superliquor.co.nz/bombay-sapphire-1-litre')
    superliquor_store_item(1002,2,item,'https://belfast.superliquor.co.nz/bombay-sapphire-1-litre')
    superliquor_store_item(1003,3,item,'https://brighton.superliquor.co.nz/bombay-sapphire-1-litre')
    superliquor_store_item(1004,4,item,'https://burnside.superliquor.co.nz/bombay-sapphire-1-litre')
    superliquor_store_item(1005,5,item,'https://colombostreet.superliquor.co.nz/bombay-sapphire-1-litre')
    superliquor_store_item(1006,6,item,'https://edgeware.superliquor.co.nz/bombay-sapphire-1-litre')
    superliquor_store_item(1007,7,item,'https://elmwood.superliquor.co.nz/bombay-sapphire-1-litre')
    superliquor_store_item(1008,8,item,'https://halswell.superliquor.co.nz/bombay-sapphire-1-litre')
    superliquor_store_item(1009,9,item,'https://hornby.superliquor.co.nz/bombay-sapphire-1-litre')
    superliquor_store_item(1010,11,item,'https://ilam.superliquor.co.nz/bombay-sapphire-1-litre')
    superliquor_store_item(1011,11,item,'https://leeston.superliquor.co.nz/bombay-sapphire-1-litre')
    superliquor_store_item(1012,12,item,'https://lincoln.superliquor.co.nz/bombay-sapphire-1-litre')
    superliquor_store_item(1013,13,item,'https://papanui.superliquor.co.nz/bombay-sapphire-1-litre')

#====================Tequila====================#
def load_superliquor_el_jimador_blanco():
    item = "el_jimador_blanco"
    superliquor_store_item(1001,1,item,'https://barrington.superliquor.co.nz/el-jimador-blanco-tequila-700ml')
    superliquor_store_item(1002,2,item,'https://belfast.superliquor.co.nz/el-jimador-blanco-tequila-700ml')
    superliquor_store_item(1003,3,item,'https://brighton.superliquor.co.nz/el-jimador-blanco-tequila-700ml')
    superliquor_store_item(1004,4,item,'https://burnside.superliquor.co.nz/el-jimador-blanco-tequila-700ml')
    superliquor_store_item(1005,5,item,'https://colombostreet.superliquor.co.nz/el-jimador-blanco-tequila-700ml')
    superliquor_store_item(1006,6,item,'https://edgeware.superliquor.co.nz/el-jimador-blanco-tequila-700ml')
    superliquor_store_item(1007,7,item,'https://elmwood.superliquor.co.nz/el-jimador-blanco-tequila-700ml')
    superliquor_store_item(1008,8,item,'https://halswell.superliquor.co.nz/el-jimador-blanco-tequila-700ml')
    superliquor_store_item(1009,9,item,'https://hornby.superliquor.co.nz/el-jimador-blanco-tequila-700ml')
    superliquor_store_item(1010,11,item,'https://ilam.superliquor.co.nz/el-jimador-blanco-tequila-700ml')
    superliquor_store_item(1011,11,item,'https://leeston.superliquor.co.nz/el-jimador-blanco-tequila-700ml')
    superliquor_store_item(1012,12,item,'https://lincoln.superliquor.co.nz/el-jimador-blanco-tequila-700ml')
    superliquor_store_item(1013,13,item,'https://papanui.superliquor.co.nz/el-jimador-blanco-tequila-700ml')
    
def load_superliquor_espolon_lanco():
    item = "espolon_blanco"
    superliquor_store_item(1001,1,item,'https://barrington.superliquor.co.nz/espolon-blanco-tequila-700ml')
    superliquor_store_item(1002,2,item,'https://belfast.superliquor.co.nz/espolon-blanco-tequila-700ml')
    superliquor_store_item(1003,3,item,'https://brighton.superliquor.co.nz/espolon-blanco-tequila-700ml')
    superliquor_store_item(1004,4,item,'https://burnside.superliquor.co.nz/espolon-blanco-tequila-700ml')
    superliquor_store_item(1005,5,item,'https://colombostreet.superliquor.co.nz/espolon-blanco-tequila-700ml')
    superliquor_store_item(1006,6,item,'https://edgeware.superliquor.co.nz/espolon-blanco-tequila-700ml')
    superliquor_store_item(1007,7,item,'https://elmwood.superliquor.co.nz/espolon-blanco-tequila-700ml')
    superliquor_store_item(1008,8,item,'https://halswell.superliquor.co.nz/espolon-blanco-tequila-700ml')
    superliquor_store_item(1009,9,item,'https://hornby.superliquor.co.nz/espolon-blanco-tequila-700ml')
    superliquor_store_item(1010,11,item,'https://ilam.superliquor.co.nz/espolon-blanco-tequila-700ml')
    superliquor_store_item(1011,11,item,'https://leeston.superliquor.co.nz/espolon-blanco-tequila-700ml')
    superliquor_store_item(1012,12,item,'https://lincoln.superliquor.co.nz/espolon-blanco-tequila-700ml')
    superliquor_store_item(1013,13,item,'https://papanui.superliquor.co.nz/espolon-blanco-tequila-700ml')    

#====================Vodka====================#
def load_superliquor_smirnoff_red_no21():
    item = "smirnoff_red_no21"
    superliquor_store_item(1001,1,item,'https://barrington.superliquor.co.nz/smirnoff-red-no21-vodka-1-litre')
    superliquor_store_item(1002,2,item,'https://belfast.superliquor.co.nz/smirnoff-red-no21-vodka-1-litre')
    superliquor_store_item(1003,3,item,'https://brighton.superliquor.co.nz/smirnoff-red-no21-vodka-1-litre')
    superliquor_store_item(1004,4,item,'https://burnside.superliquor.co.nz/smirnoff-red-no21-vodka-1-litre')
    superliquor_store_item(1005,5,item,'https://colombostreet.superliquor.co.nz/smirnoff-red-no21-vodka-1-litre')
    superliquor_store_item(1006,6,item,'https://edgeware.superliquor.co.nz/smirnoff-red-no21-vodka-1-litre')
    superliquor_store_item(1007,7,item,'https://elmwood.superliquor.co.nz/smirnoff-red-no21-vodka-1-litre')
    superliquor_store_item(1008,8,item,'https://halswell.superliquor.co.nz/smirnoff-red-no21-vodka-1-litre')
    superliquor_store_item(1009,9,item,'https://hornby.superliquor.co.nz/smirnoff-red-no21-vodka-1-litre')
    superliquor_store_item(1010,11,item,'https://ilam.superliquor.co.nz/smirnoff-red-no21-vodka-1-litre')
    superliquor_store_item(1011,11,item,'https://leeston.superliquor.co.nz/smirnoff-red-no21-vodka-1-litre')
    superliquor_store_item(1012,12,item,'https://lincoln.superliquor.co.nz/smirnoff-red-no21-vodka-1-litre')
    superliquor_store_item(1013,13,item,'https://papanui.superliquor.co.nz/smirnoff-red-no21-vodka-1-litre')

def load_superliquor_finlandia():
    item = "finlandia"
    superliquor_store_item(1001,1,item,'https://barrington.superliquor.co.nz/finlandia-vodka-1-litre')
    superliquor_store_item(1002,2,item,'https://belfast.superliquor.co.nz/finlandia-vodka-1-litre')
    superliquor_store_item(1003,3,item,'https://brighton.superliquor.co.nz/finlandia-vodka-1-litre')
    superliquor_store_item(1004,4,item,'https://burnside.superliquor.co.nz/finlandia-vodka-1-litre')
    superliquor_store_item(1005,5,item,'https://colombostreet.superliquor.co.nz/finlandia-vodka-1-litre')
    superliquor_store_item(1006,6,item,'https://edgeware.superliquor.co.nz/finlandia-vodka-1-litre')
    superliquor_store_item(1007,7,item,'https://elmwood.superliquor.co.nz/finlandia-vodka-1-litre')
    superliquor_store_item(1008,8,item,'https://halswell.superliquor.co.nz/finlandia-vodka-1-litre')
    superliquor_store_item(1009,9,item,'https://hornby.superliquor.co.nz/finlandia-vodka-1-litre')
    superliquor_store_item(1010,11,item,'https://ilam.superliquor.co.nz/finlandia-vodka-1-litre')
    superliquor_store_item(1011,11,item,'https://leeston.superliquor.co.nz/finlandia-vodka-1-litre')
    superliquor_store_item(1012,12,item,'https://lincoln.superliquor.co.nz/finlandia-vodka-1-litre')
    superliquor_store_item(1013,13,item,'https://papanui.superliquor.co.nz/finlandia-vodka-1-litre')
#====================White Wines====================#
def load_superliquor_allan_scott_SB():
    item = "allan_scott_SB"
    superliquor_store_item(1001,1,item,'https://barrington.superliquor.co.nz/allan-scott-sauvignon-blanc-750ml')
    superliquor_store_item(1002,2,item,'https://belfast.superliquor.co.nz/allan-scott-sauvignon-blanc-750ml')
    superliquor_store_item(1003,3,item,'https://brighton.superliquor.co.nz/allan-scott-sauvignon-blanc-750ml')
    superliquor_store_item(1004,4,item,'https://burnside.superliquor.co.nz/allan-scott-sauvignon-blanc-750ml')
    superliquor_store_item(1005,5,item,'https://colombostreet.superliquor.co.nz/allan-scott-sauvignon-blanc-750ml')
    superliquor_store_item(1006,6,item,'https://edgeware.superliquor.co.nz/allan-scott-sauvignon-blanc-750ml')
    superliquor_store_item(1007,7,item,'https://elmwood.superliquor.co.nz/allan-scott-sauvignon-blanc-750ml')
    superliquor_store_item(1008,8,item,'https://halswell.superliquor.co.nz/allan-scott-sauvignon-blanc-750ml')
    superliquor_store_item(1009,9,item,'https://hornby.superliquor.co.nz/allan-scott-sauvignon-blanc-750ml')
    superliquor_store_item(1010,11,item,'https://ilam.superliquor.co.nz/allan-scott-sauvignon-blanc-750ml')
    superliquor_store_item(1011,11,item,'https://leeston.superliquor.co.nz/allan-scott-sauvignon-blanc-750ml')
    superliquor_store_item(1012,12,item,'https://lincoln.superliquor.co.nz/allan-scott-sauvignon-blanc-750ml')
    superliquor_store_item(1013,13,item,'https://papanui.superliquor.co.nz/allan-scott-sauvignon-blanc-750ml')
    
def load_superliquor_babydoll_SB():
    item = "babydoll_SB"
    superliquor_store_item(1001,1,item,'https://barrington.superliquor.co.nz/babydoll-sauvignon-blanc-750ml')
    superliquor_store_item(1002,2,item,'https://belfast.superliquor.co.nz/babydoll-sauvignon-blanc-750ml')
    superliquor_store_item(1003,3,item,'https://brighton.superliquor.co.nz/babydoll-sauvignon-blanc-750ml')
    superliquor_store_item(1004,4,item,'https://burnside.superliquor.co.nz/babydoll-sauvignon-blanc-750ml')
    superliquor_store_item(1005,5,item,'https://colombostreet.superliquor.co.nz/babydoll-sauvignon-blanc-750ml')
    superliquor_store_item(1006,6,item,'https://edgeware.superliquor.co.nz/babydoll-sauvignon-blanc-750ml')
    superliquor_store_item(1007,7,item,'https://elmwood.superliquor.co.nz/babydoll-sauvignon-blanc-750ml')
    superliquor_store_item(1008,8,item,'https://halswell.superliquor.co.nz/babydoll-sauvignon-blanc-750ml')
    superliquor_store_item(1009,9,item,'https://hornby.superliquor.co.nz/babydoll-sauvignon-blanc-750ml')
    superliquor_store_item(1010,11,item,'https://ilam.superliquor.co.nz/babydoll-sauvignon-blanc-750ml')
    superliquor_store_item(1011,11,item,'https://leeston.superliquor.co.nz/babydoll-sauvignon-blanc-750ml')
    superliquor_store_item(1012,12,item,'https://lincoln.superliquor.co.nz/babydoll-sauvignon-blanc-750ml')
    superliquor_store_item(1013,13,item,'https://papanui.superliquor.co.nz/babydoll-sauvignon-blanc-750ml')

#====================Red Wines====================#
def load_superliquor_dashwood_PN():
    item = "dashwood_PN"
    superliquor_store_item(1001,1,item,'https://barrington.superliquor.co.nz/dashwood-pinot-noir-750ml')
    superliquor_store_item(1002,2,item,'https://belfast.superliquor.co.nz/dashwood-pinot-noir-750ml')
    superliquor_store_item(1003,3,item,'https://brighton.superliquor.co.nz/dashwood-pinot-noir-750ml')
    superliquor_store_item(1004,4,item,'https://burnside.superliquor.co.nz/dashwood-pinot-noir-750ml')
    superliquor_store_item(1005,5,item,'https://colombostreet.superliquor.co.nz/dashwood-pinot-noir-750ml')
    superliquor_store_item(1006,6,item,'https://edgeware.superliquor.co.nz/dashwood-pinot-noir-750ml')
    superliquor_store_item(1007,7,item,'https://elmwood.superliquor.co.nz/dashwood-pinot-noir-750ml')
    superliquor_store_item(1008,8,item,'https://halswell.superliquor.co.nz/dashwood-pinot-noir-750ml')
    superliquor_store_item(1009,9,item,'https://hornby.superliquor.co.nz/dashwood-pinot-noir-750ml')
    superliquor_store_item(1010,11,item,'https://ilam.superliquor.co.nz/dashwood-pinot-noir-750ml')
    superliquor_store_item(1011,11,item,'https://leeston.superliquor.co.nz/dashwood-pinot-noir-750ml')
    superliquor_store_item(1012,12,item,'https://lincoln.superliquor.co.nz/dashwood-pinot-noir-750ml')
    superliquor_store_item(1013,13,item,'https://papanui.superliquor.co.nz/dashwood-pinot-noir-750ml')

def load_SuperLiquor_products():
    load_superliquor_espolon_lanco()
    load_superliquor_jagermeister()
    load_superliquor_Baileys_irish_cream()
    load_superliquor_captain_morgan_dark()
    load_superliquor_kraken_black()
    load_superliquor_jim_beam()
    load_superliquor_jack_daniels()
    load_superliquor_allan_scott_SB()
    load_superliquor_babydoll_SB()
    load_superliquor_dashwood_PN()
    load_superliquor_bombay_sapphire()
    load_superliquor_el_jimador_blanco()
    load_superliquor_smirnoff_red_no21()
    load_superliquor_finlandia()    
