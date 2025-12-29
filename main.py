try:
    from fastapi import FastAPI
except Exception:
    # Permite que el archivo exista sin FastAPI instalado
    app = None