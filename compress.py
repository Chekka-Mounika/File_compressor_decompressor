
import heapq 
import os 
import pickle
class BinaryTree:
    def __init__(self,value,freq) :
        self.value=value 
        self.freq=freq 
        self.left=None 
        self.right=None  
    def __lt__(self,other):
        return self.freq<other.freq
    def __eq__(self,other):
        return self.freq==other.freq 

class HuffmanCode:
    def __init__(self,pathi) :
        self.path=pathi 
        self.__heap=[]
        self.__code={}
        self.__reverse_code={}
        self.__decompress_reverse_code={}

    def __frequency_creation_from_text(self,text):
        freq_dict={}
        for char in text:
            if char not in freq_dict:
                freq_dict[char]=1
            else:
                freq_dict[char]=freq_dict[char]+1
        return freq_dict
    
    def __Build_heap(self,freq_dic):
        for key in freq_dic:
            frequency=freq_dic[key]
            binary_tree_node=BinaryTree(key,frequency)
            heapq.heappush(self.__heap,binary_tree_node)
    
    def __Build_binary_tree(self):
        while len(self.__heap)>1:
            node1=heapq.heappop(self.__heap)
            node2=heapq.heappop(self.__heap)
            sum_freq=node1.freq+node2.freq
            newNode=BinaryTree(None,sum_freq)
            newNode.left=node1
            newNode.right=node2 
            heapq.heappush(self.__heap,newNode)
        return 
    
    def __Build_Tree_Code_Helper(self,root,curr_bits):
        if root is None:
            return 
        if root.value is not None:
            self.__code[root.value]=curr_bits
            self.__reverse_code[curr_bits]=root.value
            return 
        self.__Build_Tree_Code_Helper(root.left,curr_bits+'0')
        self.__Build_Tree_Code_Helper(root.right,curr_bits+'1')

    def __Build_Tree_code(self):
        root=heapq.heappop(self.__heap)
        self.__Build_Tree_Code_Helper(root,'')

    def __Build_Encoded_text(self,text):
        encode_text=''
        for char in text:
            encode_text+=self.__code[char]
        return encode_text
    
    def __Build_padded_text(self,encoded_text):
        padding_value=8-(len(encoded_text)%8)
        for i in range(padding_value):
            encoded_text+='0'
        padded_info="{0:08b}".format(padding_value).format(padding_value)         #mentioning padded info at the begining of encoding of text
        padded_text=padded_info+encoded_text
        return padded_text
    
    def __Build_bytes_array(self,padded_txt):
        array=[]
        for i in range(0,len(padded_txt),8):
            byte=padded_txt[i:i+8]
            array.append(int(byte,2))
        return array 
    

    def Compression(self):  
        print("Compression starts.......")
        #to acess the file and extract text from file
        filename,file_extension=os.path.splitext(self.path)
        output_path=filename+'.bin'
        with open(self.path,'r+') as file,open(output_path,'wb') as output:
            text=file.read()
            text=text.rstrip()
            freq_d=self.__frequency_creation_from_text(text)
            self.__Build_heap(freq_d)
            self.__Build_binary_tree()
            self.__Build_Tree_code()
            encoded_text=self.__Build_Encoded_text(text)
            padded_text=self.__Build_padded_text(encoded_text)
            bytes_array=self.__Build_bytes_array(padded_text)
            final_bytes=bytes(bytes_array)

            codebook = {'reverse_code': self.__reverse_code}
            pickle.dump(codebook, output)
            output.write(final_bytes)
        print("Compressed successfully!!!!!")
        #print(output_path)
        return output_path
    
    def __Text_after_Rm_padding(self,textt):
        padded_info=textt[:8]
        padded_value=int(padded_info,2)
        new_txt=textt[8:]
        new_txt = new_txt[:len(new_txt) - padded_value]
        return new_txt

    def __Decoded_text(self,txt):
        current_bite=''
        decoded_text=''
        for char in txt:
            current_bite+=char
            if current_bite in self.__decompress_reverse_code:
                decoded_text+=self.__decompress_reverse_code[current_bite]
                current_bite='' 
        return decoded_text
    

    def DeCompress(self,input_path):
        filename,file_extension=os.path.splitext(input_path)
        output_path=filename+"_decompressed"+".txt"
        with open(input_path,'rb') as file ,open(output_path,'w') as output:

            codebook = pickle.load(file)
            self.__decompress_reverse_code = codebook['reverse_code']

            bit_string=''
            byte=file.read(1)   #reading by bytes
            while byte:
                bits = bin(byte[0])[2:].rjust(8, '0')
                bit_string+=bits 
                byte=file.read(1)
            #print(bit_string)
            text_after_removing_padding=self.__Text_after_Rm_padding(bit_string)
            actual_text=self.__Decoded_text(text_after_removing_padding)
            output.write(actual_text)
            print("Decompressing done...")

character=input("Enter 'c' for compressing or 'd' for decompressing\n")
if(character=="c"):
    path=input("Enter the path of text file which you need to compress.Make sure you enter path without quotations : \n")
    h=HuffmanCode(path)
    output_pa=h.Compression()
elif(character=="d"):
    path=input("Enter the path of .bin file which you need to decompress.Make sure you enter path without quotations : \n")
    h=HuffmanCode(path)
    h.DeCompress(path)
else:
    print("INCORRECT INPUT")
