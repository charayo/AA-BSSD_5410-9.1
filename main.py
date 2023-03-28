# LZW Python compression code taken from: https://rosettacode.org/wiki/LZW_compression#Python
# Accessed on: 03/27/2023

import re
import pickle


def readTxt(filename, enc):
    with open(filename, 'r', encoding=enc) as file:
        file_texts = file.read()
        # print(texts)
        return file_texts


def perform_re(text):
    #  This special characters tend to cause
    text = re.sub(r"“", "\"", text)
    text = re.sub(r"”", "\"", text)
    text = re.sub(r"’", "'", text)
    text = re.sub(r"‘", "'", text)
    text = re.sub(r"—", "-", text)
    return text


def compress(uncompressed):
    """Compress a string to a list of output symbols."""

    # Build the dictionary.
    dict_size = 256
    # dictionary = dict((chr(i), i) for i in range(dict_size))
    # in Python 3:
    dictionary = {chr(i): i for i in range(dict_size)}

    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            # print(w, wc)
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    # Output the code for w.
    if w:
        # entry = (w, )
        result.append(dictionary[w])
    return result


def decompress(compressed):
    """Decompress a list of output ks to a string."""
    from io import StringIO

    # Build the dictionary.
    dict_size = 256
    dictionary = dict((i, chr(i)) for i in range(dict_size))
    # in Python 3: dictionary = {i: chr(i) for i in range(dict_size)}

    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = StringIO()
    w = chr(compressed.pop(0))
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)

        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry
    return result.getvalue()


def save_to_file(compressed_text, name):
    with open(name, "wb") as file:
        pickle.dump(compressed_text, file)
# end def save_to_file(compressed_text, name):


def load_from_file(file):
    with open(file, "rb") as file:
        text = pickle.load(file)
        return text


def read_compressed_file():
    # loading the compressed file and reading it into text
    loaded_texts = load_from_file("compressed.pickle")

    # decompressing and printing the compressed texts
    decompressed = decompress(loaded_texts)

    return decompressed[:45]


def main():
    #  loading the Alice text file for compression
    texts = readTxt("alice.txt", "utf-8")

    # replacing some special characters with the utf-8 recognized characters
    processed_text = perform_re(texts)

    #  performing the compression
    compressed = compress(processed_text)

    #  saving the compressed texts into a file
    save_to_file(compressed, "compressed.pickle")

    # load compressed file, decode and print the first 45 characters
    print(read_compressed_file())


if __name__ == "__main__":
    main()
