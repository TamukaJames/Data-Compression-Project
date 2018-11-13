from datacompression import compressionAlgorithmn


targetFile = "sample.txt
"

h = compressionAlgorithmn(targetFile)

output_path = h.compress()
h.decompress(output_path)
