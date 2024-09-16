from fastapi import FastAPI
from fastapi_socketio import SocketManager
from fastapi.middleware.cors import CORSMiddleware
import time

from fastapi.middleware.cors import CORSMiddleware




# terminalin arkaplan renkerlini ayarlayan ANSI kodları
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Gerekirse burayı sınırlandırabilirsin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
sio = SocketManager(app=app)
yukseltme2Sayi = 0  
yukseltme1Sayi = 0  


@app.get("/")
async def main():
    return {"message": "Hello World"}

@app.sio.on('connect')
async def connect(sid, environ):
    print("Client connected:", sid)
    await sio.emit('message', 'Connected', to=sid)


@app.sio.on('join')
async def handle_join(sid, *args, **kwargs):
    print("Bağlantı gerçekleşti...")
    await sio.emit('lobby', 'User joined')

@sio.on('topla')
async def test(sid,*args, **kwargs):
    sonuc = args[0] + 1
    print(f"{bcolors.WARNING}{bcolors.BOLD}Toplama işlemi gerçekleşti...\nSonuç = {sonuc}")
    print("-" * 10)
    await sio.emit('toplam', sonuc)

@sio.on('yukseltme1')
async def yukseltme1(sid, *args, **kwargs):
    if args[0] < 50:
        print(f"{bcolors.FAIL}{bcolors.BOLD}Yükseltme işlemi gerçekleşmedi...\nSonuç = {args[0]}")
        print("-" * 10)
    else:
        sonuc = args[0] - 50
        print(f"{bcolors.WARNING}{bcolors.BOLD}Yükseltme işlemi gerçekleşti...\nSonuç = {sonuc}")
        print("-" * 10)
        await sio.emit('toplam', sonuc)
        
        global yukseltme1Sayi
        while yukseltme1Sayi < 300:
            time.sleep(1)
            yukseltme1Sayi += 1
            print(f"{bcolors.WARNING}{bcolors.BOLD}Yükseltme işlemi: {yukseltme1Sayi}")
            if yukseltme1Sayi == 300:
                await sio.emit('yukseltme1', sonuc + yukseltme1Sayi)
                yukseltme1Sayi = 0
                break

@sio.on('yukseltme2')
async def yukseltme2(sid, *args, **kwargs):
    if args[0] < 500:
        print(f"{bcolors.FAIL}{bcolors.BOLD}Yükseltme işlemi gerçekleşmedi...\nSonuç = {args[0]}")
        print("-" * 10)
    else:
        sonuc = args[0] - 500
        print(f"{bcolors.WARNING}{bcolors.BOLD}Yükseltme işlemi gerçekleşti...\nSonuç = {sonuc}")
        print("-" * 10)
        await sio.emit('toplam', sonuc)
        
        global yukseltme2Sayi
        while yukseltme2Sayi < 1000:
            time.sleep(1)
            yukseltme2Sayi += 10
            print(f"{bcolors.WARNING}{bcolors.BOLD}Yükseltme işlemi: {yukseltme2Sayi}")
            if yukseltme2Sayi == 1000:
                await sio.emit('yukseltme2', sonuc + yukseltme2Sayi)
                yukseltme2Sayi = 0
                break

@sio.on('backup')
async def backup(sid, *args, **kwargs):
    try:
        with open("kayıt.txt", "r") as dosya:
            dosyaSayi = dosya.read() or "0"
        sayi = args[0].replace(" TL", "")
        if int(sayi) < int(dosyaSayi):
            await sio.emit('backup', dosyaSayi)
            print(f"{bcolors.WARNING}{bcolors.BOLD}Backup işlemi gerçekleşti...\nSonuç = {dosyaSayi}")
        else:
            await sio.emit('backup', args[0])
            print(f"{bcolors.FAIL}{bcolors.BOLD}Backup işlemi gerçekleşmedi...\nSonuç = {args[0]}")
        print("-" * 10)
    except FileNotFoundError:
        await sio.emit('backup', "0")
        print(f"{bcolors.WARNING}{bcolors.BOLD}Dosya bulunamadı, backup 0 yapıldı")
        print("-" * 10)

@sio.on('kayıt')
async def kayıt(sid, *args, **kwargs):
    deger = args[0].replace(" TL", "")
    try:
        with open("kayıt.txt", "r+") as dosya:
            okunanDeger = dosya.read() or "0"
            if int(deger) > int(okunanDeger):
                dosya.seek(0)
                dosya.write(str(deger))
                dosya.truncate()
                print(f"{bcolors.WARNING}{bcolors.BOLD}Kayıt işlemi gerçekleşti...\nSonuç = {deger}")
            else:
                print(f"{bcolors.FAIL}{bcolors.BOLD}Kayıt işlemi gerçekleşmedi...\nSonuç = {deger}")
        print("-" * 10)
    except FileNotFoundError:
        with open("kayıt.txt", "w") as dosya:
            dosya.write(deger)
        print(f"{bcolors.WARNING}{bcolors.BOLD}Yeni dosya oluşturuldu ve kayıt gerçekleşti...\nSonuç = {deger}")
        print("-" * 10)

if __name__ == '__main__':
    import logging
    import sys
    import uvicorn

    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    
    uvicorn.run("main:app", host='127.0.0.1', port=8081, reload=True)
