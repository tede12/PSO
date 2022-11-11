PyObject*
_PyEval_EvalFrameDefault(PyThreadState *tstate, PyFrameObject *f, int throwflag)
{
    // ... dichiazione di variabili locali
    // Ciclo di valutazione (loop infinito)
    for (;;) {

        // `eval_breaker` ci informa quando dobbiamo sospendere l’esecuzione del bytecode
        // es. un thread chiede i permessi di GIL
        if (_Py_atomic_load_relaxed(eval_breaker)) {

            // `eval_frame_handle_pending()` funzione che sospende l’esecuzione del bytecode
            // in particolare rilascia il GIL e attende che venga fatta richiesta di
            // ottenere i permessi di GIL (da un altro thread)
            if (eval_frame_handle_pending(tstate) != 0) {
                goto error;
            }
        }

        // prossima istruzione bytecode
        NEXTOPARG();

        switch (opcode) {
            case TARGET(NOP) {
                FAST_DISPATCH(); // prossima iterazione
            }

            case TARGET(LOAD_FAST) {
                // ... codice per caricare la variabili locali
                FAST_DISPATCH(); // prossima iterazione
            }

            // ... 117 ulteriori casi relativi a ogni possibile bytecode
        }

        // ... gestione degli errori
    }

    // ... terminazione
}
