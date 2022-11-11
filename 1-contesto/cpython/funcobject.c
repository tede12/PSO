typedef struct {
    PyObject_HEAD
    PyObject *func_code;        /* Un object code, l'attributo __code__ */
    PyObject *func_globals;     /* Un dizionario delle funzioni globali (altre mappature non funzioneranno) */
    PyObject *func_defaults;    /* NULL o una tupla */
    PyObject *func_kwdefaults;  /* NULL o un dizionario */
    PyObject *func_closure;     /* NULL o una tupla di oggetti cella */
    PyObject *func_doc;         /* L'attributo __doc__ relativo alla docstring */
    PyObject *func_name;        /* L'attributo __name__, un oggetto stringa */
    PyObject *func_dict;        /* L'attributo __dict__, un dict o NULL */
    PyObject *func_weakreflist; /* Elenco dei riferimenti deboli */
    PyObject *func_module;      /* Riferimento all'attributo __module__ */
    PyObject *func_annotations; /* Annotazioni, dict o NULL */
    PyObject *func_qualname;    /* Il nome completo della funzione */
    vectorcallfunc vectorcall;
} PyFunctionObject;

