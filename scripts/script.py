
import math
import streamlit as st
import streamlit.components.v1 as components    
from scraper import scraper
from tools import high_rating, low_price, others_articles
import base64

st.markdown("<MARQUEE><h4 style='text-align: center; color: black;'>DECOUVREZ LES PROMOTIONS DE NOS PARTENAIRES</h4></MARQUEE>", unsafe_allow_html=True)

imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")
imageUrls = [
        "https://t4.ftcdn.net/jpg/02/62/03/53/360_F_262035364_gGi8uJsPl9uljis8C6oxI0w6AM7MKDLq.jpg",
        "https://ci.jumia.is/cms/1_2022/W8/D2/CI_W07_slider_VF_KFC-DATE-min.jpg",
        "https://ci.jumia.is/cms/1_2022/W8/D1/CI_W08_S_APPLIANCE.jpg",
        "https://ci.jumia.is/cms/1_2022/W8/D1/Update/CI_W08_S_Decathlon_Fevrier-slider-1.jpg2&q=80",
        "https://ae01.alicdn.com/kf/S5dc9c94195e64619a14f979b4fa9f3ae6.jpg_Q90.jpg_.webp",
        "https://ae01.alicdn.com/kf/H8b651a029f1442d4bc0a26fef7e3082bS.jpg_Q90.jpg_.webp"
    ]
selectedImageUrl = imageCarouselComponent(imageUrls=imageUrls, height=200)

if selectedImageUrl is not None:
    st.image(selectedImageUrl)


st.sidebar.image("scripts/logo.png", width=150)
st.sidebar.markdown("<h4 style='text-align: left; color: black;'>Votre comparateur de prix</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

with st.sidebar.form(key="my_form"):
    
    keyword = st.text_input("RECHERCHE", key="keyword", help="Enter your search keyword", placeholder="Enter keyword")

    budget = st.slider("BUDGET",2000, 1000000, step=1000, help="Enter your budget" )

    submit_button = st.form_submit_button("Search")
if submit_button:
    if keyword=="":
        st.sidebar.error("Please enter your keyword")
        
    else:
        resultats = scraper(keyword, budget)
        if len(resultats) == 0:
            st.warning("Aucun article ne correspond à votre recherche!!")
        else:
            st.markdown("<h4 class='titre' style='text-align: center; color: black;'>Vos recommandations</h4>", unsafe_allow_html=True)
            #resultats = sorted(resultats, key=lambda d: float(d["note"]), reverse=1)
            best_rating_pdct = high_rating(resultats)
            #resultats = sorted(resultats, key=lambda d: d["prix"], reverse=0)
            best_price_pdct= low_price(resultats)
            col1, col2, col3 = st.columns(3)
            resultats = others_articles(resultats, best_rating_pdct, best_price_pdct)

            with col1:
                st.markdown("<h4 class= 'stitre' style='text-align: left; color: black;'>Meilleur prix</h4>", unsafe_allow_html=True)
                st.image(best_price_pdct["image"])
                info = """<p class='detail' style='text-align: left; color: black;'>{}</br>
                        {} Fcfa</br>
                        {} sur 5</br>
                        Disponible sur <a title="Cliquez pour voir le produit" href={}>{}</a>
                        </p>""".format(best_price_pdct["description"], best_price_pdct["prix"], best_price_pdct["note"], best_price_pdct['url'], best_price_pdct['site'])
                st.markdown(info, unsafe_allow_html=True)
            
            with col3:
                st.markdown("<h4 class= 'stitre' style='text-align: left; color: black;'>Meilleure note</h4>", unsafe_allow_html=True)
                st.image(best_rating_pdct["image"])
                info = """<p class='detail' style='text-align: left; color: black;'>{}</br>
                        {} Fcfa</br>
                        {} sur 5</br>
                        Disponible sur <a title="Cliquez pour voir le produit" href={}>{}</a>
                        </p>""".format(best_rating_pdct["description"], best_rating_pdct["prix"], best_rating_pdct["note"], best_rating_pdct['url'], best_rating_pdct['site'])
                st.markdown(info, unsafe_allow_html=True)
            
            st.markdown("<h4 style='text-align: center; color: black;'>Autres Articles</h4>", unsafe_allow_html=True)
            #del resultats[0:2]
           
            nbre_cel =math.ceil(len(resultats) / 4)
            k = 0
            for j in range(nbre_cel):
                cols = st.columns(4)
            
                i=0
                
                for article in resultats[k:k+4]:
                    with cols[i]:
                        st.image(article['image'])
                        info = """<p class='detail' style='text-align: left; color: black;'>{}</br>
                                {} Fcfa</br>
                                {} sur 5</br>
                                Disponible sur <a title="Cliquez pour voir le produit" href={}>{}</a>
                                </p>""".format(article["description"], article["prix"], article["note"], article['url'], article['site'])
                        st.markdown(info, unsafe_allow_html=True)
                    i+=1
                      
                k+=5           

            

   

    


