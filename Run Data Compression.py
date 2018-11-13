from datacompression import compressionAlgorithmn


targetFile = "test2.txt"

h = compressionAlgorithmn(targetFile)

output_path = h.compress()
h.decompress(output_path)
