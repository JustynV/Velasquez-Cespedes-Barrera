import pickle
import time

class Tree:
    def __init__(self):
        self.heap = {}
        self.reverseMapping = {}

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

def removePadding(text):
    padded_info = text[:8]
    extra_padding = int(padded_info, 2)
    padded_encoded_text = text[8:] 
    encodedText = padded_encoded_text[:-1*extra_padding]
    return encodedText

def decodeText(tree, encoded_text):
	current_code = ""
	decoded_text = ""

	for bit in encoded_text:
		current_code += bit
		if(current_code in tree.reverseMapping):
			character = tree.reverseMapping[current_code]
			decoded_text += character
			current_code = ""

	return decoded_text


def decompress():

    output_path = "descomprimido-elmejorprofesor.txt"
    with open("comprimido.elmejorprofesor", 'rb') as file, open("clave.elmejorprofesor", "rb") as key, open(output_path, 'w',encoding="ISO-8859-1") as output:
        start = time.time()
        bit_string = ''.join([bin(byte)[2:].rjust(8, '0') for byte in file.read()])
        encoded_text = removePadding(bit_string)
        tree = pickle.load(key)
        decompressed_text = decodeText(tree,encoded_text)
        output.write(decompressed_text)
        end = time.time()
        tminus = end-start
        print("Tiempo tardado: ", tminus, " segundos")
        

if __name__ == "__main__":
    decompress()