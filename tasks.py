from invoke import run, task
import zipfile
import os

@task
def clean(binaries=False):
    files = [
        "main.zip",
        "__main__.py",
        "cython/embedded.exp",
        "cython/embedded.lib",
        "cython/embedded.obj",
        "cython/embedded.c",
    ]
    if binaries:
        files.append("test.exe")
        files.append("main.exe")
        files.append("cython/embedded.exe")
    for f in files:
        try:
            os.unlink(f)
        except OSError:
            pass

@task
def build(cython=False):
    run("gcc -o main.exe main.c -IC:\\Apps\\Python34\\include C:\\Windows\\system32\\python34.dll")
    run("strip -s main.exe")
    if cython:
        os.chdir("cython")
        run("cython --embed embedded.pyx")
        run("cl /Feembedded.exe .\embedded.c /I C:\\Apps\\Python34\\Include C:\\Apps\\Python34\\libs\\python34.lib")

@task
def build_test():
    with open("test.exe", 'wb') as f:
        with open("main.exe", 'rb') as src:
            f.write(src.read())
        with zipfile.ZipFile(f, 'w') as z:
            with open("test.py", 'rb') as t:
                z.writestr("__main__.py", t.read())
