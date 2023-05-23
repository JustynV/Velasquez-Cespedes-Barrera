import heapq
import pickle
import time
import os
import sys

class Tree:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverseMapping = {}

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq
        
    def __eq__(self, other):
        if(other == None):
            return False
        if(not isinstance(other, Node)):
            return False
        return self.freq == other.freq

def getCodesHelper(tree, root, current_code):

    if (root.char != None):
        tree.codes[root.char] = current_code
        tree.reverseMapping[current_code] = root.char
        return

    getCodesHelper(tree, root.left, current_code + "0")
    getCodesHelper(tree, root.right, current_code + "1")

def getCodes(tree):
    root = heapq.heappop(tree.heap)
    current_code = ""
    getCodesHelper(tree, root, current_code)

def makeFreq(text):
    frequency = {char: text.count(char) for char in set(text)}
    return frequency

def joinNodes(self):
    while(len(self.heap)>1):
        node1 = heapq.heappop(self.heap)
        node2 = heapq.heappop(self.heap)
        newnode = Node(None, node1.freq + node2.freq)
        newnode.left = node1
        newnode.right = node2
        heapq.heappush(self.heap, newnode)

def make_heap(tree, frequency):
    nodes = [Node(key, frequency[key]) for key in frequency]
    [heapq.heappush(tree.heap, node) for node in nodes]
    tree.root = tree.heap[len(tree.heap)-1]

def getEncodeText(tree, text):
    encoded_text = ""
    encoded_text += ''.join([tree.codes.get(char, '') for char in text])
    return encoded_text

def getByteArray(text):
    bytes_list = [int(text[i:i+8], 2) for i in range(0, len(text), 8)]
    return bytearray(bytes_list)

def pad_encoded_text(encoded_text):
	extra_padding = 8 - len(encoded_text) % 8
	for i in range(extra_padding):
		encoded_text += "0"
	padded_info = "{0:08b}".format(extra_padding)
	encoded_text = padded_info + encoded_text
	return encoded_text

def compress():
    output_path = "comprimido.elmejorprofesor"
    path = sys.argv[1]

    with open(path, 'r+') as file, open("clave.elmejorprofesor", "wb") as key,open(output_path, 'wb') as output:
        start = time.time()
        text = file.read()
        words = makeFreq(text)
        tree = Tree()
        make_heap(tree, words)
        joinNodes(tree)
        getCodes(tree)
        pickle.dump(tree, key)
        encodedText = getEncodeText(tree,text)
        paddedEncodedText = pad_encoded_text(encodedText)
        b = getByteArray(paddedEncodedText)
        output.write(bytes(b))
        end = time.time()
        tminus = end-start
        sizeold = os.path.getsize(path)
        sizenew = os.path.getsize(output_path)
        comp = ((sizeold - sizenew)/sizeold)*100
        print("Tiempo tardado: ", tminus, " segundos")
        print("Compresión de ",comp,"%")
        print("Archivo comprimido: ", output_path)

if __name__ == "__main__":
    compress()

