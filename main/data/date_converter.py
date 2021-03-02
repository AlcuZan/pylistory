from datetime import datetime

def convert():
    y = 2021
    m = 2
    d = 27
    print(datetime(y, m, d).strftime("%Y-%m-%d"))

if __name__ == "__main__":
    convert()
