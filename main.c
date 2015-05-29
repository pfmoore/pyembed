#define UNICODE
#define _UNICODE
#include <Python.h>
#include <windows.h>

int
main()
{
    TCHAR program[MAX_PATH];
    LPWSTR *argv;
    int argc;
    PyObject *runpy;
    PyObject *ret;

    argv = CommandLineToArgvW(GetCommandLineW(), &argc);
    GetModuleFileName(NULL, program, MAX_PATH);
    Py_SetProgramName(program);  /* optional but recommended */
    Py_Initialize();
    PySys_SetArgvEx(argc, argv, 0);
    runpy = PyImport_ImportModule("runpy");
    if (!runpy) PyErr_Print();
    ret = PyObject_CallMethod(runpy, "run_path", "u", program);
    if (!ret) PyErr_Print();
    Py_Finalize();
    return 0;
}
