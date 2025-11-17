#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente de Chat - Exemplo de Socket TCP com Threading
Permite enviar e receber mensagens simultaneamente.
"""

import socket
import threading

def receber_mensagens(cliente):
    """Thread para receber mensagens do servidor"""
    while True:
        try:
            mensagem = cliente.recv(1024).decode('utf-8')
            if mensagem == 'APELIDO':
                cliente.send(apelido.encode('utf-8'))
            else:
                print(mensagem)
        except:
            print('Erro ao receber mensagem!')
            cliente.close()
            break

def enviar_mensagens(cliente):
    """Thread para enviar mensagens ao servidor"""
    while True:
        try:
            mensagem = input('')
            mensagem_completa = f'{apelido}: {mensagem}'
            cliente.send(mensagem_completa.encode('utf-8'))
        except:
            cliente.close()
            break

# Configuração
apelido = input('Escolha seu apelido: ')

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('localhost', 5000))

# Iniciar threads
thread_receber = threading.Thread(target=receber_mensagens, args=(cliente,))
thread_receber.start()

thread_enviar = threading.Thread(target=enviar_mensagens, args=(cliente,))
thread_enviar.start()
