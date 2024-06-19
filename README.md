# Huffman Coding Compression-Decompression System

## Table of Contents

- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Key Features](#key-features)
- [Prerequisites](#prerequisites)
- [How to Run](#how-to-run)
  - [Compress a File](#compress-a-file)
  - [Decompress a File](#decompress-a-file)
- [Code Description](#code-description)
  - [BinaryTree Class](#binarytree-class)
  - [HuffmanCode Class](#huffmancode-class)

## Problem Statement

In the field of data storage and transmission, efficiently reducing the size of data files without losing information is crucial. Huffman Coding is a popular compression technique that helps in reducing file sizes by encoding data using variable-length codes. The challenge is to create a robust and efficient system for compressing and decompressing text files using Huffman Coding.

## Solution

This project addresses the problem by implementing a Huffman Coding compression and decompression system in Python. The system efficiently compresses text files and decompresses them back to their original form, ensuring no loss of data.

### Key Features

- **Efficient Compression:** Reduces the size of text files using Huffman Coding.
- **Accurate Decompression:** Restores compressed files back to their original form.
- **Binary Tree Construction:** Utilizes a binary tree for Huffman Coding.
- **File Handling:** Reads from and writes to files seamlessly.

## Prerequisites
1. Install the required library using pip:
- Python 3.x
  ```bash
    pip install numpy

### How to Run
## Compress a File
1. To compress a file, run the following command:
   ```bash
     python huffman.py
When prompted, enter c for compression and provide the path to the text file to be compressed.
## Decompress a File
2. To decompress a file, run the following command:
   ```bash
     python huffman.py
When prompted, enter d for decompression and provide the path to the .bin file to be decompressed.

### Code Description
## BinaryTree Class
1. The BinaryTree class represents a node in the Huffman Coding tree. Each node contains a value, a frequency, and references to left and right child nodes.
   ```bash
    class BinaryTree:
    def __init__(self, value, freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        return self.freq == other.freq
## HuffmanCode Class 
1. The HuffmanCode class handles the compression and decompression processes. It includes methods for creating frequency dictionaries, building heaps and binary trees, generating codes, encoding and decoding text, and managing file I/O.
    ```python
    class HuffmanCode:
    def __init__(self, pathi):
        self.path = pathi
        self.__heap = []
        self.__code = {}
        self.__reverse_code = {}
        self.__decompress_reverse_code = {}

    def __frequency_creation_from_text(self, text):
        freq_dict = {}
        for char in text:
            if char not in freq_dict:
                freq_dict[char] = 1
            else:
                freq_dict[char] += 1
        return freq_dict

    def __Build_heap(self, freq_dic):
        for key in freq_dic:
            frequency = freq_dic[key]
            binary_tree_node = BinaryTree(key, frequency)
            heapq.heappush(self.__heap, binary_tree_node)

    def __Build_binary_tree(self):
        while len(self.__heap) > 1:
            node1 = heapq.heappop(self.__heap)
            node2 = heapq.heappop(self.__heap)
            sum_freq = node1.freq + node2.freq
            newNode = BinaryTree(None, sum_freq)
            newNode.left = node1
            newNode.right = node2
            heapq.heappush(self.__heap, newNode)
        return

    def __Build_Tree_Code_Helper(self, root, curr_bits):
        if root is None:
            return
        if root.value is not None:
            self.__code[root.value] = curr_bits
            self.__reverse_code[curr_bits] = root.value
            return
        self.__Build_Tree_Code_Helper(root.left, curr_bits + '0')
        self.__Build_Tree_Code_Helper(root.right, curr_bits + '1')

    def __Build_Tree_code(self):
        root = heapq.heappop(self.__heap)
        self.__Build_Tree_Code_Helper(root, '')

    def __Build_Encoded_text(self, text):
        encode_text = ''
        for char in text:
            encode_text += self.__code[char]
        return encode_text

    def __Build_padded_text(self, encoded_text):
        padding_value = 8 - (len(encoded_text) % 8)
        for i in range(padding_value):
            encoded_text += '0'
        padded_info = "{0:08b}".format(padding_value)
        padded_text = padded_info + encoded_text
        return padded_text

    def __Build_bytes_array(self, padded_txt):
        array = []
        for i in range(0, len(padded_txt), 8):
            byte = padded_txt[i:i + 8]
            array.append(int(byte, 2))
        return array

    def Compression(self):
        print("Compression starts.......")
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + '.bin'
        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()
            freq_d = self.__frequency_creation_from_text(text)
            self.__Build_heap(freq_d)
            self.__Build_binary_tree()
            self.__Build_Tree_code()
            encoded_text = self.__Build_Encoded_text(text)
            padded_text = self.__Build_padded_text(encoded_text)
            bytes_array = self.__Build_bytes_array(padded_text)
            final_bytes = bytes(bytes_array)

            codebook = {'reverse_code': self.__reverse_code}
            pickle.dump(codebook, output)
            output.write(final_bytes)
        print("Compressed successfully!!!!!")
        return output_path

    def __Text_after_Rm_padding(self, textt):
        padded_info = textt[:8]
        padded_value = int(padded_info, 2)
        new_txt = textt[8:]
        new_txt = new_txt[:len(new_txt) - padded_value]
        return new_txt

    def __Decoded_text(self, txt):
        current_bite = ''
        decoded_text = ''
        for char in txt:
            current_bite += char
            if current_bite in self.__decompress_reverse_code:
                decoded_text += self.__decompress_reverse_code[current_bite]
                current_bite = ''
        return decoded_text

    def DeCompress(self, input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + "_decompressed" + ".txt"
        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            codebook = pickle.load(file)
            self.__decompress_reverse_code = codebook['reverse_code']

            bit_string = ''
            byte = file.read(1)
            while byte:
                bits = bin(byte[0])[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)
            text_after_removing_padding = self.__Text_after_Rm_padding(bit_string)
            actual_text = self.__Decoded_text(text_after_removing_padding)
            output.write(actual_text)
            print("Decompressing done...")

    ```
- __frequency_creation_from_text(text): Creates a frequency dictionary from the input text.
- __Build_heap(freq_dic): Builds a heap from the frequency dictionary.
- __Build_binary_tree(): Constructs the binary tree from the heap.
- __Build_Tree_Code_Helper(root, curr_bits): Helper function to generate codes from the binary tree.
- __Build_Tree_code(): Generates Huffman codes from the binary tree.
- __Build_Encoded_text(text): Encodes the input text using the generated codes.
- __Build_padded_text(encoded_text): Pads the encoded text to ensure it is a multiple of 8 bits.
- __Build_bytes_array(padded_txt): Converts the padded text to a byte array.
- Compression(): Compresses the input text file and saves the compressed file.
- __Text_after_Rm_padding(textt): Removes padding from the decompressed text.
- __Decoded_text(txt): Decodes the decompressed text using the reverse codes.
- DeCompress(input_path): Decompresses the input file and saves the decompressed text file.


## Running the Code
1. Run the script and follow the prompts for compression and decompression:
   ```bash
   character = input("Enter 'c' for compressing or 'd' for decompressing\n")
   if character == "c":
      path = input("Enter the path of text file which you need to compress. Make sure you enter path without quotations: \n")
      h = HuffmanCode(path)
      output_pa = h.Compression()
   elif character == "d":
      path = input("Enter the path of .bin file which you need to decompress. Make sure you enter path without quotations: \n")
      h = HuffmanCode(path)
      h.DeCompress(path

