import src.projector

try:
    with open("projector.py") as f:
        exec(f.read())
except Exception as N:
    print("Terminated - " + str(N))
