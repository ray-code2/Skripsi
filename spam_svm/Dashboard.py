#import fundamental library 
import streamlit as st
import pandas as pd
import numpy as np
import xlsxwriter

# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
#import library preprocessing 
from sklearn.svm import SVC
# from selenium.webdriver import FirefoxOptions

import re
import time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
#library Machine Learning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, recall_score, precision_score, f1_score, roc_auc_score
from sklearn.preprocessing import LabelEncoder
# from sklearn.multiclass import OneVsRestClassifier
# from sklearn.multiclass import OneVsOneClassifier
#import library ambil data komentar
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os, sys
# /home/appuser/venv/lib/python3.10/site-packages/selenium/webdriver/chrome/webdriver.py



from bs4 import BeautifulSoup
import time

from humanfriendly import format_timespan
#Visualisasi library 
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.metrics import plot_confusion_matrix, plot_roc_curve, plot_precision_recall_curve
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import joblib

# https://www.youtube.com/watch?v=EJYK3PtyJLY
import nltk
# from webdriver_manager.core.utils import ChromeType


# st.set_page_config(
#     page_title="Youtube Spam Detection",
#     page_icon="💬",
# )

def stopword_removal(words):
    list_stopwords = stopwords.words('indonesian')
    list_stopwords.extend(["nih","jess","gak","ngk","enga","jes","wkwk","tanboy","waseda boys","ken",'ya','jer',"az","ah","david","David","Jerome","jerome","justin","anya","oh","kgk","gk",  "si", 'y', 'jd', 'bang','dong' 'bangg', 'bg', 'bng', 'ygy', 'yg', 'om', 'nya','baiknya', 'berkali', 'boys', 'kali', 'kurangnya', 'mata', 'olah', 'sekurang', 'setidak', 'tama', 'tidaknya', 'waseda'])
    return [word for word in words if word not in list_stopwords]

def token(komentar):
    return word_tokenize(komentar)

@st.experimental_memo(show_spinner=False,suppress_st_warning=True)
def stemming(comment):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    do = []
    
    for v in comment:
        dt = stemmer.stem(v)
        do.append(dt)
        
    d_clean = []
    print()
    # print('Proses Stemming Mulai dari sini:')
    d_clean = " ".join(do)
    print(d_clean)
    return d_clean


    
    
# #Style 
# st.markdown("""
# <style>
# .css-1lsmgbg.egzxvld0 , .css-6x4l1z.edgvbvh3
# {
#     visibility:hidden;
# }
# </style>
# """,unsafe_allow_html=True)

# pilih_menu = st.sidebar.selectbox("Navigasi" ,('Halaman Utama','Halaman Dashboard','Tentang Aplikasi'))
def trans(komentar):
    tf = tfidf.transform(komentar)
    # print(tf)
    return tf
    # review_vector = tf.transform([komentar])
    # print(review_vector)
    # pred_text = text_classifier_linear.predict(review_vector)
def preprocess(komentar):
    komentar = komentar.lower() # mengubah menjadi huruf kecil
    komentar = komentar.encode('ascii','replace').decode('ascii') #menghilangkan Non ascii
    komentar = re.sub(r"\d+", "",komentar) # menghilangkan angka
    komentar = komentar.translate(str.maketrans('', '', '!@#$.?,-+*&^%)(]['''))
    komentar = re.sub(r"\b[a-zA-Z]\b", "", komentar) #menghilangkan single char
    komentar = re.sub("\s+", " ", komentar) #menghilangkan beberapa spasi kosong
    komentar = komentar.strip() # menghilangkan suffix dan prefix yang kosong
    return komentar


    # col3 = st.columns(1)
    # with col3:
    #     fig = plt.figure(figsize=(10, 8))
    #     df['Komentar'].value_counts()[:20].plot(kind='barh')
    #     st.pyplot(fig)
@st.cache
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

# Function 
def color_df(val):
    if val == 'bukan spam':
        color = '#116466'
    elif val == 'promosi':
       color = '#6F2232'
    else: 
        color = '#05386B'
    return f'background-color: {color}'




