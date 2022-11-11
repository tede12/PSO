import threading
import time
import random

lock = threading.Lock()


def task(count=0):
    if count > 10:  # se le iterazioni sono più di 10 allora termina
        return

    numero_grande = random.randint(1, 10 ** 8)  # genera un numero casuale tra 1 e 10^8
    while numero_grande:  # decrementa il numero casuale fino a che non è 0
        numero_grande -= 1
    tempo_di_attesa = random.randint(1, 3)  # genera un numero casuale tra 1 e 3
    print(f'Il {threading.current_thread().name}. Attendo {tempo_di_attesa} secondi...')
    time.sleep(tempo_di_attesa)  # attende un numero casuale di secondi
    task(count + random.randint(1, 3))  # richiama la funzione con un numero casuale di iterazioni


threads = []
for i in range(3):
    threads.append(threading.Thread(target=task, name=f'Thread-{i + 1}'))

for t in threads:
    t.start()  # avvio i thread
for t in threads:
    t.join()  # aspetto che i thread terminino

# ------------------------------------------------------------
# per tracciare Viztracer
# python -m viztracer main.py
# per la visualizzazione
# vizviewer result.json
