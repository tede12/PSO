struct _frame {
    PyObject_VAR_HEAD
    struct _frame *f_back;                 /* frame precedente o NULL */
    PyCodeObject *f_code;                  /* segmento di codice */
    PyObject *f_builtins;                  /* tabella dei simboli built-in (PyDictObject) */
    PyObject *f_globals;                   /* tabella dei simboli globale (PyDictObject) */
    PyObject *f_locals;                    /* tabella dei simboli locali (qualsiasi mappatura)*/
    PyObject **f_valuestack;               /* puntatore all'ultimo valore locale */

    PyObject **f_stacktop;                 /* Prossimo slot libero in f_valuestack */
    PyObject *f_trace;                     /* Funzione di traccia */
    char f_trace_lines;                    /* Eventi di traccia per riga */
    char f_trace_opcodes;                  /* Eventi di traccia per codice operativo */

    /* Riferimento preso in prestito a un generatore o NULL */
    PyObject *f_gen;

    int f_lasti;                           /* Ultima istruzione se chiamata */
    /* ... altri membri ... */
    int f_lineno;                          /* Numero di riga corrente */
    int f_iblock;                          /* Indice in f_blockstack */
    char f_executing;                      /* Indica se il frame è ancora in esecuzione */
    PyTryBlock f_blockstack[CO_MAXBLOCKS]; /* Per blocchi try e loop */
    PyObject *f_localsplus[1];             /* locals+stack, per le dimensioni dinamiche */
};