@st.experimental_memo(show_spinner=False,suppress_st_warning=True)
def countPlot(df):
    col1,col2 = st.columns([2,2])
    with col1:
        # fig = plt.figure(figsize=(4, 3))
        # # sns.countplot(data = df , x='Label', hue='Label', palette=['#e06666','#8cbc76','#2986cc']).set(title="Grafik Batang")
        # count = df["Label"].value_counts()
        # plt.bar(count.index, count.values, color=['#8cbc76','#e06666','#2986cc'])
        # plt.rc_context({'axes.edgecolor':'white', 'xtick.color':'white', 'ytick.color':'white'})
        with plt.rc_context({'axes.edgecolor':'white'}):
            fig, ax = plt.subplots()
            ax = df["Label"].value_counts().plot(kind="bar", color=['#116466','#6F2232','#05386B'], figsize=[4, 4],edgecolor = "white")
            plt.xticks(rotation=0, horizontalalignment="center", fontsize=12, color='#fafafa')
            # params = {'axes.edgecolor':'#fafafa'}
            ax.tick_params(colors='white', which='both') 
            plt.style.use('ggplot')
            plt.ylabel("Jumlah Data", fontsize=12, color='#fafafa')
            plt.title('Bar Plot',color='#fafafa')
            mpl.rc('text', color='#fafafa')
            mpl.rc('axes', labelcolor='#fafafa')
            plt.grid(visible=None)
            fig.patch.set_facecolor('#1A1A1D')
            ax.set_facecolor("#1A1A1D")

            for p in ax.patches:
               ax.annotate(
                   str(p.get_height()), xy=(p.get_x() + 0.20, p.get_height() + 1), fontsize=10
                )
            # name = savefig()
            # fig = latex_figure(name)
            # sns.set_theme(style="whitegrid")
            plt.savefig("test.png")
            st.pyplot(fig)
    with col2:
        fig = plt.figure(figsize=(10, 8))
        fig.patch.set_facecolor('#1A1A1D')
        ax.set_facecolor("#1A1A1D")
        counts = df['Label'].value_counts()
        counts.plot(kind='pie', autopct='%1.0f%%',colors=['#116466','#6F2232','#05386B'], textprops={'fontsize': 26,'color':"w"})
        plt.xlabel("Jumlah Data", fontsize=26, color='white')
        plt.ylabel(".", fontsize=1)
        plt.title("Pie Plot", fontsize=26, color='white')
        st.pyplot(fig)

@st.experimental_memo(show_spinner=False,suppress_st_warning=True)
def installff():
  os.system('sbase install chromedriver latest')
  os.system('ln -s /home/appuser/venv/lib/python3.10/site-packages/seleniumbase/drivers/chromedriver /home/appuser/venv/bin/chromedriver')

@st.experimental_memo(show_spinner=False,suppress_st_warning=True)
def get_driver():
    option = Options()
    option.add_argument("--headless") #headless
    option.add_argument("--mute-audio")
    option.add_argument("--disable-gpu")
    option.add_argument("--no-sandbox")
    return webdriver.Chrome(service=Service(installff()), options=option)
    
@st.experimental_memo(show_spinner=False,suppress_st_warning=True)
def ambil_komen(url, angka, semua):
    
#     chromedriver_autoinstaller.install()
#     option = Options()
#     option.binary = FirefoxBinary(r'/Applications/Firefox.app/Contents/MacOS/firefox')
#     option.binary_location = FirefoxBinary("./firefox/firefox")
#     option.add_argument("--headless") #headless
#     option.add_argument("--mute-audio")
#     option.add_argument("--disable-gpu")
#     option.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
#     option.add_argument("--no-sandbox")
#     option.add_argument("--disable-dev-shm-usage")
#     option.add_argument("--disable-features=NetworkService")
#     option.add_argument("--window-size=1920x1080")
#     option.add_argument("--disable-features=VizDisplayCompositor")
#     service = ChromeService(executable_path='/home/appuser/venv/lib/python3.10/site-packages/seleniumbase/drivers/chromedriver')
# service = service
#     service = Service(GeckoDriverManager().install())
#     serv = Service(GeckoDriverManager().install())
    driver = get_driver()
