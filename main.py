# main.py - shim para Railway: ejecuta run_backend.py como script
import runpy

if __name__ == "__main__":
    # Ejecuta run_backend.py como si lo ejecutarás con `python run_backend.py`
    runpy.run_path("run_backend.py", run_name="__main__")