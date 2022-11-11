import threading
from threading import RLock, Event
import _thread

_start_new_thread = _thread.start_new_thread
_active_limbo_lock = RLock()
_active = {}
_limbo = {}


class Thread(threading.Thread):

    def start(self):
        """Start the thread’s activity.

        It must be called at most once per thread object. It arranges for the
        object’s run() method to be invoked in a separate thread of control.

        This method will raise a RuntimeError if called more than once on the
        same thread object.

        """
        if not self._initialized:  # controllo se è già stata inizializzata l’istanza
            raise RuntimeError("thread.__init__() not called")

        if self._started.is_set():  # cotrollo se il thread è già stato precedentemente avviato
            raise RuntimeError("threads can only be started once")

        with _active_limbo_lock:  # controllo su un re-entrant lock
            _limbo[self] = self
        try:
            _start_new_thread(self._bootstrap, ())  # equivalente al metodo run()
        except Exception:
            with _active_limbo_lock:
                del _limbo[self]
            raise
        self._started.wait()

    def run(self):
        """Method representing the thread’s activity.

        You may override this method in a subclass. The standard run() method
        invokes the callable object passed to the object’s constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.

        """
        try:
            if self._target:  # controllo dell’esistenza della funzione da eseguire nel thread
                self._target(*self._args, **self._kwargs)  # esecuzione della funzione
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs


class Timer(Thread):
    """Call a function after a specified number of seconds:

            t = Timer(30.0, f, args=None, kwargs=None)
            t.start()
            t.cancel()     # stop the timer’s action if it’s still waiting

    """

    def __init__(self, interval, function, args=None, kwargs=None):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.finished = Event()

    def cancel(self):
        """Stop the timer if it hasn’t finished yet."""
        self.finished.set()

    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()
