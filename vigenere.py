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
#parte 2

FREQ_PT = {'A': 0.1463, 'B': 0.0104, 'C': 0.0388, 'D': 0.0499, 'E': 0.1257, 'F': 0.0102, 'G': 0.0130, 'H': 0.0128, 'I': 0.0618, 'J': 0.0040, 'K': 0.0002, 'L': 0.0278, 'M': 0.0474, 'N': 0.0505, 'O': 0.1073, 'P': 0.0252, 'Q': 0.0120, 'R': 0.0653, 'S': 0.0781, 'T': 0.0434, 'U': 0.0463, 'V': 0.0167, 'W': 0.0001, 'X': 0.0021, 'Y': 0.0001, 'Z': 0.0047}

FREQ_EN = {'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702, 'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507, 'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056, 'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974, 'Z': 0.00074}

def quebrar_vigenere(criptograma, freq_idioma, max_tam=20):
    texto = "".join([c for c in criptograma.upper() if c.isalpha()])
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # 1. DESCOBRIR O TAMANHO DA CHAVE 
    ic_tamanhos = {}
    
    # Primeiro, calculamos o Índice de Coincidência para todos os tamanhos
    for tam in range(1, max_tam + 1):
        soma_ic_colunas = 0
        for i in range(tam):
            coluna = texto[i::tam]
            if len(coluna) > 0:
                soma_ic_colunas += sum((coluna.count(c) / len(coluna)) ** 2 for c in alfabeto)
        ic_tamanhos[tam] = soma_ic_colunas / tam

    #Depois, procuramos o primeiro tamanho que atinge um IC aceitável (> 0.065)
    melhor_tam = 1 
    for tam in range(1, max_tam + 1):
        if ic_tamanhos[tam] > 0.065:
            melhor_tam = tam
            break

    #DESCOBRIR A SENHA
    senha = ""
    for i in range(melhor_tam):
        coluna = texto[i::melhor_tam]
        melhor_letra = 'A'
        maior_produto = 0
        
        for letra_teste in alfabeto:
            col_decifrada = decifrador_de_vigenere(coluna, letra_teste)
            
            produto = sum((col_decifrada.count(c) / len(coluna)) * freq_idioma.get(c, 0) for c in alfabeto)
            
            if produto > maior_produto:
                maior_produto = produto
                melhor_letra = letra_teste
        senha += melhor_letra
        
    return senha

# Função auxiliar para evitar o erro de IndexError com acentos durante o teste
def limpar_texto(texto):
    com_acento = "ÁÀÃÂÉÈÊÍÌÎÓÒÕÔÚÙÛÇáàãâéèêíìîóòõôúùûç"
    sem_acento = "AAAAEEEIIIOOOOUUUCaaaaeeeiiioooouuuc"
    return texto.translate(str.maketrans(com_acento, sem_acento))

#Portugues
mensagem_pt = """
O cifrador recebe uma senha e uma mensagem que e cifrada segundo a cifra de Vigenere 
gerando um criptograma enquanto o decifrador recebe uma senha e um criptograma que 
e decifrado segundo a cifra de Vigenere recuperando uma mensagem. Os primeiros 
usuarios da cifra de Vigenere utilizavam um quadrado de Vigenere como mostrado na 
Figura 1 para descobrir rapidamente qual letra do texto cifrado usar dado um texto plano 
e fluxo de teclas especificos.
"""
mensagem_pt_limpa = limpar_texto(mensagem_pt)
criptograma_pt = cifrador_de_vigenere(mensagem_pt_limpa, "PASCOA")

# O ataque usando a tabela do Português
senha_descoberta_pt = quebrar_vigenere(criptograma_pt, FREQ_PT)
print(f"Senha recuperada: {senha_descoberta_pt}")
print(f"Mensagem: {decifrador_de_vigenere(criptograma_pt, senha_descoberta_pt)}\n")

mensagem_en = """
The Vigenere cipher is a method of encrypting alphabetic text by using a series of 
interwoven Caesar ciphers, based on the letters of a keyword. It employs a form of 
polyalphabetic substitution. The cipher is easy to understand and implement, but it 
resisted all attempts to break it for three centuries, which earned it the description 
le chiffre indechiffrable (the indecipherable cipher).
"""
mensagem_en_limpa = limpar_texto(mensagem_en)
criptograma_en = cifrador_de_vigenere(mensagem_en_limpa, "SECURITY")

# O ataque usando a tabela do Inglês
senha_descoberta_en = quebrar_vigenere(criptograma_en, FREQ_EN)
print(f"Senha recuperada: {senha_descoberta_en}")
print(f"Mensagem: {decifrador_de_vigenere(criptograma_en, senha_descoberta_en)}\n")