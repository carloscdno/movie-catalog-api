import sys
import os

# Forzar limpieza de módulos cacheados
for module in list(sys.modules.keys()):
    if any(x in module for x in ['main', 'movies', 'database', 'models']):
        del sys.modules[module]

# Verificar imports
print("=== VERIFICANDO IMPORTS ===")
try:
    from main import app
    print("✓ main.py importado correctamente")
    
    # Verificar rutas
    print("\n=== RUTAS REGISTRADAS ===")
    for route in app.routes:
        print(f"{route.path} - {route.methods}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()