import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import base64

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Project Ahi-AI", layout="centered", page_icon="🛡️")

# --- FONKSİYONLAR ---
def temizle_pdf_icin(metin):
    if not isinstance(metin, str): return str(metin)
    ceviri = str.maketrans("ğĞüÜşŞıİöÖçÇ", "gGuUsSiIoOcC")
    metin = metin.translate(ceviri)
    # Latin-1 uyumlu hale getir
    return metin.encode('latin-1', 'ignore').decode('latin-1')

def radar_ciz(kategoriler, puanlar):
    puanlar_grafik = puanlar + [puanlar[0]]
    acilar = np.linspace(0, 2 * np.pi, len(kategoriler), endpoint=False).tolist() + [0]
    
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    
    # Eksen Yazıları
    plt.xticks(acilar[:-1], kategoriler, size=10, color="black", weight='bold')
    
    # Y Eksen (Halkalar)
    ax.set_rlabel_position(0)
    plt.yticks([2,4,6,8,10], ["2","4","6","8","10"], color="grey", size=7)
    plt.ylim(0, 10)
    
    # Çizim
    ax.plot(acilar, puanlar_grafik, linewidth=2, linestyle='solid', color='#D2691E')
    ax.fill(acilar, puanlar_grafik, '#D2691E', alpha=0.3)
    
    # Arkaplanı temizle
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#fafafa')
    
    return fig

def pdf_yap(isim, yorum, fig_radar):
    pdf = FPDF()
    pdf.add_page()
    
    # Başlık
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(139, 69, 19)
    pdf.cell(0, 15, "PROJECT AHI-AI", 0, 1, 'C')
    
    # İsim
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Rapor Sahibi: {temizle_pdf_icin(isim)}", 0, 1, 'C')
    
    # Grafik
    fig_radar.savefig("temp_radar.png", bbox_inches='tight')
    pdf.image("temp_radar.png", x=60, y=40, w=90)
    
    # Yorum
    pdf.set_y(140)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 6, temizle_pdf_icin(yorum))
    
    # Dosya çıktısı
    dosya_adi = f"Rapor_{temizle_pdf_icin(isim)}.pdf"
    pdf.output(dosya_adi)
    return dosya_adi

# --- ARAYÜZ ---
st.title("🛡️ PROJECT AHI-AI")
st.markdown("**Geleneksel Değerler & Modern Yetkinlik Analizi**")
st.markdown("---")

# Veri Giriş Alanı
ad = st.text_input("Öğrenci Adı Soyadı", "Örnek Öğrenci")

col1, col2 = st.columns(2)
puan_skalasi = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

with col1:
    st.subheader("📜 Ahilik Değerleri")
    p1 = st.selectbox("Sabır", puan_skalasi, index=6)
    p2 = st.selectbox("Cömertlik", puan_skalasi, index=7)
    p3 = st.selectbox("Ahlak", puan_skalasi, index=8)
    p4 = st.selectbox("Yarenlik", puan_skalasi, index=5)

with col2:
    st.subheader("💻 Teknik Beceriler")
    p5 = st.selectbox("Dijital", puan_skalasi, index=4)
    p6 = st.selectbox("Mantık", puan_skalasi, index=5)
    p7 = st.selectbox("Girişim", puan_skalasi, index=3)

st.markdown("---")

# Buton
if st.button("ANALİZ ET VE RAPORLA", type="primary"):
    kategoriler = ['Sabır', 'Cömertlik', 'Ahlak', 'Yarenlik', 'Dijital', 'Mantık', 'Girişim']
    puanlar = [p1, p2, p3, p4, p5, p6, p7]
    genel_ort = sum(puanlar) / 7
    
    st.success(f"Analiz Tamamlandı! Ortalama: {genel_ort:.1f}")
    
    col_g1, col_g2 = st.columns([1,1])
    with col_g1:
        st.pyplot(radar_ciz(kategoriler, puanlar))
        
    with col_g2:
        yorum = f"Sayin {ad}, Ahi-AI analizine gore:\\n\\n"
        if genel_ort > 8: yorum += "Tebrikler! Usta seviyesindesin.\\n"
        elif genel_ort > 5: yorum += "Gelisim gostermelisin (Kalfa).\\n"
        else: yorum += "Daha cok calismalisin (Yamak).\\n"
        
        if p5 < 5: yorum += "Teknoloji konusuna egilmelisin.\\n"
        
        st.info(yorum)
        
        dosya = pdf_yap(ad, yorum, radar_ciz(kategoriler, puanlar))
        
        # PDF Okuma ve İndirme Butonu
        with open(dosya, "rb") as f:
            pdf_data = f.read()
            st.download_button(
                label="📥 PDF İndir",
                data=pdf_data,
                file_name=dosya,
                mime="application/pdf"
            )