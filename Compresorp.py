import heapq
import pickle
import time
import sys
import math
from mpi4py import MPI
 
 #Definimos la clase para el Arbol de Huffman
class Tree:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverseMapping = {}

#Definimos la clase Nodo para el Arbol de Huffman
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

#Funcion recursiva auxiliar para obtener los codigos dentro del arbol
def getCodesHelper(tree, root, current_code):

    if (root.char != None):
        tree.codes[root.char] = current_code
        tree.reverseMapping[current_code] = root.char
        return

    getCodesHelper(tree, root.left, current_code + "0")
    getCodesHelper(tree, root.right, current_code + "1")

#Funcion principal para obtener los codigos dentro del arbol
def getCodes(tree):
    root = heapq.heappop(tree.heap)
    current_code = ""
    getCodesHelper(tree, root, current_code)

#Funcion para obtener la frecuencia de un caracter
def makeFreq(text):
    frequency = {char: text.count(char) for char in set(text)}
    return frequency

#Funcion para juntar los nodos con el arbol
def joinNodes(self):
    while(len(self.heap)>1):
        node1 = heapq.heappop(self.heap)
        node2 = heapq.heappop(self.heap)
        newnode = Node(None, node1.freq + node2.freq)
        newnode.left = node1
        newnode.right = node2
        heapq.heappush(self.heap, newnode)

#Funcion para hacer saltos entre niveles del arbol
def make_heap(tree, frequency):
    nodes = [Node(key, frequency[key]) for key in frequency]
    [heapq.heappush(tree.heap, node) for node in nodes]
    tree.root = tree.heap[len(tree.heap)-1]

#Funcion para obtener el texto codificado
def getEncodeText(tree, text):
    encoded_text = ""
    encoded_text += ''.join([tree.codes.get(char, '') for char in text])
    return encoded_text

#Funcion para obtener el arreglo de Bytes
def getByteArray(text):
    bytes_list = [int(text[i:i+8], 2) for i in range(0, len(text), 8)]
    return bytearray(bytes_list)

#Funcion para añadir padding al arreglo de bytes
def pad_encoded_text(encoded_text):
	extra_padding = 8 - len(encoded_text) % 8
	for i in range(extra_padding):
		encoded_text += "0"
	padded_info = "{0:08b}".format(extra_padding)
	encoded_text = padded_info + encoded_text
	return encoded_text

#Funcion principal del compresor
def compress():

    #Nombre y ruta de salida del archivo
    output_path = "comprimidop.elmejorprofesor"
    path = sys.argv[1]
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  
    size = comm.Get_size() 

    with open(path, 'r', encoding="ISO-8859-1", newline="") as file, open("clave.elmejorprofesor", "wb") as key,open(output_path, 'wb') as output:
        
        #Trabajador raiz
        if rank == 0:
            text = file.read()
            chunk_size = math.ceil(len(text) / size)
            start = time.time()
            words = makeFreq(text)
            tree = Tree()
            make_heap(tree, words)
            joinNodes(tree)
            getCodes(tree)
            pickle.dump(tree, key)
            comm.bcast(tree, root=0)

            scattered_text = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

            encoded_chunks = comm.scatter(scattered_text, root=0)
            encodedText = getEncodeText(tree, encoded_chunks)
            gathered_chunks = comm.gather(encodedText, root=0)
            received_chunks = ''.join(gathered_chunks)
            pad_received_chunks = pad_encoded_text(received_chunks)

            b = getByteArray(pad_received_chunks)
            output.write(bytes(b))

            end = time.time()
            tminus = end - start
            print("Tiempo tardado: ", tminus, " segundos")

        #Demás Trabajadores
        else:
            scattered_text = None
            encoded_chunk = comm.scatter(scattered_text, root=0)
            tree = comm.bcast(None, root=0)
            encodedText = getEncodeText(tree, encoded_chunk)
            comm.gather(encodedText, root=0)
if __name__ == "__main__":
    compress()

