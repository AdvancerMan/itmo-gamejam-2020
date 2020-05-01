def log(message: str):
    with open("log.txt", 'a') as f:
        f.write("\n")
        f.write(message)
    print(message)