#     service.start()
    driver.get(url)
    wait = WebDriverWait(driver,25)
    if semua == True:
        prev_h = 0
        while True:
            height = driver.execute_script("""
                    function getActualHeight() {
                        return Math.max(
                            Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
                            Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
                            Math.max(document.body.clientHeight, document.documentElement.clientHeight)
                        );
                    }
                    return getActualHeight();
                """)
            driver.execute_script(f"window.scrollTo({prev_h},{prev_h + 200})")
            # fix the time sleep value according to your network connection
            time.sleep(1)
            prev_h +=200  
            if prev_h >= height:
                break
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        title_text_div = soup.select_one('#container h1')
        title = title_text_div and title_text_div.text
        data = []
        comment_div = soup.select("#content #content-text")
        for x in comment_div:
            print(x.text)
            data.append(x.text)
        elems = driver.find_elements(By.XPATH,"//div[@id='comment-content']//a[@href]")
        for elem in elems:
            print(elem.get_attribute("href"))
            data.append(elem.get_attribute("href"))
        driver.quit()
        dataframe = pd.DataFrame(data, columns=['Komentar'])
        a = dataframe['Komentar']

        #Preprocessing
        dataframe['Komentar'] = dataframe['Komentar'].apply(preprocess)
        dataframe['Komentar'] = dataframe['Komentar'].apply(token)
        dataframe['Komentar'] = dataframe['Komentar'].apply(stopword_removal)
        print()
        print('Proses Stemming Mulai dari sini')
        dataframe['Komentar'] = dataframe['Komentar'].apply(stemming)
        #klasifikasi
        D_list = []
        P_list = []
        for index, row in dataframe.iterrows():
            ubah = trans(row) #transform ke vector TFIDF
            pred_text = model.predict(ubah) # Model Prediksi
            pred_text = le.inverse_transform(pred_text) #Ubah 0 dan 1 menjadi bentuk awalnya
            score_text = model.predict_proba(ubah) #persentase dia spam promosi 
            prob_score = np.round(score_text * 100,2)
            for record in prob_score:
                r = list(map("{0:.2f}%".format, record))
                P_list.append(r)
            text = ' '.join(pred_text) #menghilangkan kurung kotak
            my_list = [row.Komentar,text]
            D_list.append(my_list)
        dt = pd.DataFrame(P_list, columns =['Probabilitas bukan spam', 'Probabilitas promosi', 'Probabilitas tautan'], dtype=str) 
        print(D_list)

        df = pd.DataFrame(D_list, columns=['Komentar setelah dibersihkan','Label'])
        df.insert(0, "Komentar original", a)
        # st.dataframe(df.style.applymap(color_df, subset=['Label']),width=3000, height=1000) #details
        # st.success('Done Klasifikasi')
        ## Judul
        st.markdown(f''' #### Judul : {title}''')
        countPlot(df)
        # promosi = df.loc[df.Label == 'promosi', 'Komentar setelah dibersihkan'].value_counts().head(10).index #10 komentar promosi
        # normal = df.loc[df.Label == 'bukan spam', 'Komentar setelah dibersihkan'].value_counts().head(10).index #10 komentar bukan spam
        excel = to_excel(df)
        with st.expander("lihat Data"):
            result = pd.concat([df, dt], axis=1)
            st.table(data= result.style.applymap(color_df, subset=['Label']))
        st.download_button(
            label="Download data",
            data=excel,
            file_name=f'{title}.xlsx',
            )
        

    else:
        for item in range(angka): #angka adalah jumlah iterasi dan per iterasi akan di scrape 20 data
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            # wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@class='input-content' or @class='style-scope' or @class='paper-input-container']")))
            time.sleep(10) #menunggu 10 detik scroll
        data = []

        # for lnk in wait.until(EC.presence_of_all_elements_located((By.XPATH, "//h2[contains(@class, 'yt-simple-endpoint style-scope yt-formatted-string')]/a"))):
        #     data.append(lnk.text)
        #     print(lnk)

        for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text "))):
            data.append(comment.text)

            # print(comment.get_attribute('href'))
            print(comment.text)
            # //a[@href] this works but not link in the comment!
            # //div[@id='comment-content']//a[@href] #ini bisa!

        elems = wait.until(lambda x: x.find_elements(By.XPATH,"//div[@id='comment-content']//a[@href]"))
        for elem in elems:
            print(elem.get_attribute("href"))
            data.append(elem.get_attribute("href"))
    
        dataframe = pd.DataFrame(data, columns=['Komentar'])
        # st.write(dataframe) 
        soup = BeautifulSoup(driver.page_source,'html.parser')
        # for link in soup.find_all('a',href=True):
        #     print(link['href'])

        title_text_div = soup.select_one('#container h1')
        title = title_text_div and title_text_div.text
        # st.session_state['judul'] = title
        driver.quit()
        a = dataframe['Komentar']
        # st.session_state['Sebelum'] = a
        # a.to_csv('data_scrape.txt',sep='\t',index=False)
        # st.success('Done Scraping')

        #Preprocessing
        dataframe['Komentar'] = dataframe['Komentar'].apply(preprocess)
        dataframe['Komentar'] = dataframe['Komentar'].apply(token)
        dataframe['Komentar'] = dataframe['Komentar'].apply(stopword_removal)
        print()
        print('proses Stemming mulai dari sini')
        dataframe['Komentar'] = dataframe['Komentar'].apply(stemming)
        # st.success('Done Preprocessing')
        #klasifikasi
        D_list = []
        P_list = []
        
        for index, row in dataframe.iterrows():
            ubah = trans(row) #transform ke vector TFIDF
            pred_text = model.predict(ubah) # Model Prediksi
            pred_text = le.inverse_transform(pred_text) #Ubah 0 dan 1 menjadi bentuk awalnya
            score_text = model.predict_proba(ubah) #persentase dia spam promosi 
            prob_score = np.round(score_text * 100,2)
            for record in prob_score:
                r = list(map("{0:.2f}%".format, record))
                P_list.append(r)
            # for record in prob_score:
            #     print(record)

            text = ' '.join(pred_text) #menghilangkan kurung kotak
            my_list = [row.Komentar,text]
            D_list.append(my_list)
        dt = pd.DataFrame(P_list, columns =['Probabilitas bukan spam', 'Probabilitas promosi', 'Probabilitas tautan'], dtype = str) 

        # print(D_list)

        df = pd.DataFrame(D_list, columns=['Komentar setelah dibersihkan','Label']) # Tambah 3 kolom persentase proba,'Bukan Spam %', 'Promosi %', 'Tautan'
        df.insert(0, "Komentar original", a)
        # # st.dataframe(df.style.applymap(color_df, subset=['Label']),width=3000, height=1000) #details
        # # st.success('Done Klasifikasi')
        # st.session_state['df'] = df
        ## Judul
        st.markdown(f''' #### Judul : {title}''')
        countPlot(df)
        # promosi = df.loc[df.Label == 'promosi', 'Komentar setelah dibersihkan'].value_counts().head(10).index #10 komentar promosi
        # normal = df.loc[df.Label == 'bukan spam', 'Komentar setelah dibersihkan'].value_counts().head(10).index #10 komentar bukan spam
        excel = to_excel(df)
        with st.expander("lihat Data"):
            result = pd.concat([df, dt], axis=1)
            st.table(data= result.style.applymap(color_df, subset=['Label']))
        st.download_button(
            label="Download data",
            data=excel,
            file_name=f'{title}.xlsx'
            )
    # col3, col4, col5 = st.columns(3)
    # with col3:
    #      with st.expander("lihat Wordcloud Promosi"):
    #         fig, ax = plt.subplots()
    #         # st.table(promosi)
    #         wc = WordCloud(width=800,height=800,min_font_size=10,background_color="black",contour_color='white')
    #         spam_wc = wc.generate(df[df['Label'] == 'promosi']['Komentar setelah dibersihkan'].str.cat(sep= " "))
    #         # plt.figure(figsize=(12,6))
    #         plt.imshow(spam_wc)
    #         plt.axis('off')
    #         st.pyplot(fig)
    # with col4:
    #      with st.expander("lihat Wordcloud bukan spam"):
    #         # st.table(normal)
    #         fig, ax = plt.subplots()
    #         wc = WordCloud(width=800,height=800,min_font_size=10,background_color="black",contour_color='orange')
    #         normal_wc = wc.generate(df[df['Label'] == 'bukan spam']['Komentar setelah dibersihkan'].str.cat(sep= " "))
    #         plt.imshow(normal_wc)
    #         plt.axis('off')
    #         st.pyplot(fig)
    # try:
    #     with col5:
    #         with st.expander("lihat Wordcloud Tautan"):
    #             fig, ax = plt.subplots()
    #             wc = WordCloud(width=800,height=800,min_font_size=10,background_color="black",contour_color='orange')
    #             tautan_wc = wc.generate(df[df['Label'] == 'tautan']['Komentar setelah dibersihkan'].str.cat(sep= " "))
    #             plt.imshow(tautan_wc)
    #             plt.axis('off')
    #             st.pyplot(fig)
    # except:
    #     st.info('Data tidak mengandung tautan!', icon="ℹ️")

