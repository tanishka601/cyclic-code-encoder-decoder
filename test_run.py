print("CYCLIC CODE PROJECT STARTED!")

GENERATOR = 0b1011

def remainder(poly):
    while poly.bit_length() >= GENERATOR.bit_length():
        shift = poly.bit_length() - GENERATOR.bit_length()
        poly ^= GENERATOR << shift
    return poly

def encode(message):
    shifted = message << 3
    return shifted | remainder(shifted)

message = 0b1011
codeword = encode(message)

print("Original message:", format(message, "04b"))
print("Encoded codeword:", format(codeword, "07b"))
print("Syndrome:", format(remainder(codeword), "03b"))
