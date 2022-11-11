struct PyCodeObject {
    PyObject_HEAD
    int co_argcount;            /* #argomenti, eccetto *args */
    int co_posonlyargcount;     /* solo #argomenti posizionali */
    int co_kwonlyargcount;      /* solo #argomenti per chiave */
    int co_nlocals;             /* #variabili locali */
    int co_stacksize;           /* #voci necessarie per l'evaluation stack */
    int co_flags;               /* CO_..., e relative flag sotto */
    int co_firstlineno;         /* numero della prima riga di origine */
    PyObject *co_code;          /* codici operativi delle istruzioni (opcodes) */
    PyObject *co_consts;        /* elenco delle costanti utilizzate */
    PyObject *co_names;         /* elenco di stringhe (nomi utilizzati) */
    PyObject *co_varnames;      /* tupla di stringhe (nomi di variabili locali) */
    PyObject *co_freevars;      /* tupla di stringhe (nomi di variabili liberi) */
    PyObject *co_cellvars;      /* tupla di stringhe (nomi delle variabili cella) */

    Py_ssize_t *co_cell2arg;    /* Mappa le variabili di cella che sono argomenti. */
    PyObject *co_filename;      /* unicode del file (da dove è stato caricato) */
    PyObject *co_name;          /* unicode (nome, per riferimento) */
    /* ... altri membri ... */
};
