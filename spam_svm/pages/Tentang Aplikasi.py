import streamlit as st
#Style 

st.set_page_config(
    page_title="Tentang Aplikasi",
    page_icon="ℹ️",
)

#Style 
st.markdown("""
<style>
.css-1lsmgbg.egzxvld0 , .css-6x4l1z.edgvbvh3
{
    visibility:hidden;
}
</style>
""",unsafe_allow_html=True)

st.markdown(" ## Aplikasi Deteksi Komentar Spam Youtube dengan Metode SVM Berbasis Web")
st.markdown(' ##### Deskripsi Aplikasi:', unsafe_allow_html=True)
st.markdown(''' ###### Aplikasi ini adalah sebuah aplikasi berbasis website yang menerapkan metode Support Vector Machine dalam melakukan klasifikasi data komentar youtube.''')
st.markdown(''' ##### Fungsi dari Aplikasi:''')
st.markdown(''' ###### 1. Dapat membedakan berbagai jenis komentar yang ada pada video youtube berdasarkan 3 kategori. ''')
st.markdown(''' ###### 2. Mempermudah proses labelling data.''')
st.markdown(''' ###### 3. Membantu para content creator menganalisis komentar para penonton.''')
st.markdown(''' ##### Cara menggunakan Aplikasi:''')
st.markdown(''' ###### 1. kunjungi youtube.com''')
st.markdown(''' ###### 2. Copy link video youtube yang dipilih ''')
st.markdown(''' ###### 3. Paste link video youtube pada Aplikasi''')
st.markdown(''' ###### 4. Memilih berapa banyak komentar yang ingin diklasifikasi dari link tersebut''')
st.markdown(''' ###### 5. Download Hasil Klasifikasi''')

footer="""<style>

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #1A1A1D;
color: #fafafa;
text-align: center;
}
</style>
<div class="footer">
<p>Dibuat oleh Raymond Tjahyadi NPM: 535190030 <a style='display: block; text-align: center;'</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
