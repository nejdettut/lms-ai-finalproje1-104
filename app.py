import streamlit as st
from ai_service import analyze_text
from database import init_db, save_analysis, get_history

# --- 1. Başlatma ---
# Veritabanını başlat (Streamlit her yenilendiğinde çalışır)
init_db()

# --- 2. Sayfa Yapılandırması ---
st.set_page_config(page_title="AI Destekli LMS", page_icon="🎓", layout="centered")

st.title("🎓 AI Destekli LMS Analiz Paneli")
st.markdown("""
Bu sistem, öğrenci geri bildirimlerini **Doğal Dil İşleme (NLP)** kullanarak analiz eder.
Eğitmenlere ders kalitesini artırmak için yapay zeka tabanlı içgörüler sunar.
""")

st.divider()

# --- 3. Kullanıcı Girdi Alanları ---
feedback_text = st.text_area(
    "📝 Öğrenci Geri Bildirimi",
    placeholder="Örneğin: 'Ders içeriği çok iyiydi ama pratik örnekler biraz az kalmış.'",
    height=150
)

col1, col2 = st.columns(2)
with col1:
    provider = st.selectbox("🤖 AI Sağlayıcı", ["gemini", "groq"], index=0)

# --- 4. Analiz Süreci ---
if st.button("Analiz Et", type="primary", use_container_width=True):
    if not feedback_text.strip():
        st.warning("Lütfen analiz etmek için bir metin girin!")
    else:
        with st.spinner(f"{provider.capitalize()} üzerinden analiz yapılıyor..."):
            try:
                # Doğrudan ai_service fonksiyonunu çağırıyoruz
                response = analyze_text(text=feedback_text, provider=provider)

                if "error" in response:
                    st.error(f"AI Servis Hatası: {response['error']}")
                else:
                    st.success("Analiz Tamamlandı!")
                    st.subheader("📊 AI Analiz Sonucu")
                    st.info(response["analysis"])
                    
                    # Veritabanına kaydet
                    save_analysis(
                        user_name="Streamlit Kullanıcısı",
                        text=feedback_text,
                        result=response["analysis"],
                        provider=response["source"]
                    )
                    st.caption(f"Kaynak: {response['source']}")
                    st.toast("Sonuç veritabanına kaydedildi.")

            except Exception as e:
                st.error(f"Sistem Hatası: {e}")

st.divider()

# --- 5. Geçmiş Analizleri Göster ---
if st.checkbox("📜 Analiz Geçmişini Göster"):
    history = get_history()
    if history:
        for row in history:
            # row nesnesinin dict formatında veya attribute formatında olmasına göre düzenle
            label = f"📌 {row['user_name']} - {row['created_at']}"
            with st.expander(label):
                st.write(f"**Metin:** {row['original_text']}")
                st.write(f"**Analiz:** {row['ai_result']}")
    else:
        st.write("Henüz kayıt bulunamadı.")
