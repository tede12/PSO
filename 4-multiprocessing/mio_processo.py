import multiprocessing
import time


class MioProcesso(multiprocessing.Process):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = f"MioProcesso - {self.name}"
        # ... posso definire ulteriori variabili e metodi

    def run(self):
        try:
            print(f"{self.name} - Processo partito!")
            # super().run() # posso invocare il metodo run() della classe padre
            self._target(*self._args, **self._kwargs)  # oppure posso invocare il metodo target() passando gli argomenti
        except Exception as e:
            print("Exception", e)


if __name__ == '__main__':
    p1 = MioProcesso(target=time.sleep, args=(120,))  # creo un processo che esegue la funzione sleep
    p1.start()  # avvio il processo
    time.sleep(5)  # aspetto 5 secondi
    p1.terminate()  # termino il processo
