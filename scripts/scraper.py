from ast import Str
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from time import sleep
from selenium.webdriver.chrome.options import Options


DRIVER_PATH = "webdrivers/chromedriver"

options = Options()
options.add_argument('--headless')
browser = webdriver.Chrome(DRIVER_PATH, options=options)




# SCRAPING JUMIA

def scraper_jumia(keyword:str, budget=2000):
    URL = "https://www.jumia.ci/catalog/?q={}".format(keyword)
    results = requests.get(URL)
    results_content = results.content
    soup = BeautifulSoup(results_content,'html.parser' )
    try:
        table = soup.find("div",{'class': '-paxs row _no-g _4cl-3cm-shs'})
        
    except Exception:
        return []
    articles = []

    for raw in table.findAll("a", {'class':'core' }):
        article = {}
        #print(raw.find('div', attrs={'class': 'prc'}).get_text())
        if raw.find('div', attrs={'class': 'prc'}).get_text() != '':
            if int(raw.find('div', attrs={'class': 'prc'}).get_text().split(" ")[0].replace(",","")) <= budget :
        
                article["description"] = raw.get("data-name").split(",")[0]
                article["url"] = "".join(["https://www.jumia.ci/", raw.get("href")])
                article["site"] = "jumia"
                article["prix"] = int(raw.find('div', attrs={'class': 'prc'}).get_text().replace(",","").split(" ")[0])
                article["image"] = raw.div.img.get('data-src')
                try:
                    article['note'] = float(raw.find('div', {'class':'stars _s'}).get_text().split(" ")[0])
                except Exception :
                    article['note'] = 0
                articles.append(article)
        #return articles
    
    return articles




# SCRAPER ALIEXPRESS

#driver_path pour chrome 

# On va sur notre page test.html
URL = "https://AliExpress.com"

def connexion_to_AliExpress(url, driver_path) :
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.get(url)
    sleep(5)
    return driver

id_research_zone = "SearchText"

def marke_research(driver, id_research_zone, my_research):
    # On recupere la bar de recherche, on la remplit avec "iphone" puis on appuie "Entrez"
    search_bar = driver.find_element_by_name(id_research_zone)
    search_bar.send_keys(my_research)
    sleep(10)    
    # Valider la recherche
    search_bar.send_keys(Keys.ENTER)


# Get all publications available on the page
class_names_items = "_3t7zg"

def get_all_items(driver, class_names_items) : 
        # Access to all posts stories container
    publications = driver.find_elements_by_class_name(class_names_items)
    return publications





def convert_to_cfa(x):
    return 580.50*x

def get_all_variables(driver, publications):
    
    # description
    description = [x.find_element_by_tag_name('h1').text for x in publications]
    
    # prix 
    price = list()
    for prix in publications :
        x = prix.text.split("\n")
        [price.append(i) for i in x if ("$" in i and "+" not in i) ]
        
    # name
    description = [x.text.split("\n")[-1] for x in publications]
    
    # url article
    url_article = [x.get_property('href') for x in publications]
    
    
    # note 
    note = driver.find_elements_by_class_name("eXPaM")
    note = note[:10]
    note = [x.text for x in note]
    
    # photo 
    photo = driver.find_elements_by_class_name("product-img")
    photo = photo[:10]
    url_photo = [x.get_attribute('src') for x in photo]
    
    
    return description, price, url_article, note, url_photo





def scraper_aliexpress(research:Str, value=2000):
    driver = connexion_to_AliExpress(URL,DRIVER_PATH )
    marke_research(driver, id_research_zone, research)
    
    publications = get_all_items(driver , class_names_items)
    publications = publications[:10]
    
    description, price, url_article, note, url_photo = get_all_variables(driver, publications)
    
    dataframe = pd.DataFrame(list(zip(description, price, url_article, note, url_photo )),
               columns =['description', 'prix', 'url', 'note', 'image'])
    
    search = driver.find_element_by_name('SearchText')
    search.clear()
    
    dataframe["name"] = dataframe["description"].apply(lambda x : x.split(',')[0])
    
    dataframe["site"] = "AliExpress"
    
    
    dataframe["prix"] = dataframe["prix"].apply(lambda x : x.replace('$', ''))
    dataframe["prix"] = dataframe["prix"].apply(lambda x : x.replace('US', ''))
    dataframe["prix"] = dataframe["prix"].apply(lambda x : x.replace(',', ''))
    dataframe["prix"] = dataframe["prix"].apply(lambda x : convert_to_cfa(float(x)))

    # qui contre pas dans le panier value 
    dataframe = dataframe[dataframe.prix <= value]

    data = dataframe.to_dict('records')
    driver.close()
    
    return data


# SCRAPING AMAZON 

def url_article(article_rechercher):
    pattern="https://www.amazon.fr/s?k=()&__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=25RSTOC45RSY4&sprefix\
    =()%2Caps%2C260&ref=nb_sb_noss_1"
    article_rechercher=article_rechercher.replace(' ','+')
    return pattern.replace('()', article_rechercher)


def ecom_scrap(elt):
    
    try:
        acces=elt.h2
    except:
        description=""
        url="" 
    else:
        description=acces.a.span.get_text()
        url="https://www.amazon.fr"+acces.a.get("href")
    try:
        price=elt.find("span", {"class": "a-price-whole"}).text.strip(".").strip()
    except:
        prix=''
    else:
        prix =''.join(price.split(','))
   
    try:
        note=(elt.i.text).split(" ")[0].replace(",",".")
    except:
        note=0
    try:  
        image=elt.find("img", {"class": "s-image"}).get("src")
    except:
        image=""
    
    #result_recherch=(image, description, prix, note, url)
    
    results_recherch={"image":image, "description":description, "prix": prix, "note": note,"url":url, "site":"https://www.amazon.fr"}
    return results_recherch


def bon_element(resultats):
    en, et = 0,0
    resultat=[]
    for e in resultats:
        #print("----------------------")
        ed = e.find("span", {"class": "a-price"})
        eb = False if ed.__class__.__name__ == "NoneType" else True
        if eb == True:
             resultat.append(resultats[resultats.index(e)])
    return resultat


def scraper_amazon(article_rechercher, budget=2000):
    

    # Création d'une instance driver
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    
    url=r"https://www.amazon.fr"
    url = url_article(article_rechercher)
    
   
    driver.get(url)
    
    
    sel = "input#sp-cc-accept.a-button-input.celwidget"
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    bs=soup.select(sel)
    if len(bs) == 1:
        btn = driver.find_element(By.CSS_SELECTOR, sel)
        btn.click()  
   
       
        
    resultats= soup.find_all("div", {"data-component-type":"s-search-result"})
    bon_resultats=(bon_element(resultats))
    
    article=[]
    for elt in bon_resultats:
        if float(ecom_scrap(elt).get("prix")) <= budget:
            article.append(ecom_scrap(elt))

    return article
    








def scraper(keyword:str, budget=2000):
    articles = scraper_jumia(keyword, budget)
    articles.extend(scraper_aliexpress(keyword, budget))
    #articles.extend(scraper_amazon(keyword, budget))
    return articles

