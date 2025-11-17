#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Básico - Exemplo de Socket TCP
Aceita uma conexão e envia uma mensagem de boas-vindas.
"""

import socket

# Criar um socket TCP/IP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Permitir reutilização do endereço
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Vincular o socket a um endereço e porta
endereco = ('localhost', 5000)
servidor.bind(endereco)

# Escutar por conexões (máximo de 1 conexão na fila)
servidor.listen(1)
print(f'Servidor escutando em {endereco[0]}:{endereco[1]}')

# Aguardar por uma conexão
conexao, endereco_cliente = servidor.accept()
print(f'Conexão estabelecida com {endereco_cliente}')

# Enviar mensagem
mensagem = 'Bem-vindo ao servidor!'
conexao.send(mensagem.encode('utf-8'))

# Fechar a conexão
conexao.close()
servidor.close()
print('Servidor encerrado')
