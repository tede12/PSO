def mia_funzione(string):  # funzione che accetta in input un parametro chiamato string
    a = 1  # dichiarazione e inizializzazione di una variabile locale

    def mia_funzione_interna():  # funzione all’interno di un'altra funzione
        return string + "world" + str(a)  # ritorno della funzione “mia_funzione_interna”

    return mia_funzione_interna()  # ritorno della chiamata della funzione “mia_funzione”


mia_funzione("hello")  # chiamata della funzione “mia_funzione”