#code utama


if __name__ == "__main__":
#     _ = installff()
    nltk.download('stopwords')
    le = LabelEncoder()
    path = open(r'spam_svm/data.csv')
    df = pd.read_csv(path)
    df['Label'] = le.fit_transform(df['Label'])
    X = df['Komentar'].values
    y = df['Label'].values
# print(y)
# st.write('Jumlah baris dan kolom', X.shape)
# st.write('Jumlah kelas: ',len(np.unique(y)
    list_stopwords = stopwords.words('indonesian')
    list_stopwords.extend(["nih","jess","gak","ngk","enga","jes","wkwk","tanboy","waseda boys","ken",'ya','jer',"az","ah","david","David","Jerome","jerome","justin","anya","oh","kgk","gk",  "si", 'y', 'jd', 'bang','dong' 'bangg', 'bg', 'bng', 'ygy', 'yg', 'om', 'nya','baiknya', 'berkali', 'boys', 'kali', 'kurangnya', 'mata', 'olah', 'sekurang', 'setidak', 'tama', 'tidaknya', 'waseda'])
    tfidf = TfidfVectorizer(max_features=2000, min_df=5, max_df=0.7,stop_words=list_stopwords,ngram_range=(1,3))
    text_tf = tfidf.fit_transform(X.astype('U'))
    X_train,X_test,y_train,y_test = train_test_split(text_tf,y,test_size=0.25,random_state=33)
    model = joblib.load('spam_svm/OVO') # Load model OVO
    y_pred = model.predict(X_test)
    print("Support Vector Machine")
    print('Accuracy  = ', round(accuracy_score(y_test, y_pred)*100,2),'%')
    print('Recall    = ', round(recall_score(y_test, y_pred, average='macro')*100,2),'%')
    print('Precision = ', round(precision_score(y_test, y_pred, average='macro')*100,2),'%')
    print('F1-Score  = ', round(f1_score(y_test, y_pred, average='macro')*100,2),'%')
    print("Support Vector Machine")
    print(confusion_matrix(y_test,y_pred))  
    print("Support Vector Machine")
    print(classification_report(y_test,y_pred))

    st.markdown(" ## Aplikasi Deteksi Komentar Spam Youtube dengan Metode SVM Berbasis Web")
    link_input = st.text_input('Input link dari Video Youtube: ')
    angka = 0
    pilih = st.sidebar.number_input('berapa banyak komentar yang mau di klasifikasi dari video tersebut?',min_value=0,max_value=500,step=100)
    semua = st.sidebar.checkbox('Semua Komentar')
    if pilih == 100:
        angka = 5
    elif pilih == 200:
        angka = 10
    elif pilih == 300:
        angka = 15
    elif pilih == 400:
        angka = 20
    elif pilih == 500:
        angka = 25
    else:
        angka = 0
    
    get = st.button("Klasifikasi Data")
    start = time.perf_counter()
    if get:
        if angka == 0:
            st.error('Tidak ada data yang diklasifikasi!', icon="🚨")
            st.stop()
        elif link_input == '':
            st.warning('Belum input Link!')
        else:
            with st.spinner('Dimohon tunggu sebentar...'):
                ambil_komen(link_input , angka , semua)
                end_time = time.perf_counter()
                hasil = end_time - start
                print(f"Waktu Process: {format_timespan(round(hasil,2))}")
                # st.success('Selesai')





