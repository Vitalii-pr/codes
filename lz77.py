

class lz77:
    def __init__(self, buffer:int) -> None:
        self.buffer = buffer if buffer > 0 else 5
        
    def encode(self, message):
        result = []
        index = 0

        while index < len(message):
            best_offset = -1
            best_length = -1
            best_match = ''

            for length in range(1, len(message) - index):
                substring = message[index:index + length]
                offset = message.rfind(substring, max(0, index - self.buffer), index)

                if offset != -1 and length > best_length:
                    best_offset = index - offset
                    best_length = length
                    best_match = substring

            if best_match:
                result.append((best_offset, best_length, message[index + best_length]))
                index += best_length + 1
            else:
                result.append((0, 0, message[index]))
                index += 1
        return self._list2text(result)

    def decode(self, code):
        code = self._text2list(code)
        message = ''
        for i in code:
            if i[0] == 0:
                message += str(i[2])
            else:
                start_index = len(message) - i[0]
                message += message[start_index:start_index + i[1]] + i[2]

        return message
    
    def _list2text(self, encoded):
        return ','.join([','.join(map(str,x)) for x in encoded])
    
    def _text2list(self, text:str):
        text = text.split(',')
        return [(int(text[x]), int(text[x+1]), text[x+2]) for x in range(0, len(text), 3)]


code = lz77(3)
encoded = code.encode('abacabacabadaca')
print(encoded)

print(code.decode(encoded))
    