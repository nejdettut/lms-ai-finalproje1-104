import streamlit as st
from fastapi import FastAPI, HTTPException
from ai_service import analyze_text
from database import init_db, save_analysis, get_history
from models import TextRequest
import requests

# --- 1. Veritabanı ve API Başlatma ---
init_db()
app = FastAPI(title="AI Destekli LMS API")

# --- 2. FastAPI Endpoints ---
@app.get("/")
def read_root():
    return {"message": "AI Destekli LMS API'sine Hoş Geldiniz!"}

@app.post("/analyze-text")
def analyze(request: TextRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Analiz edilecek metin boş olamaz.")
    
    response = analyze_text(request.text, request.provider)
    
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    
    save_analysis(
        user_name="API Kullanıcısı",
        text=request.text,
        result=response["analysis"],
        provider=response["source"]
    )
    return response

@app.get("/history")
def get_analysis_history():
    history = get_history()
    return {"history": [dict(row) for row in history]}

# --- 3. Streamlit Arayüzü (Opsiyonel Çalışma İçin) ---
# Eğer bu dosya 'streamlit run' ile çalıştırılırsa bu kısım devreye girer.
try:
    # Streamlit komutları sadece bir streamlit bağlamında çalışır
    st.set_page_config(page_title="AI Destekli LMS", page_icon="🎓", layout="centered")
    
    st.title("🎓 AI Destekli LMS Analiz Paneli")
    st.markdown("""
    Bu sistem, öğrenci geri bildirimlerini **Doğal Dil İşleme (NLP)** kullanarak analiz eder.
    Eğitmenlere ders kalitesini artırmak için yapay zeka tabanlı içgörüler sunar.
    """)

    st.divider()

    # Kullanıcı Girdi Alanları
    feedback_text = st.text_area(
        "📝 Öğrenci Geri Bildirimi",
        placeholder="Örneğin: 'Ders içeriği çok iyiydi ama pratik örnekler biraz az kalmış.'",
        height=150
    )

    col1, col2 = st.columns(2)
    with col1:
        provider = st.selectbox("🤖 AI Sağlayıcı", ["gemini", "groq"], index=0)

    # Analiz Süreci
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
    
    # Geçmiş Analizleri Göster (Streamlit'te ek özellik)
    if st.checkbox("📜 Analiz Geçmişini Göster"):
        history = get_history()
        if history:
            for row in history:
                with st.expander(f"📌 {row['user_name']} - {row['created_at']}"):
                    st.write(f"**Metin:** {row['original_text']}")
                    st.write(f"**Analiz:** {row['ai_result']}")
        else:
            st.write("Henüz kayıt bulunamadı.")

except Exception:
    # Eğer streamlit ile çalışmıyorsa (örn: uvicorn), hataları sessizce geç
    pass