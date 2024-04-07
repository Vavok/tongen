from tonsdk.contract.wallet import WalletVersionEnum, Wallets
from tonsdk.utils import bytes_to_b64str
from tonsdk.crypto import mnemonic_new
import threading, time
from multiprocessing import Process, Value
import telebot
import socket

hostname = socket.gethostname()
wton=[]
with open('config.txt', 'r') as file:
    first_line = file.readline()
    token = first_line.replace('TOKEN=', '')
bot = telebot.TeleBot(token)
idv=964464775
bot.send_message(idv,f'{hostname} старт')
with open('wton.txt', 'r') as file:
    for line in file:
        wton.append(line.strip())
def export_mnemonic(file):
    with open(file, 'r') as file:
        first_line = file.readline()
        first_line = first_line.replace('SEED=', '')
    wallet_mnemonics = first_line.split()
    return wallet_mnemonics

start_time=time.time()
test = ['_KG','KILO','KGRAM','kGRAM','KIL0','KILOG','KILOGr','kiloG','kilog','kilogram','KIL']
a=['UQCqPdkvuiXF79L2YdyYJlKAMztkfAnjae4bwgGGVHvQB_Am',
   'EQCiLN0gEiZqthGy-dKl4pi4kqWJWjRzR3Jv4jmPOtQHveDN',
   'EQC10L__G2SeEeM2Lw9osGyYxhoIPqJwE-8Pe7728JcmnJzW',
   'EQCfwe95AJDfKuAoP1fBtu-un1yE7Mov-9BXaFM3lrJZwqg_',
   'UQCtiv7PrMJImWiF2L5oJCgPnzp-VML2CAt5cbn1VsKAxOVB',
   ]

wton=wton+a
test=test
#print(test)
def start(i):
    wallet_workchain = 0
    wallet_version = WalletVersionEnum.v4r2
    while True:
        wallet_mnemonics = mnemonic_new()
        _mnemonics, _pub_k, _priv_k, wallet = Wallets.from_mnemonics(
            wallet_mnemonics, wallet_version, wallet_workchain)
        seeds=''

        address=wallet.address.to_string(True, True, False)

        #print(address,' : ',seeds)
        def proverka(address, a, txt):
            for st in range(len(a)):
                n = len(a[st])
                if address[-n:] == a[st]:
                    print('Совпало')
                    seeds=''
                    for en in range(len(wallet_mnemonics)):
                        seeds+=wallet_mnemonics[en]+str(' ')
                    end = time.time() - start_time
                    speed = i.value / end
                    text=f'{address} : {seeds}  : №{i.value} {speed}h/s \n'
                    text2 = f'{address} : <code>{seeds}</code>  : №{i.value} {speed}h/s \n'
                    with open(txt, "a+", encoding="utf-8") as f:
                        f.write(text)
                    print(i.value, address, seeds, speed, 'h/s')
                    bot.send_message(idv,text2,parse_mode='html')
        proverka(address, test, 'tonb.txt')
        proverka(address, wton, 'ton.txt')
        i.value += 1
        # if i.value % 1000 == 0:
        #     end = time.time() - start_time
        #     speed = i.value / end
        #     print(speed, 'h/s')
        #     print(i.value)


if __name__ == "__main__":
    # создаем несколько процессов
    processes = []
    i = Value('i', 0)
    for n in range(3):
        print(f'Cтарт {n+1}')
        p = Process(target=start, args=(i,))
        processes.append(p)
        p.start()
        time.sleep(1)

    #ждем завершения всех процессов
    for p in processes:
        p.join()
