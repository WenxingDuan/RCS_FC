import numpy as np


def generate_bit_strings(n, p):
    # Initialize all bit strings to zero
    bit_strings = np.zeros((50000, n), dtype=np.int8)

    # Generate a uniform random array with the same shape as bit_strings
    rand_array = np.random.rand(50000, n)

    # Find where a random event (with probability p) occurs
    event_occurs = rand_array < p

    # Where an event occurs, generate a new bit (0 or 1)
    bit_strings[event_occurs] = np.random.randint(
        2, size=np.count_nonzero(event_occurs))

    # Convert the bit strings to strings
    bit_strings = np.array([''.join(row.astype(str)) for row in bit_strings])

    return bit_strings


p = 0.5
bit_strings = generate_bit_strings(12, p=0.5)

# Open the file in write mode ('w')
with open(f'Toy Circuit\\OriganToy\\{p}.txt', 'w') as f:
    # Write each bit string on a new line
    for bit_string in bit_strings:
        f.write(bit_string + '\n')

def process_bit_strings(bit_strings, x):
    # Initialize a list to hold the processed bit strings
    processed_bit_strings = []

    # Iterate over the bit strings
    for bit_string in bit_strings:
        # Convert the string to a list of integers
        bit_list = list(map(int, bit_string))

        # Iterate over the bits in the list
        for i in range(len(bit_list)):
            # If the bit is 1
            if bit_list[i] == 1:
                # With probability x, change it to 0
                if np.random.rand() < x:
                    bit_list[i] = 0

        # Convert the list of bits back to a string and add it to the processed list
        processed_bit_string = ''.join(map(str, bit_list))
        processed_bit_strings.append(processed_bit_string)

    return processed_bit_strings

processed_bit_strings = process_bit_strings(bit_strings, 0.3)

# Open the file in write mode ('w')
with open(f'Toy Circuit\\ADToy\\{p}.txt', 'w') as f:
    # Write each processed bit string on a new line
    for bit_string in processed_bit_strings:
        f.write(bit_string + '\n')
