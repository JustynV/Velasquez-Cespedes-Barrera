import sys

def check():
    input1 = sys.argv[1]
    input2 = sys.argv[2]
    with open(input1, 'rb') as f1, open(input2, 'rb') as f2:
        while True:
            b1 = f1.read()
            b2 = f2.read()
            if b1 != b2:
                return "Not ok"
            if not b1:
                return "Ok"

if __name__ == "__main__":
    
    print(check())
