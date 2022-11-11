import threading


def mia_funzione(param_1, param_2):
    # ...
    pass


t = threading.Thread(target=mia_funzione, args=(1, 2))
t.start()
