#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente Echo - Exemplo de Socket TCP
Envia mensagens ao servidor e recebe respostas.
"""

import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('localhost', 5000))
print('Conectado ao servidor Echo')
print('Digite "sair" para encerrar a conexão\n')

try:
    while True:
        # Ler mensagem do usuário
        mensagem = input('Digite uma mensagem: ')
        
        if mensagem.lower() == 'sair':
            break
            
        # Enviar mensagem
        cliente.send(mensagem.encode('utf-8'))
        
        # Receber resposta
        resposta = cliente.recv(1024)
        print(f'Resposta: {resposta.decode("utf-8")}\n')
        
finally:
    cliente.close()
    print('Conexão encerrada')
