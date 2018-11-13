import heapq
import os


#Data compression through the HuffMan Algorithmn and the heapq module used for traversing through the huffman tress
class HeapNode:
	def __init__(self, char, freq):
		self.char = char
		self.freq = freq
		self.left = None
		self.right = None

	# defining comparators less_than and equals
	def __lt__(self, other):
		return self.freq < other.freq

	def __eq__(self, other):
		if(other == None):
			return False
		if(not isinstance(other, HeapNode)):
			return False
		return self.freq == other.freq


class compressionAlgorithmn:
	def __init__(self, targetFile):
		self.targetFile = targetFile
		self.heap = []
		self.codes = {}
		self.reverseMap = {}

	# functions for compression:

	def freqDict(self, text):
		dictionary = {}
		for item in text:
			if not item in dictionary:
				dictionary[item] = 0
			dictionary[item] += 1
		return dictionary

	def buildHeap(self, dictionary):
		for key in dictionary:
			node = HeapNode(key, dictionary[key])
			heapq.heappush(self.heap, node)

	def mergeNodes(self):
		while(len(self.heap)>1):
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = HeapNode(None, node1.freq + node2.freq)
			merged.left = node1
			merged.right = node2

			heapq.heappush(self.heap, merged)


	def charMap(self, root, charCodes):
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = charCodes
			self.reverseMap[charCodes] = root.char
			return

		self.charMap(root.left, charCodes + "0")
		self.charMap(root.right, charCodes + "1")


	def charCode(self):
		root = heapq.heappop(self.heap)
		charCodes = ""
		self.charMap(root, charCodes)


	def encode(self, text):
		encodedTxt = ""
		for item in text:
			encodedTxt += self.codes[item]
		return encodedTxt


	def padEncodedtxt(self, encodedTxt):
		extra_padding = 8 - len(encodedTxt) % 8
		for i in range(extra_padding):
			encodedTxt += "0"

		pinfo = "{0:08b}".format(extra_padding)
		encodedTxt = pinfo + encodedTxt
		return encodedTxt


	def byteArray(self, paddedTxt):
		if(len(paddedTxt) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(paddedTxt), 8):
			byte = paddedTxt[i:i+8]
			b.append(int(byte, 2))
		return b


	def compress(self):
		filename, file_extension = os.path.splitext(self.targetFile)
		output_path = filename + ".zip"

		with open(self.targetFile, 'r+') as file, open(output_path, 'wb') as output:
			text = file.read()
			text = text.rstrip()

			dictionary = self.freqDict(text)
			self.buildHeap(dictionary)
			self.mergeNodes()
			self.charCode()

			encodedTxt = self.encode(text)
			paddedTxt = self.padEncodedtxt(encodedTxt)

			b = self.byteArray(paddedTxt)
			output.write(bytes(b))

		print("File successfully Compressed")
		return output_path




#Functions to process decompression

	def remPadding(self, paddedTxt):
		pinfo = paddedTxt[:8]
		extra = int(pinfo, 2)

		paddedTxt = paddedTxt[8:]
		encodedTxt = paddedTxt[:-1*extra]

		return encodedTxt

	def decode(self, encodedTxt):
		charCodes = ""
		decoded = ""

		for bit in encodedTxt:
			charCodes += bit
			if(charCodes in self.reverseMap):
				item = self.reverseMap[charCodes]
				decoded += item
				charCodes = ""

		return decoded


	def decompress(self, input_path):
		filename, file_extension = os.path.splitext(self.targetFile)
		output_path = filename + "_decompressed" + ".txt"

		with open(input_path, 'rb') as file, open(output_path, 'w') as output:
			bit_string = ""

			byte = file.read(1)
			while(len(byte) > 0):
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bit_string += bits
				byte = file.read(1)

			encodedTxt = self.remPadding(bit_string)

			decompressed_text = self.decode(encodedTxt)

			output.write(decompressed_text)

		print("Previously Compressed File Has been Successfully Decompressed")
		return output_path
