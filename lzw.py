import matplotlib.pyplot as plt
import time
import random

class LZW:
    '''lzw class'''
    def __init__(self) -> None:
        pass

    def __dictio(self, message:str): 
        """initialize dictionary"""
        result = []    
        for char in message:
            if char not in result:
                result.append(char)
        return result

    def encode(self, message):
        '''encode message'''
        dictionary = self.__dictio(message)
        index = 0
        result = []
        sub, char = '', ''
        while index < len(message):
            char = message[index]
            if sub+char in dictionary:
                sub = sub+char
            else:
                result.append(dictionary.index(sub))
                dictionary.append((sub+char))
                sub = char
            index += 1

        mes = ''.join([dictionary[x] for x in result])
        if mes != message:
            ost = message.replace(mes, '')
            result.append(dictionary.index(ost))
    
        return (result, self.__dictio(message))

    def decode(self, encoded_list, first_dict):
        '''decode message'''
        result = ''
        current_code = encoded_list[0]
        result += first_dict[current_code]
 
        for code in encoded_list[1:]:
            if code < len(first_dict):
                entry = first_dict[code]
            elif code == len(first_dict):
                entry = first_dict[current_code] + first_dict[current_code][0]
            else:
                raise ValueError("Invalid code in encoded list")
            result += entry
            first_dict.append(first_dict[current_code] + entry[0])
            current_code = code
        return result
   


# Function to generate random text of specified length
def generate_random_text(length):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choice(alphabet) for _ in range(length))

# Function to measure execution time of encoding and decoding
def measure_execution_time(input_size):
    lzw = LZW()
    text = generate_random_text(input_size)
    
    start_encode = time.time()
    encoded_result, _ = lzw.encode(text)
    end_encode = time.time()
    
    start_decode = time.time()
    decoded_result = lzw.decode(encoded_result, lzw._LZW__dictio(text))
    end_decode = time.time()
    
    encode_time = end_encode - start_encode
    decode_time = end_decode - start_decode
    
    return encode_time, decode_time, len(text), len(encoded_result)

# Function to calculate compression ratio
def calculate_compression_ratio(original_size, compressed_size):
    return ((original_size - compressed_size) / original_size) * 100

# Input sizes for investigation
input_sizes = [1000, 5000, 10000, 50000, 100000]

# Lists to store results
compression_ratios = []
encode_times = []
decode_times = []

# Investigating different input sizes
for size in input_sizes:
    encode_time, decode_time, original_size, compressed_size = measure_execution_time(size)
    
    compression_ratio = calculate_compression_ratio(original_size, compressed_size)
    
    compression_ratios.append(compression_ratio)
    encode_times.append(encode_time)
    decode_times.append(decode_time)

# Plotting compression ratio vs input size
plt.figure(figsize=(10, 5))
plt.plot(input_sizes, compression_ratios, marker='o', color='blue')
plt.title('Compression Ratio vs Input Size')
plt.xlabel('Input Size (bytes)')
plt.ylabel('Compression Ratio (%)')
plt.grid(True)
plt.show()

# Plotting execution time vs input size
plt.figure(figsize=(10, 5))
plt.plot(input_sizes, encode_times, marker='o', color='red', label='Encode Time')
plt.plot(input_sizes, decode_times, marker='o', color='green', label='Decode Time')
plt.title('Execution Time vs Input Size')
plt.xlabel('Input Size (bytes)')
plt.ylabel('Time (seconds)')
plt.legend()
plt.grid(True)
plt.show()