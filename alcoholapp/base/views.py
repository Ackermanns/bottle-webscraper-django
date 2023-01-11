from django.shortcuts import render
from django.http import HttpResponse
import sqlite3
import os


BASE_DIR = os.getcwd()
DATABASE_DIRECTORY = os.path.join(BASE_DIR,"base\\scripts\\database\\booze.db")

# Create your views here.
def home(request):
    """home page, user should select their desired alcohol category type"""
    return render(request, 'index.html')

def category(request, category):
    """alcohol category type selected, now user should chose specific product"""
    #check to see if weblink is valid, if not link sql injection attempted?
    valid_categories = {'bourbon_whiskey', 'Gin', 'Liqueurs', 'Rum', 'Tequila', 'Vodka', 'White_Wine', 'Red_Wine'}
    if str(category) in valid_categories:
        try: #get items from db in relevant category
            conn = sqlite3.connect(DATABASE_DIRECTORY)
            c = conn.cursor()
            query = f"SELECT table_name, type, image_name FROM items WHERE real_name = '{category}' ORDER BY type;"
            c.execute(query)
            rows = c.fetchall()
            item_selection = []
            for table_name, prod_type, image_name in rows: #list of relevant items
                item_selection.append((table_name, prod_type, image_name))
            total_entries = len(item_selection)
            better_heading = category.replace("_", " ")
            better_heading = better_heading.replace("bourbon whiskey", "bourbon/whiskey")
        except:
            #render 404
            print('wrong')
        
        context = {'category':category,
                   'item_selection':item_selection,
                   'total_entries':total_entries,
                   'better_heading':better_heading}
        return render(request, 'category.html', context)
    else:
        #not a valid link
        pass

def item(request, category, item):
    try: #get items from db in relevant category
        conn = sqlite3.connect(DATABASE_DIRECTORY)
        c = conn.cursor()
        #query = f"SELECT original_price, discounted_price, website FROM {item} ORDER BY discounted_price;"
        query = f"SELECT {item}.original_price, {item}.discounted_price, {item}.website, stores.address, stores.website FROM {item}, stores WHERE {item}.store_id = stores.store_id ORDER BY {item}.discounted_price;"
        #print(query)
        context = {}
        c.execute(query)
        rows = c.fetchall()
        items = []
        for row in rows: #list of relevant items
            original_price = row[0]
            discounted_price = row[1]
            item_website = row[2]
            store_address = row[3]
            store_link = row[4]
            if (original_price == -1) and (discounted_price != -1): #only want entries with shops selling them
                if str(original_price) == '-1':
                    original_price = '-'
                else:
                    original_price = f"${original_price:.2f}"
                if str(discounted_price) == '-1':
                    original_price = '-'
                else:
                    discounted_price = f"${discounted_price:.2f}"
                items.append((original_price, discounted_price, item_website, store_address, store_link))
            elif (original_price != -1) and (discounted_price != -1):
                original_price = f"${original_price:.2f}"
                discounted_price = f"${discounted_price:.2f}"
                items.append((original_price, discounted_price, item_website, store_address, store_link))
        total_entries = len(items)
        better_heading = category.replace("_", " ")
        better_heading = better_heading.replace("bourbon whiskey", "bourbon/whiskey")
        
    except: #table not in db
        pass
    context = {'category' : category,
               'item' : item,
               'items':items,
               'total_entries':total_entries,
               'better_heading':better_heading}
               
    return render(request, 'item.html', context)