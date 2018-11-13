from test import compressionAlgo


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