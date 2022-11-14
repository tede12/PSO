import math
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def is_notebook():
    try:
        shell = get_ipython().__class__.__name__  # noqa
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook o qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminale che esegue IPython
        else:
            return False  # Altro tipo (?)
    except NameError:
        return False  # Probabilmente l'interprete standard di Python


# Jupyter ha un problema con il multiprocessing, causato dalla serializzazione dei dati
# per risolvere il problema si può usare il modulo multiprocess che usa il modulo dill anziché pickle per serializzare
# https://stackoverflow.com/questions/41385708/multiprocessing-example-giving-attributeerror
# if is_notebook():
#     import multiprocess as multiprocessing
#     from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
# else:
#     import multiprocessing

import multiprocessing

import numpy as np
from functools import wraps
import time

import requests
import os

os.makedirs('reports', exist_ok=True)  # crea la cartella per i report se non esiste


def rimuovi_caratteri_speciali(text):
    return text.replace(' ', '_').replace('/', '_')


def format_bytes(bytes_):
    """
    Get human-readable version of given bytes.
    Ripped from https://github.com/rg3/youtube-dl
    """
    if bytes_ is None:
        return 'N/A'
    if type(bytes_) is str:
        bytes_ = float(bytes_)
    if bytes_ == 0.0:
        exponent = 0
    else:
        exponent = int(math.log(bytes_, 1024.0))
    suffix = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'][exponent]
    converted = float(bytes_) / float(1024 ** exponent)
    return '{0:.2f}{1}'.format(converted, suffix)


def info_file(url):
    @tempo_di_esecuzione
    def dimensioni_del_file():
        resp = requests.get(url)
        print(resp)
        # calcola le dimensioni del file in MB
        print("Le dimensioni del file sono: ", format_bytes(len(resp.content)))

    res = dimensioni_del_file()
    print(f"Eseguito in {(res[1] - res[0]):.4f} secondi")


def tempo_di_esecuzione(func):
    """
    Decoratore che misura il tempo di esecuzione di una funzione
    :param func:  funzione da eseguire
    :return:  funzione decorata
    """

    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # print(f'Funzione {func.__name__}{args} {kwargs} eseguita in {total_time:.4f} seconds')
        return start_time, end_time  # ritorno i tempi di inizio e fine
        # return result  # ritornerà il risultato della funzione

    return timeit_wrapper


def visualizza_grafico(risultati, titolo, salva_grafico=False):
    """
    Visualizza un grafico a barre con i risultati
    :param salva_grafico:  se True salva il grafico su file
    :param risultati:  lista di tuple temporali (tempo di inizio, tempo di fine)
    :param titolo:  titolo del grafico
    :return:  tempo di esecuzione totale
    """
    import matplotlib.pyplot as plt
    if 'thread' in titolo.lower():
        color = 'C0'
    else:
        color = 'C1'
    inizio, fine = np.array(risultati).T  # creo due array, uno con i tempi di inizio e uno con i tempi di fine
    plt.barh(y=range(1, len(inizio) + 1), width=fine - inizio, left=fine, color=color,
             alpha=.7)  # creo un grafico a barre orizzontali
    plt.grid(axis='x')  # aggiungo una griglia orizzontale
    plt.ylabel("Task")  # imposto l'etichetta dell'asse y
    plt.xlabel("Tempo (s)")  # imposto l'etichetta dell'asse x
    plt.title(titolo)  # imposto il titolo del grafico

    if salva_grafico is True:
        fig1 = plt.gcf()
        file_name = f'reports/{rimuovi_caratteri_speciali(titolo)}.png'
        fig1.savefig(file_name, format='png')
        print('file saved', file_name)

    plt.show()  # visualizzo il grafico

    plt.clf()
    plt.cla()
    plt.close()

    return fine[-1] - inizio[0]  # ritorno il tempo totale di esecuzione


