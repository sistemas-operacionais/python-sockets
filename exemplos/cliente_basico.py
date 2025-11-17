#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente Básico - Exemplo de Socket TCP
Conecta ao servidor e recebe uma mensagem.
"""

import socket

# Criar um socket TCP/IP
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar ao servidor
endereco_servidor = ('localhost', 5000)
cliente.connect(endereco_servidor)
print(f'Conectado ao servidor em {endereco_servidor[0]}:{endereco_servidor[1]}')

# Receber dados
dados = cliente.recv(1024)
print(f'Mensagem recebida: {dados.decode("utf-8")}')

# Fechar conexão
cliente.close()
print('Conexão encerrada')
