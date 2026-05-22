import os
import random
import requests
import json
from datetime import datetime
import google.generativeai as genai

GEMINI_API_KEY       = os.environ["GEMINI_API_KEY"]
THREADS_ACCESS_TOKEN = os.environ["THREADS_ACCESS_TOKEN"]
THREADS_USER_ID      = os.environ["THREADS_USER_ID"]

TOPICS = [
    "kenapa gua nolak tawaran kerja luar negeri padahal gajinya jauh lebih gede",
    "realita bangun brand sambil kerja full-time sebagai network engineer",
    "yang gua pelajari dari program affiliate yang ternyata zero konversi",
    "perbedaan mindset karyawan vs founder yang gua rasain sendiri",
    "kenapa gua pilih bangun brand lokal daripada ngejar karir di MNC",
    "cara gua validasi produk sebelum keluar duit banyak untuk produksi",
    "behind the scenes proses maklon parfum di Indonesia",
    "berapa modal minimal buat mulai brand EDP sendiri",
    "kesalahan gua di bulan pertama jualan online yang bikin rugi waktu",
    "kenapa data lebih penting dari feeling kalau mau jualan online",
    "gaji tetap vs bisnis sendiri: mana yang lebih aman buat gua",
    "yang nggak diajarkan waktu kuliah tentang bikin brand",
    "cara gua riset kompetitor tanpa ngeluarin budget sepeserpun",
    "pola pikir yang berubah setelah gua serius terjun ke bisnis",
    "kenapa konsistensi di satu channel lebih penting dari coba-coba semua platform",
]

PROMPT_TEMPLATE = """Kamu adalah ghostwriter untuk seorang founder muda Indonesia bernama Dani.

PROFIL DANI:
- NOC Engineer di perusahaan fintech besar di Jakarta
- Punya sertifikasi CCNA, kerja di bidang jaringan dan data center
- Membangun brand parfum sendiri: L'Aura (room spray & EDP) dan SCNTR (premium unisex EDP)
- Pernah ditawari kerja di luar negeri tapi menolak demi bangun brand lokal
- Introvert, lebih suka bangun dari balik layar daripada tampil di depan

GAYA PENULISAN:
- Casual, natural, seperti orang ngobrol
- Bahasa Indonesia sehari-hari
- WAJIB mulai dengan question hook
- Jujur dan spesifik, hindari motivasi generik
- 3-5 baris, maksimal 280 karakter
- Maksimal 2 hashtag
- Maksimal 2 emoji

Buat 1 post Threads tentang: {topic}

Tulis HANYA teks post-nya saja, langsung tanpa penjelasan."""

def generate_post(topic):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(PROMPT_TEMPLATE.format(topic=topic))
    return response.text.strip()

def create_threads_container(text):
    url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads"
    resp = requests.post(url, params={
        "media_type": "TEXT",
        "text": text,
        "access_token": THREADS_ACCESS_TOKEN
    })
    resp.raise_for_status()
    return resp.json()["id"]

def publish_threads_post(container_id):
    url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads_publish"
    resp = requests.post(url, params={
        "creation_id": container_id,
        "access_token": THREADS_ACCESS_TOKEN
    })
    resp.raise_for_status()
    return resp.json()["id"]

def main():
    topic = random.choice(TOPICS)
    print(f"Topic: {topic}\n")
    post_text = generate_post(topic)
    print(f"Post:\n{post_text}\n")
    container_id = create_threads_container(post_text)
    post_id = publish_threads_post(container_id)
    print(f"✅ Posted! ID: {post_id}")

if __name__ == "__main__":
    main()
