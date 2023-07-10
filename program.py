try:
    with open("src/projector.py") as f:
        exec(f.read())
except Exception as N:
    print("Terminated - " + str(N))
