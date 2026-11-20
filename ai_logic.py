import ollama


def analyze_with_ai(
    computer_name,
    system_name,
    processor,
    cpu_usage,
    ram_usage,
    ram_total,
    ram_available,
    disk_percent,
    disk_total,
    disk_used,
):
  prompt = f"""
Kamu adalah teknisi komputer yang sangat profesional.

Analisis kondisi PC berikut:

Computer Name: {computer_name}
Operating System: {system_name}
CPU: {processor}

CPU Usage: {cpu_usage:.1f}%
RAM Usage: {ram_usage:.1f}%
RAM Total: {ram_total:.2f} GB
RAM Available: {ram_available:.2f} GB

Disk Usage: {disk_percent:.1f}%
Disk Total: {disk_total:.2f} GB
Disk Used: {disk_used:.2f} GB
Disk Free: {(disk_total - disk_used):.2f} GB

Berikan analisis dalam bahasa Indonesia.

Jelaskan:

1. Kondisi komputer saat ini.
2. Komponen yang memiliki penggunaan tinggi.
3. Kemungkinan penyebab jika terdapat masalah.
4. Saran perbaikan atau optimasi.
5. Saran upgrade komponen.
6. Kesimpulan singkat.

Gunakan bahasa yang mudah dipahami, jelas, detail, dan berikan tabel penggunaan hardware.
"""

  try:
    response = ollama.chat(
        model="qwen2.5:1.5b", messages=[{"role": "user", "content": prompt}]
    )
    result = response["message"]["content"]
    return result, None
  except Exception as e:
    return None, str(e)