from fastapi import FastAPI
from fastapi_socketio import SocketManager
from fastapi.middleware.cors import CORSMiddleware
import time

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

 
sio = SocketManager(app=app)
yukseltme2Sayi = 0  
yukseltme1Sayi = 0  


@app.get("/")
async def main():
    return {"message": "Hello World"}

@app.sio.on('join')
async def handle_join(sid, *args, **kwargs):
    print("Bağlantı gerçekleşti...")
    await sio.emit('lobby', 'User joined')

@sio.on('topla')
async def test(sid,*args, **kwargs):
    # print(args[0])
    sonuc = args[0] + 1
    print(f"{bcolors.WARNING}{bcolors.BOLD}Toplama işlemi gerçekleşti...\nSonuç = {sonuc}")
    print("-"*10)
    await sio.emit('toplam',sonuc)

@sio.on('yukseltme1')
async def test(sid,*args, **kwargs):
    # print(args[0])
    if args[0] <50:
        print(f"{bcolors.FAIL}{bcolors.BOLD}Yükseltme işlemi gerçekleşmedi...\nSonuç = {args[0]}")
        print("-"*10)
    else:
        sonuc = args[0] - 50
        print(f"{bcolors.WARNING}{bcolors.BOLD}Yükseltme işlemi gerçekleşti...\nSonuç = {sonuc}")
        print("-"*10)
        await sio.emit('toplam',sonuc)
        # sonuc her saniye 1 arttırıyoruz
        while 1:
            global yukseltme1Sayi
            if yukseltme1Sayi == 300:
                await sio.emit('yukseltme1',sonuc+yukseltme1Sayi)
                yukseltme1Sayi = 0
                break
            elif yukseltme1Sayi < 300:
                time.sleep(1)
                print(f"{bcolors.WARNING}{bcolors.BOLD}Yükseltme işlemi gerçekleşti...\nSonuç = {yukseltme1Sayi}")
                print("-"*10)
                yukseltme1Sayi += 1
            else:
                break

@sio.on('yukseltme2')
async def test(sid,*args, **kwargs):

    # print(args[0])
    if args[0] <500:
        print(f"{bcolors.FAIL}{bcolors.BOLD}Yükseltme işlemi gerçekleşmedi...\nSonuç = {args[0]}")
        print("-"*10)
    else:
        sonuc = args[0] - 500
        print(f"{bcolors.WARNING}{bcolors.BOLD}Yükseltme işlemi gerçekleşti...\nSonuç = {sonuc}")
        print("-"*10)
        await sio.emit('toplam',sonuc)
        # sonuc her saniye 10 arttırıyoruz
        while 1:
            global yukseltme2Sayi
            if yukseltme2Sayi == 1000:
                await sio.emit('yukseltme2',sonuc+yukseltme2Sayi)
                yukseltme2Sayi = 0
                break
            elif yukseltme2Sayi < 1000:
                time.sleep(1)
                print(f"{bcolors.WARNING}{bcolors.BOLD}Yükseltme işlemi gerçekleşti...\nSonuç = {yukseltme2Sayi}")
                print("-"*10)
                yukseltme2Sayi += 10
            else:
                break


# geri yükleme işlemi
@sio.on('backup')
async def test(sid,*args, **kwargs):
    dosya = open("kayıt.txt")
    sayi = args[0].replace(" TL","")
    # print(dosya.read())
    # print("\ndosyadan okunan ana değer: " + dosya.read())
    dosyaSayi = dosya.read()
    # print("Dosyadan gelen sayı: " + dosyaSayi + "\nhtml den gelen sayı: " + args[0])
    # print(sayi + " < " + dosyaSayi)
    if dosyaSayi == "":
        dosyaSayi = 0
    if int(sayi) < int(dosyaSayi):
        await sio.emit('backup',dosyaSayi)
        print(f"{bcolors.WARNING}{bcolors.BOLD}Backup işlemi gerçekleşti...\nSonuç = {dosyaSayi}")
        print("-"*10)
    elif dosyaSayi == "":
        await sio.emit('backup',"0")
        print(f"{bcolors.WARNING}{bcolors.BOLD}Backup işlemi gerçekleşti...\nSonuç = 0")
        print("-"*10)
    else:
        await sio.emit('backup',args[0])
        print(f"{bcolors.FAIL}{bcolors.BOLD}Backup işlemi gerçekleşmedi...\nSonuç = {args[0]}")
        print("-"*10)

# txt dosyasına kayıt işlemi
@sio.on('kayıt')
async def test(sid,*args, **kwargs):
    open("kayıt.txt","w+")
    if open("kayıt.txt").read():
        deger = args[0].replace(" TL","")
        okunanDeger = open("kayıt.txt","+r")
        okunanDeger = okunanDeger.read()
        if okunanDeger == "":
            dosya = open("kayıt.txt","w+")
            dosya.write(str(deger))
            dosya.close()
            print(f"{bcolors.WARNING}{bcolors.BOLD}Kayıt işlemi gerçekleşti...\nSonuç = {args[0]}")
            print("-"*10)
        elif int(deger) > int(okunanDeger):
            dosya = open("kayıt.txt","w")
            dosya.write(str(deger))
            dosya.close()
            print(f"{bcolors.WARNING}{bcolors.BOLD}Kayıt işlemi gerçekleşti...\nSonuç = {args[0]}")
            print("-"*10)
        else:
            print(f"{bcolors.FAIL}{bcolors.BOLD}Kayıt işlemi gerçekleşmedi...\nSonuç = {args[0]}")
            print("-"*10)
    else:
        open("kayıt.txt","w+")
        deger = args[0].replace(" TL","")
        okunanDeger = open("kayıt.txt","+r")
        okunanDeger = okunanDeger.read()
        if okunanDeger == "":
            dosya = open("kayıt.txt","w+")
            dosya.write(str(deger))
            dosya.close()
            print(f"{bcolors.WARNING}{bcolors.BOLD}Kayıt işlemi gerçekleşti...\nSonuç = {args[0]}")
            print("-"*10)
        elif int(deger) > int(okunanDeger):
            dosya = open("kayıt.txt","w")
            dosya.write(str(deger))
            dosya.close()
            print(f"{bcolors.WARNING}{bcolors.BOLD}Kayıt işlemi gerçekleşti...\nSonuç = {args[0]}")
            print("-"*10)
        else:
            print(f"{bcolors.FAIL}{bcolors.BOLD}Kayıt işlemi gerçekleşmedi...\nSonuç = {args[0]}")
            print("-"*10)






if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG,
                        stream=sys.stdout)
    
    import uvicorn

    uvicorn.run("socket_handlers:app", host='127.0.0.1', port=8081, reload=True)