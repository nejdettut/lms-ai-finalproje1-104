import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

try:
    from groq import Groq
except ImportError:
    Groq = None


# .env dosyasını oku (Mutlak yol ve override kullanarak daha güvenli hale getiriyoruz)
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

def get_api_key(key_name):
    # 1. Önce ortam değişkenlerine bak (Yerel çalışma için .env)
    api_key = os.getenv(key_name)

    # 2. Eğer yoksa Streamlit Secrets'a bak (Bulut ortamı için)
    if not api_key:
        try:
            # st.secrets'a erişirken hata oluşma ihtimaline karşı try-except
            if key_name in st.secrets:
                api_key = st.secrets[key_name]
        except Exception:
            # Secrets henüz yüklenmemişse veya erişilemiyorsa sessizce geç
            pass

    return api_key


# --- Mühendislik Kuralı: System Prompt ---
SYSTEM_PROMPT = """
Sen bir eğitim platformunda çalışan profesyonel bir yapay zeka asistanısın.
Görevin, öğrenci geri bildirimlerini derinlemesine analiz etmek.
Lütfen yanıtını şu yapıda ver:
1. Kısa Özet: (Metnin ana fikri)
2. Duygu Durumu: (Pozitif, Negatif veya Nötr)
3. Eğitmen İçin Öneri: (Eğitim kalitesini artıracak aksiyon adımı)
"""

def analyze_text(text, provider="gemini"):
    """
    Ana servis fonksiyonu. İstediğin sağlayıcıyı (Gemini veya Groq) seçebilirsin.
    """
    if not text:
        return {"error": "Analiz edilecek metin boş olamaz."}

    if provider == "gemini":
        return _analyze_with_gemini(text)
    elif provider == "groq":
        return _analyze_with_groq(text)
    else:
        return {"error": "Geçersiz sağlayıcı seçimi."}

# --- Google Gemini Motoru ---
def _analyze_with_gemini(text):
    api_key = get_api_key("GEMINI_API_KEY")
    if not api_key:
        return {"error": "Gemini API Key bulunamadı!", "api_configured": False}

    try:
        genai.configure(api_key=api_key)
        
        # 2026 Güncel Model Listesi ve Hata Giderme Stratejisi
        # Sistem sırasıyla bu modelleri deneyecek:
        available_models = [
            'gemini-1.5-flash',   # 1. Tercih (Hızlı ve Stabil)
            'gemini-2.0-flash',   # 2. Tercih (En Yeni Nesil)
            'gemini-1.5-pro',     # 3. Tercih (Yüksek Zeka)
            'gemini-pro'          # 4. Tercih (Legacy/Eski fallback)
        ]
        
        model = None
        last_error = ""

        # Modelleri sırayla deniyoruz
        for model_name in available_models:
            try:
                model = genai.GenerativeModel(model_name)
                # Test amaçlı küçük bir deneme değil, direkt içeriği üretmeyi deniyoruz
                full_prompt = f"{SYSTEM_PROMPT}\n\nAnaliz edilecek öğrenci metni: {text}"
                response = model.generate_content(full_prompt)
                
                # Eğer buraya kadar geldiyse model çalışmıştır
                return {
                    "source": f"Google Gemini ({model_name})",
                    "analysis": response.text,
                    "api_configured": True
                }
            except Exception as e:
                last_error = str(e)
                continue # Hata verirse bir sonraki modeli dene
        
        # Hiçbir model çalışmazsa son hatayı dön
        return {"error": f"Tüm Gemini modelleri denendi ancak başarısız oldu. Son Hata: {last_error}", "api_configured": False}

    except Exception as e:
        return {"error": f"Genel Gemini Hatası: {str(e)}", "api_configured": False}
# --- Groq Cloud Motoru ---
def _analyze_with_groq(text):
    if Groq is None:
        return {"error": "Groq paketi yüklü değil.", "api_configured": False}

    api_key = get_api_key("GROQ_API_KEY")
    if not api_key:
        return {"error": "Groq API Key bulunamadı!", "api_configured": False}

    try:
        client = Groq(api_key=api_key)
        full_prompt = f"{SYSTEM_PROMPT}\n\nAnaliz edilecek öğrenci metni: {text}"

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": full_prompt}]
        )
        return {
            "source": "Groq (Llama 3)",
            "analysis": completion.choices[0].message.content,
            "api_configured": True
        }
    except Exception as e:
        return {"error": f"Groq Hatası: {str(e)}", "api_configured": False}