def visualizza_grafico_combinato(risultati2, titolo, salva_grafico=False):
    """
    Visualizza un grafico a barre con i risultati
    :param salva_grafico:  se True salva il grafico su file
    :param risultati2:  lista che continene liste di tuple temporali (tempo di inizio, tempo di fine)
    :param titolo:  titolo del grafico
    :return:  tempo di esecuzione totale
    """
    import matplotlib.pyplot as plt

    plt.grid(axis='x')  # aggiungo una griglia orizzontale
    plt.ylabel("Task")  # imposto l'etichetta dell'asse y
    plt.xlabel("Tempo (s)")  # imposto l'etichetta dell'asse x
    plt.title(titolo)  # imposto il titolo del grafico

    ret_res = []
    labels = ['Thread', 'Processi']  # etichette per la legenda
    max_width = 0
    for num, risultati in enumerate(risultati2):
        inizio, fine = np.array(risultati).T  # creo due array, uno con i tempi di inizio e uno con i tempi di fine
        plt.barh(y=range(1, len(inizio) + 1), width=fine - inizio, left=fine,
                 label=labels[num], alpha=.7)  # creo un grafico a barre orizzontali, alpha è la trasparenza

        ret_res.append(fine[-1] - inizio[0])
        max_width = max(inizio.max(), fine.max(), max_width)

    plt.legend()  # aggiungo una legenda con le etichette dei grafici

    if salva_grafico is True:
        fig1 = plt.gcf()
        file_name = f'reports/{rimuovi_caratteri_speciali(titolo)}.png'
        fig1.savefig(file_name, format='png')
        print('file saved', file_name)

    plt.show()  # visualizzo il grafico

    plt.clf()
    plt.cla()
    plt.close()

    return ret_res  # ritorno il tempo totale di esecuzione


def esegui_thread(funzione, args, num_thread):
    """
    Esegue una funzione su un numero di thread specificato
    :param funzione:  funzione da eseguire
    :param args:  lista di argomenti da passare alla funzione
    :param num_thread:  numero di thread da utilizzare
    :return:  lista dei risultati
    """
    with ThreadPoolExecutor(max_workers=num_thread) as executor:
        return list(
            executor.map(funzione, args)
        )


def esegui_processi2(funzione, args, num_processi):
    """
    Esegue una funzione su un numero di processi specificato
    :param funzione:  funzione da eseguire
    :param args:  lista di argomenti da passare alla funzione
    :param num_processi:  numero di processi da utilizzare
    :return:  lista dei risultati
    """
    with ProcessPoolExecutor(max_workers=num_processi) as executor:
        return list(executor.map(funzione, args))


def esegui_processi(funzione, args, num_processi):
    """
    Esegue una funzione su un numero di processi specificato
    :param funzione:  funzione da eseguire
    :param args:  lista di argomenti da passare alla funzione
    :param num_processi:  numero di processi da utilizzare
    :return:  lista dei risultati
    """

    with ProcessPoolExecutor(max_workers=num_processi) as executor:
        return list(
            executor.map(funzione, args)
        )


# altro metodo per eseguire processi
def esegui_processi_version_2(funzione, args, num_processi):
    with multiprocessing.Pool(num_processi) as pool:
        return list(
            pool.map(funzione, args)
        )


def esegui_thread_processi(funzione, args, grafico_combinato=False, lista_thread_processi=None):
    if lista_thread_processi is None:
        lista_thread_processi = [1, 2, 4, 8]

    for num in lista_thread_processi:
        nome_processo = 'processi' if num > 1 else 'processo'

        if grafico_combinato is True:
            visualizza_grafico_combinato([
                esegui_thread(funzione, args, num),
                esegui_processi(funzione, args, num)
            ], f'{num} thread/{nome_processo}', salva_grafico=True)
        else:

            visualizza_grafico(esegui_thread(funzione, args, num), f'{num} thread', salva_grafico=True)
            visualizza_grafico(esegui_processi(funzione, args, num), f'{num} {nome_processo}', salva_grafico=True)

        # ----------------------------
        # lista_thread = esegui_thread(funzione, args, 4)
        # lista_processi = esegui_processi(funzione, args, 4)
        #
        # visualizza_grafico(lista_thread, "4 thread")
        # visualizza_grafico(lista_processi, "4 processi")

        # visualizza_grafico_combinato([
        #     lista_thread,
        #     lista_processi,
        # ], "4 thread/processi", salva_grafico=False)
