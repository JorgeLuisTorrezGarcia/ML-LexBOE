from app.main import app

paths = [r.path for r in app.routes]
print("import ok")
print("num rutas:", len(paths))
print("mounts:", [p for p in paths if p == "/"])
