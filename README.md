# 🎓 AI Destekli LMS Analiz Sistemi

Bu proje, eğitim platformları (LMS) için geliştirilmiş, öğrenci geri bildirimlerini yapay zeka ile analiz eden bir sistemdir. Hem bir **FastAPI** backend servisi hem de kullanıcı dostu bir **Streamlit** arayüzü sunar.

## 🚀 Özellikler

- **NLP Analizi:** Öğrenci yorumlarını özetler, duygu durumunu (Pozitif/Negatif/Nötr) belirler ve eğitmenler için aksiyon önerileri sunar.
- **Çift Model Desteği:** 
  - **Google Gemini 3.1 Pro:** Yüksek kaliteli analizler için.
  - **Groq (Llama 3.3 70B):** Ultra hızlı sonuçlar için.
- **Veritabanı Entegrasyonu:** Tüm analizler SQLite veritabanında saklanır ve geçmişe dönük incelenebilir.
- **Modern Arayüz:** Streamlit ile geliştirilmiş şık ve etkileşimli panel.
- **API Erişimi:** FastAPI üzerinden diğer sistemlerle entegrasyon imkanı.

## 🛠️ Teknolojiler

- **Backend:** FastAPI, Python 3.9+
- **Frontend:** Streamlit
- **AI:** Google Generative AI (Gemini), Groq SDK
- **Veritabanı:** SQLite
- **Environment:** python-dotenv, Pydantic

## 📦 Kurulum

1.  **Depoyu Klonlayın:**
    ```bash
    git clone <github-repo-url>
    cd lms-yapayzeka-final-104
    ```

2.  **Sanal Ortam Oluşturun ve Paketleri Yükleyin:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows için: .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **.env Dosyasını Hazırlayın:**
    Ana dizine bir `.env` dosyası oluşturun ve API anahtarlarınızı ekleyin:
    ```env
    GEMINI_API_KEY=your_gemini_key
    GROQ_API_KEY=your_groq_key
    ```

## 💻 Çalıştırma

### Streamlit Arayüzünü Başlatmak:
```bash
streamlit run app.py
```

### FastAPI Servisini Başlatmak:
```bash
uvicorn app:app --reload
```
API dökümantasyonuna `http://127.0.0.1:8000/docs` adresinden ulaşabilirsiniz.

## 🌐 Canlıya Taşıma (Deployment)

### GitHub & Streamlit Cloud
1. Projeyi GitHub'a yükleyin.
2. Streamlit Cloud üzerinden yeni bir uygulama oluşturun.
3. **Kritik:** Streamlit Cloud panelinde `Advanced Settings > Secrets` kısmına API anahtarlarınızı ekleyin:
   ```toml
   GEMINI_API_KEY = "your_key"
   GROQ_API_KEY = "your_key"
   ```

---
**Geliştiren:** Nejdet TUT
**Sürüm:** 1.0.0
