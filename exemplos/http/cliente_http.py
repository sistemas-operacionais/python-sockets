#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente HTTP Básico - Exemplo de Socket TCP
Implementa um cliente HTTP simples que faz requisições GET.
"""

import socket

def fazer_requisicao_http(host, porta, caminho='/'):
    """
    Faz uma requisição HTTP GET e retorna a resposta.
    
    Args:
        host: Nome do host ou endereço IP
        porta: Número da porta
        caminho: Caminho da requisição (padrão: '/')
    
    Returns:
        Tuple (status_code, headers, body) ou None em caso de erro
    """
    # Criar socket TCP/IP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Conectar ao servidor
        print(f'Conectando a {host}:{porta}...')
        cliente.connect((host, porta))
        print('Conectado!\n')
        
        # Construir requisição HTTP GET
        requisicao = f"GET {caminho} HTTP/1.1\r\n"
        requisicao += f"Host: {host}:{porta}\r\n"
        requisicao += "User-Agent: Cliente-HTTP-Python/1.0\r\n"
        requisicao += "Accept: text/html\r\n"
        requisicao += "Connection: close\r\n"
        requisicao += "\r\n"
        
        # Enviar requisição
        print('Enviando requisição:')
        print('-' * 40)
        print(requisicao)
        cliente.sendall(requisicao.encode('utf-8'))
        
        # Receber resposta completa
        resposta = b''
        while True:
            dados = cliente.recv(4096)
            if not dados:
                break
            resposta += dados
        
        # Decodificar resposta
        resposta_str = resposta.decode('utf-8', errors='ignore')
        
        # Separar cabeçalhos do corpo
        partes = resposta_str.split('\r\n\r\n', 1)
        if len(partes) != 2:
            print('Resposta HTTP inválida')
            return None
        
        cabecalhos_raw, corpo = partes
        
        # Extrair código de status
        linhas_cabecalho = cabecalhos_raw.split('\r\n')
        status_line = linhas_cabecalho[0]
        
        partes_status = status_line.split(' ', 2)
        if len(partes_status) >= 2:
            status_code = partes_status[1]
        else:
            status_code = 'Desconhecido'
        
        # Extrair cabeçalhos
        cabecalhos = {}
        for linha in linhas_cabecalho[1:]:
            if ':' in linha:
                chave, valor = linha.split(':', 1)
                cabecalhos[chave.strip()] = valor.strip()
        
        return status_code, cabecalhos, corpo
    
    except ConnectionRefusedError:
        print(f'Erro: Não foi possível conectar a {host}:{porta}')
        print('Verifique se o servidor está rodando.')
        return None
    
    except Exception as e:
        print(f'Erro: {e}')
        return None
    
    finally:
        cliente.close()

def exibir_resposta(status_code, cabecalhos, corpo):
    """
    Exibe a resposta HTTP de forma formatada.
    
    Args:
        status_code: Código de status HTTP
        cabecalhos: Dicionário com os cabeçalhos
        corpo: Corpo da resposta
    """
    print('Resposta recebida:')
    print('=' * 40)
    print(f'Status: {status_code}')
    print('\nCabeçalhos:')
    for chave, valor in cabecalhos.items():
        print(f'  {chave}: {valor}')
    
    print('\nCorpo da resposta:')
    print('-' * 40)
    print(corpo)
    print('-' * 40)

def menu_interativo():
    """Menu interativo para fazer requisições."""
    host = 'localhost'
    porta = 8080
    
    print('=' * 50)
    print('Cliente HTTP Básico em Python')
    print('=' * 50)
    print(f'\nServidor padrão: {host}:{porta}')
    print('(Certifique-se de que o servidor está rodando)\n')
    
    while True:
        print('\nEscolha uma opção:')
        print('1. Página inicial (/)')
        print('2. Sobre (/sobre)')
        print('3. Contato (/contato)')
        print('4. Página customizada')
        print('5. Sair')
        
        opcao = input('\nOpção: ').strip()
        
        if opcao == '1':
            caminho = '/'
        elif opcao == '2':
            caminho = '/sobre'
        elif opcao == '3':
            caminho = '/contato'
        elif opcao == '4':
            caminho = input('Digite o caminho (ex: /teste): ').strip()
        elif opcao == '5':
            print('\nEncerrando cliente...')
            break
        else:
            print('Opção inválida!')
            continue
        
        print(f'\n{"=" * 50}')
        resultado = fazer_requisicao_http(host, porta, caminho)
        
        if resultado:
            status_code, cabecalhos, corpo = resultado
            exibir_resposta(status_code, cabecalhos, corpo)
        
        print('=' * 50)

def main():
    """Função principal do cliente HTTP."""
    try:
        menu_interativo()
    except KeyboardInterrupt:
        print('\n\nCliente encerrado pelo usuário')
    except Exception as e:
        print(f'\nErro: {e}')

if __name__ == '__main__':
    main()
