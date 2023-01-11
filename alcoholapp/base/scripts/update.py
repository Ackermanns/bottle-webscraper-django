#standard libraries
from bs4 import BeautifulSoup
from selenium import webdriver

#project libraries
from dbhandler import create_table_stores, commit_queries, create_table_item
from superLiquorScraper import *
from liquorlandScraper import *
import sqlite3
import os



def main():
    #cleanup
    try:
        os.remove("temp/loadSuperliquorProducts.txt")
    except:
        print("[ERROR] could not remove temp/loadSuperliquorProducts.txt")
    try:
        os.remove("temp/loadSuperliquorStores.txt")
    except:
        print("[ERROR] could not remove temp/loadSuperliquorStores.txt")
    try:
        os.remove("temp/loadLiquorlandProducts.txt")
    except:
        print("[ERROR] could not remove temp/loadLiquorlandProducts.txt")    
    try:
        os.remove("database/booze.db")
    except:
        print("[ERROR] could not remove database/booze.db")



    #create table stores
    create_table_stores()
    #special table for items by tables
    commit_queries("temp/tableTableStatic.txt") #do not delete file!!!
    #create tables for products
    create_table_item("jagermeister")
    create_table_item("baileys_irish_cream")
    create_table_item("captain_morgan_dark")
    create_table_item("kraken_black")
    create_table_item("jim_beam")
    create_table_item("jack_daniels")
    create_table_item("allan_scott_SB")
    create_table_item("babydoll_SB")
    create_table_item("dashwood_PN")
    create_table_item("bombay_sapphire")
    create_table_item("el_jimador_blanco")
    create_table_item("smirnoff_red_no21")
    create_table_item("finlandia")
    create_table_item("espolon_blanco")
    
    
    #LOAD SUPERLIQUOR SECTION
    load_superliquor_stores()
    commit_queries("temp/loadSuperliquorStores.txt")
    load_SuperLiquor_products()
    commit_queries("temp/loadSuperliquorProducts.txt")
    
    #LOAD LIQUORLAND SECTION
    commit_queries("temp/loadLiquerLandStoresStatic.txt") #do not delete file!!!
    load_Liquorland_products()
    commit_queries("temp/loadLiquorlandProducts.txt")
    
    
    
if __name__ == "__main__":
    main()