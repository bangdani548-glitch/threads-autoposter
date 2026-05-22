import os
import random
import requests
import json
from datetime import datetime
import google.generativeai as genai

# ── Config dari environment variables ──────────────────────────────────────
GEMINI_API_KEY       = os.environ["GEMINI_API_KEY"]
THREADS_ACCESS_TOKEN = os.environ["THREADS_ACCESS_TOKEN"]
THREADS_USER_ID      = os.environ["THREADS_USER_ID"]

# ── Topics pool ─────────────────────────────────────────────────────────────
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
    "yang nggak diajarkan waktu kuliah atau sekolah tentang bikin brand",
    "cara gua riset kompetitor tanpa ngeluarin budget sepeserpun",
    "pola pikir yang berubah setelah gua serius terjun ke bisnis",
    "kenapa konsistensi di satu channel lebih penting dari coba-coba semua platform",
    "keputusan terberat gua sebagai founder yang kerja 9-5 sekaligus",
    "apa yang bikin brand parfum lokal bisa bersaing sama brand luar",
    "channel mana yang paling efektif buat jualan produk lokal di 2025",
    "jujur soal berapa lama sampai brand gua mulai balik modal",
    "kenapa personal branding founder lebih penting dari iklan produk",
]

# ── Prompt / persona ────────────────────────────────────────────────────────
PROMPT_TEMPLATE = """Kamu adalah ghostwriter untuk seorang founder muda Indonesia bernama Dani.

PROFIL DANI:
- NOC Engineer di perusahaan fintech besar di Jakarta
- Punya sertifikasi CCNA, kerja di bidang jaringan dan data center
- Membangun brand parfum sendiri: L'Aura (room spray & EDP) dan SCNTR (premium unisex EDP)
- Pernah ditawari kerja di luar negeri tapi menolak demi bangun brand lokal
- Introvert, lebih suka bangun dari balik layar daripada tampil di depan
- Orang Jakarta Utara, hidup sederhana tapi punya goals yang jelas

GAYA PENULISAN:
- Casual, natural, seperti orang ngobrol — bukan seperti motivator
- Bahasa Indonesia sehari-hari, boleh mix sedikit English kalau natural
- WAJIB mulai dengan question hook (contoh: "Pernah nggak lo...", "Emang beneran bisa...", "Kalau lo dikasih pilihan...")
- Jujur dan spesifik — hindari kalimat motivasi generik dan kosong
- Panjang: 3–5 baris, maksimal ~280 karakter
- Hashtag: maksimal 2, atau tidak sama sekali
- Emoji: maksimal 1–2, jangan lebay

Buat 1 post Threads tentang topik ini: {topic}

Tulis HANYA teks post-nya saja. Tidak ada penjelasan tambahan, langsung teksnya."""


# ── Functions ────────────────────────────────────────────────────────────────
def generate_post(topic: str) -> str:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(PROMPT_TEMPLATE.format(topic=topic))
    return response.text.strip()


def create_threads_container(text: str) -> str:
    url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads"
    resp = requests.post(url, params={
        "media_type": "TEXT",
        "text": text,
        "access_token": THREADS_ACCESS_TOKEN
    })
    resp.raise_for_status()
    return resp.json()["id"]


def publish_threads_post(container_id: str) -> str:
    url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads_publish"
    resp = requests.post(url, params={
        "creation_id": container_id,
        "access_token": THREADS_ACCESS_TOKEN
    })
    resp.raise_for_status()
    return resp.json()["id"]


def main():
    topic = random.choice(TOPICS)
    print(f"📌 Topic: {topic}\n")

    post_text = generate_post(topic)
    print(f"📝 Generated post:\n{post_text}\n")

    container_id = create_threads_container(post_text)
    post_id = publish_threads_post(container_id)

    log = {
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "post": post_text,
        "post_id": post_id
    }
    print("✅ Posted successfully!")
    print(json.dumps(log, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
