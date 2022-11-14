import random
import string

import numpy as np
import requests

from libreria.utils import visualizza_grafico, visualizza_grafico_combinato, esegui_thread_processi, info_file, \
    tempo_di_esecuzione, format_bytes


# IO BOUND - SOCKET
@tempo_di_esecuzione  # decoratore che permette di salvare il tempo di esecuzione della funzione
def download(url):
    try:
        resp = requests.get(url)  # richiesta e download dei dati della risorsa esterna
    except requests.exceptions.RequestException as errore:
        print('Errore HTTP: ', errore)


def io_bound_socket():
    # url = 'https://freetestdata.com/wp-content/uploads/2021/09/Free_Test_Data_1MB_PDF.pdf'  # 1 MB
    # url = 'https://freetestdata.com/wp-content/uploads/2021/09/500kb.png'  # 500 KB
    url = 'https://freetestdata.com/wp-content/uploads/2021/09/Free_Test_Data_100KB_PDF.pdf'  # 100 KB
    info_file(url)

    num_urls = 16  # numero di url da scaricare
    urls = [url for i in range(num_urls)]  # creo una lista di url da scaricare
    esegui_thread_processi(download, urls, grafico_combinato=True, lista_thread_processi=[1, 2, 4, 8])


# ----------------------------


# CPU BOUND - SCRITTURA SU FILE


@tempo_di_esecuzione
def scrittura_su_file(testo):
    try:
        with open('reports/test.txt', 'wt', encoding='utf-8') as f:  # apro il file in scrittura
            f.write(testo)
    except IOError as errore:
        print('Errore I/O: ', errore)


def io_bound_pesante():
    num_test = 16  # numero di test da eseguire
    testo = ''.join(random.choice(string.ascii_lowercase) for i in range(10 ** 8))
    print("Dimensioni del testo: ", format_bytes(len(testo)))
    test = [testo for i in range(num_test)]  # creo una lista di test da eseguire
    esegui_thread_processi(scrittura_su_file, test, grafico_combinato=True, lista_thread_processi=[1, 2, 4, 8])


# ----------------------------


# CPU BOUND - CALCOLO PESANTE

@tempo_di_esecuzione
def aggiungi_a_lista(num):
    lista = []
    for n in range(num):
        lista.append(random.random())


def cpu_bound_pesante():
    num_test = 16  # numero di test da eseguire
    test = [10 ** 7 for i in range(num_test)]  # creo una lista di test da eseguire
    esegui_thread_processi(aggiungi_a_lista, test, grafico_combinato=True, lista_thread_processi=[1, 2, 4, 8])


# ----------------------------

# CPU BOUND - FUNZIONI NUMPY

@tempo_di_esecuzione
def addizione(array):
    res = array[0] + array[1]


def gil_unbound():
    dimensione = 4000
    num_test = 16  # numero di test da eseguire
    dimensione_array = [dimensione for i in range(num_test)]
    a = np.random.rand(dimensione, dimensione)
    b = np.random.rand(dimensione, dimensione)
    test = [(a, b) for i in range(num_test)]  # creo una lista di test da eseguire
    esegui_thread_processi(addizione, test, grafico_combinato=True, lista_thread_processi=[1, 2, 4, 8])


# ----------------------------

