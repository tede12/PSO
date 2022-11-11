import threading


class MioThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = f"MioThread - {self.name}"
        # ... posso definire ulteriori variabili e metodi

    def run(self):
        try:
            print(f"{self.name} - thread partito!")
            # super().run() # posso invocare il metodo run() della classe padre
            # oppure posso invocare il metodo target() passando gli argomenti
            self._target(*self._args, **self._kwargs)
        except Exception as e:
            print("Exception", e)


if __name__ == '__main__':
    t1 = MioThread(target=print, args=("Ciao",))  # creo un thread che esegue la funzione print
    t1.start()  # avvio il thread
    t1.join()  # aspetto che il thread termini
