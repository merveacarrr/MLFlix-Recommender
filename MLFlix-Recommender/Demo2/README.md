# MLFlix Film Öneri Sistemi API

Bu proje, kullanıcıların film değerlendirmelerine dayalı olarak kişiselleştirilmiş film önerileri sunan bir REST API'dir. FastAPI framework'ü kullanılarak geliştirilmiştir.

## 🚀 Özellikler

- Kullanıcı kaydı ve kimlik doğrulama
- Film değerlendirme sistemi
- Kişiselleştirilmiş film önerileri
- Kullanıcı istatistikleri
- JWT tabanlı güvenlik
- SQLite veritabanı desteği
- Swagger UI dokümantasyonu

## 📋 Gereksinimler

- Python 3.8+
- FastAPI
- SQLAlchemy
- Pydantic
- Python-jose
- Passlib
- Uvicorn

## 🔧 Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/merveacarrr/MLFlix-Recommender.git
cd MLFlix-Recommender
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. Veritabanını oluşturun:
```bash
python create_db.py
```

5. Örnek verileri ekleyin:
```bash
python data/generate_sample_data.py
```

6. API'yi başlatın:
```bash
uvicorn main:app --reload
```

## 📚 API Dokümantasyonu

API'yi test etmek için:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Temel Endpoint'ler

#### Kullanıcı İşlemleri
- `POST /api/v1/users/` - Yeni kullanıcı oluşturma
- `POST /api/v1/users/token` - Kullanıcı girişi ve token alma
- `GET /api/v1/users/` - Tüm kullanıcıları listeleme
- `GET /api/v1/users/{user_id}` - Belirli bir kullanıcıyı görüntüleme
- `PUT /api/v1/users/{user_id}` - Kullanıcı bilgilerini güncelleme
- `DELETE /api/v1/users/{user_id}` - Kullanıcı silme

#### Film Önerileri
- `GET /api/v1/users/{user_id}/recommendations` - Kullanıcı için film önerileri
- `GET /api/v1/users/{user_id}/stats` - Kullanıcı istatistikleri

## 🎯 Kullanım Örneği

1. Yeni kullanıcı oluşturma:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "test123"}'
```

2. Giriş yapma ve token alma:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/users/token" \
     -d "username=test@example.com&password=test123"
```

3. Film önerilerini görüntüleme:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/users/1/recommendations" \
     -H "Authorization: Bearer your-token-here"
```

## 📊 Veri Yapısı

### Filmler
- ID
- Başlık
- Yayın Yılı
- Tür
- Yönetmen
- Açıklama
- Ortalama Puan

### Kullanıcılar
- ID
- Kullanıcı Adı
- E-posta
- Şifre (hash'lenmiş)
- Oluşturulma Tarihi

### Değerlendirmeler
- ID
- Kullanıcı ID
- Film ID
- Puan
- Oluşturulma Tarihi

## 🔒 Güvenlik

- JWT tabanlı kimlik doğrulama
- Şifre hash'leme (bcrypt)
- Token süresi: 30 dakika
- CORS desteği

## 🤝 Katkıda Bulunma

1. Fork'layın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

Proje Sahibi - [@merveacarrr](https://github.com/merveacarrr)

Proje Linki: [https://github.com/merveacarrr/MLFlix-Recommender](https://github.com/merveacarrr/MLFlix-Recommender)
