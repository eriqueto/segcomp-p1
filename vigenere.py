def quadro_de_vigenere():
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    quadro = []
    for i in range(len(alfabeto)):
        linha = alfabeto[i:] + alfabeto[:i]
        quadro.append(linha)
    return quadro

quadro = quadro_de_vigenere()

def cifrador_de_vigenere(plaintext, key):
    ciphertext = []
    # plaintext define coluna
    plaintext = plaintext.upper()
    # key define linha
    key = key.upper()
    
    idx = 0
    for char in plaintext:
        if not char.isalpha():
            ciphertext.append(char)
        else:
            coluna = ord(char) - ord('A')
            linha = ord(key[idx]) - ord('A')
            ciphertext.append(quadro[linha][coluna])
            idx = (idx+1) % len(key)

    return "".join(ciphertext)

def decifrador_de_vigenere(ciphertext, key):
    plaintext = []
    # fazer o caminho inverso do encoder
    key = key.upper()
    ciphertext = ciphertext.upper()

    idx = 0
    for char in ciphertext:
        if not char.isalpha():
            plaintext.append(char)
        else:
            linha = ord(key[idx]) - ord('A')
            quadro_linha = quadro[linha]
            coluna = quadro_linha.index(char)
            plaintext.append(chr(coluna + ord('A')))
            idx = (idx+1) % len(key)

    return "".join(plaintext)

ciphertext = cifrador_de_vigenere('ATTACK AT DAWN', 'LEMON')
plaintext = decifrador_de_vigenere('LXFOPV EF RNHR', 'LEMON')
print(plaintext)