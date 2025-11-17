#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Echo - Exemplo de Socket TCP
Devolve qualquer mensagem que recebe (echo).
Pode processar múltiplas conexões sequencialmente.
"""

import socket

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(('localhost', 5000))
servidor.listen(1)
print('Servidor Echo escutando em localhost:5000')

while True:
    print('\nAguardando conexão...')
    conexao, endereco = servidor.accept()
    print(f'Conectado com {endereco}')
    
    try:
        while True:
            # Receber dados
            dados = conexao.recv(1024)
            
            if not dados:
                print('Cliente desconectou')
                break
                
            mensagem = dados.decode('utf-8')
            print(f'Recebido: {mensagem}')
            
            # Enviar dados de volta (echo)
            resposta = f'Echo: {mensagem}'
            conexao.send(resposta.encode('utf-8'))
            
    finally:
        conexao.close()