# # uploaded_file = st.file_uploader("Choose a file")
# if uploaded_file is not None:
#     # analisis masuk sini
#     dataframe = pd.read_csv(uploaded_file)
#     a = dataframe['Komentar']
#     # dataframe.drop(columns=['Unnamed: 0'], inplace=True
#     # st.write(a)
#     st.session_state['Sebelum'] = a
#     # st.write(dataframe)
#     #text_input = st.text_input('Input komentar','Silahkan masukan komentar disini')
#     #st.markdown("***ex: Komentar yang mengandung penipuan, promosi dan ujaran kebencian***")
#     klasifikasi = st.button('Klasifikasi')
    
#     if klasifikasi:
#         my_bar = st.progress(0)
#         for percent_complete in range(100):
#             time.sleep(0.1)
#             my_bar.progress(percent_complete + 1)
#         #Preprocess data
#         dataframe.dropna()
#         # dataframe['Komentar'] = dataframe['Komentar'].apply(preprocess)
#         # dataframe['Komentar'] = dataframe['Komentar'].apply(token)
#         # dataframe['Komentar'] = dataframe['Komentar'].apply(stopword_removal)
#         # dataframe['Komentar'] = dataframe['Komentar'].apply(stemming)
#         # D_list = []

#         # for index, row in dataframe.iterrows():
#         #     ubah = trans(row) #transform ke vector TFIDF
#         #     pred_text = model.predict(ubah) # Model Prediksi
#         #     pred_text = le.inverse_transform(pred_text) #Ubah 0 dan 1 menjadi bentuk awalnya
#         #     print(pred_text)
#         #     text = ' '.join(pred_text) #menghilangkan kurung kotak
#         #     my_list = [row.Komentar,text]
#         #     D_list.append(my_list)
#         # print(D_list)
#         # df = pd.DataFrame(D_list, columns=['Sesudah','Label'])
      
#         # st.write(df)
#     st.session_state['df'] = df  
   
               
            
            
      
