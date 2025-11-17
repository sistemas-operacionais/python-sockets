#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor de Chat - Exemplo de Socket TCP com Threading
Suporta múltiplos clientes simultaneamente usando threads.
"""

import socket
import threading

clientes = []
apelidos = []

def broadcast(mensagem, remetente=None):
    """Envia mensagem para todos os clientes conectados"""
    for cliente in clientes:
        if cliente != remetente:
            try:
                cliente.send(mensagem)
            except:
                # Remove cliente se houver erro
                indice = clientes.index(cliente)
                clientes.remove(cliente)
                apelidos.pop(indice)

def handle_cliente(cliente):
    """Gerencia a comunicação com um cliente específico"""
    while True:
        try:
            # Receber mensagem
            mensagem = cliente.recv(1024)
            if mensagem:
                broadcast(mensagem, cliente)
            else:
                # Cliente desconectou
                indice = clientes.index(cliente)
                clientes.remove(cliente)
                cliente.close()
                apelido = apelidos[indice]
                apelidos.remove(apelido)
                broadcast(f'{apelido} saiu do chat!'.encode('utf-8'))
                print(f'{apelido} desconectou')
                break
        except:
            indice = clientes.index(cliente)
            clientes.remove(cliente)
            cliente.close()
            apelido = apelidos[indice]
            apelidos.remove(apelido)
            broadcast(f'{apelido} saiu do chat!'.encode('utf-8'))
            print(f'{apelido} desconectou')
            break

def receber_conexoes():
    """Aceita novas conexões de clientes"""
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(('localhost', 5000))
    servidor.listen()
    print('Servidor de Chat iniciado em localhost:5000')
    
    while True:
        cliente, endereco = servidor.accept()
        print(f'Conexão estabelecida com {endereco}')
        
        # Solicitar apelido
        cliente.send('APELIDO'.encode('utf-8'))
        apelido = cliente.recv(1024).decode('utf-8')
        
        # Adicionar à lista
        apelidos.append(apelido)
        clientes.append(cliente)
        
        print(f'Apelido do cliente: {apelido}')
        broadcast(f'{apelido} entrou no chat!'.encode('utf-8'))
        cliente.send('Conectado ao servidor!'.encode('utf-8'))
        
        # Criar thread para o cliente
        thread = threading.Thread(target=handle_cliente, args=(cliente,))
        thread.start()

if __name__ == '__main__':
    receber_conexoes()
