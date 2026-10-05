#!/home/fresh/Projects/POLBAN_academic_console/.venv/bin/python

import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

os.system('cls' if os.name == 'nt' else 'clear')

load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
SUBMIT = os.getenv('SUBMIT')
LEVEL = os.getenv('LEVEL')

url = 'https://akademik.polban.ac.id'
login_payload = {'username': USERNAME, 'password': PASSWORD, 'submit' : SUBMIT}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15"
}

session = requests.Session()

# Log-in website akademik
session.post(f"{url}/laman/login", data=login_payload)

# Navigasi ke halaman Dashboard
# mhs_response = session.get(f"{url}/mhs")

# Navigasi ke halaman absensi
absensi_response = session.get(f"{url}/ajar/absen")
soup = BeautifulSoup(absensi_response.text, 'html.parser')
# Simpan nama
nama = soup.find(class_='hidden-xs')

# Header
# print(soup.h1.text.strip(), "\n")
print("Jadwal Perkuliahan")

# Nama Mahasiswa
print(f"Nama: {nama.get_text()}\n")

# Jadwal hari ini
for cell in soup.thead.next_sibling.next_sibling:
    print(cell.get_text("\t", strip=True))

# Daftar mata kuliah hari ini
subjects = soup.tbody.find_all('tr')
subject_list = []
for subject in subjects:
    sub = subject.get_text("|", strip=True)
    subject_list.append(sub.split('|'))

print(subject_list)

while True:
    choice = input("\n Nomor mata kuliah yang ingin diisi kehadirannya? ")
    if choice == 'q':
        break
    else:
        choice = int(choice)
        attend_payload = {
            'ja': subject_list[choice-1][5], 
            'jb': subject_list[choice-1][6], 
            'mk' : subject_list[choice-1][2], 
            'dsn' : subject_list[choice-1][1].split('-')[0], 
            'tp' : subject_list[choice-1][4] , 
            'kls' : LEVEL
        }
        print(attend_payload)
        session.post(f"{url}/ajar/absen/absensi_awal", data=attend_payload)

# Log-out website akademik
session.get(f"{url}/laman/logout")
