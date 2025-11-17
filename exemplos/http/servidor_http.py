#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor HTTP Básico - Exemplo de Socket TCP
Implementa um servidor HTTP simples que responde a requisições GET.
"""

import socket

def construir_resposta_http(codigo, mensagem, conteudo):
    """
    Constrói uma resposta HTTP válida.
    
    Args:
        codigo: Código de status HTTP (ex: 200, 404)
        mensagem: Mensagem de status (ex: "OK", "Not Found")
        conteudo: Conteúdo HTML da resposta
    
    Returns:
        String com a resposta HTTP completa
    """
    resposta = f"HTTP/1.1 {codigo} {mensagem}\r\n"
    resposta += "Content-Type: text/html; charset=utf-8\r\n"
    resposta += f"Content-Length: {len(conteudo.encode('utf-8'))}\r\n"
    resposta += "Connection: close\r\n"
    resposta += "\r\n"
    resposta += conteudo
    return resposta

def processar_requisicao(requisicao):
    """
    Processa uma requisição HTTP e retorna a resposta apropriada.
    
    Args:
        requisicao: String com a requisição HTTP
    
    Returns:
        String com a resposta HTTP
    """
    # Extrair primeira linha da requisição
    linhas = requisicao.split('\r\n')
    if not linhas:
        return construir_resposta_http(400, "Bad Request", "<h1>400 - Requisição Inválida</h1>")
    
    primeira_linha = linhas[0].split()
    if len(primeira_linha) < 2:
        return construir_resposta_http(400, "Bad Request", "<h1>400 - Requisição Inválida</h1>")
    
    metodo = primeira_linha[0]
    caminho = primeira_linha[1]
    
    print(f"  Método: {metodo}, Caminho: {caminho}")
    
    # Suportar apenas GET
    if metodo != "GET":
        conteudo = "<h1>405 - Método Não Permitido</h1><p>Este servidor suporta apenas GET</p>"
        return construir_resposta_http(405, "Method Not Allowed", conteudo)
    
    # Roteamento simples
    if caminho == "/" or caminho == "/index.html":
        conteudo = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Servidor HTTP Python</title>
</head>
<body>
    <h1>Bem-vindo ao Servidor HTTP!</h1>
    <p>Este é um servidor HTTP básico implementado com sockets Python.</p>
    <ul>
        <li><a href="/">Página Inicial</a></li>
        <li><a href="/sobre">Sobre</a></li>
        <li><a href="/contato">Contato</a></li>
    </ul>
</body>
</html>
"""
        return construir_resposta_http(200, "OK", conteudo)
    
    elif caminho == "/sobre":
        conteudo = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Sobre - Servidor HTTP Python</title>
</head>
<body>
    <h1>Sobre Este Servidor</h1>
    <p>Este é um exemplo educacional de servidor HTTP implementado usando sockets TCP em Python.</p>
    <p>Características:</p>
    <ul>
        <li>Aceita requisições HTTP GET</li>
        <li>Serve páginas HTML estáticas</li>
        <li>Usa apenas a biblioteca padrão do Python</li>
    </ul>
    <p><a href="/">Voltar à página inicial</a></p>
</body>
</html>
"""
        return construir_resposta_http(200, "OK", conteudo)
    
    elif caminho == "/contato":
        conteudo = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Contato - Servidor HTTP Python</title>
</head>
<body>
    <h1>Contato</h1>
    <p>Para mais informações sobre programação com sockets em Python:</p>
    <ul>
        <li><a href="https://docs.python.org/3/library/socket.html">Documentação oficial do módulo socket</a></li>
        <li><a href="https://docs.python.org/3/howto/sockets.html">Python Socket Programming HOWTO</a></li>
    </ul>
    <p><a href="/">Voltar à página inicial</a></p>
</body>
</html>
"""
        return construir_resposta_http(200, "OK", conteudo)
    
    else:
        conteudo = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>404 - Não Encontrado</title>
</head>
<body>
    <h1>404 - Página Não Encontrada</h1>
    <p>A página <code>{caminho}</code> não existe neste servidor.</p>
    <p><a href="/">Voltar à página inicial</a></p>
</body>
</html>
"""
        return construir_resposta_http(404, "Not Found", conteudo)

def main():
    """Função principal do servidor HTTP."""
    # Criar socket TCP/IP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Permitir reutilização do endereço
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Vincular a localhost na porta 8080
    host = 'localhost'
    porta = 8080
    servidor.bind((host, porta))
    
    # Escutar por conexões
    servidor.listen(5)
    print(f'Servidor HTTP escutando em http://{host}:{porta}')
    print('Pressione Ctrl+C para encerrar\n')
    
    try:
        while True:
            # Aguardar conexão
            conexao, endereco = servidor.accept()
            print(f'Conexão recebida de {endereco}')
            
            try:
                # Receber requisição HTTP
                requisicao = conexao.recv(4096).decode('utf-8')
                
                if requisicao:
                    # Processar e enviar resposta
                    resposta = processar_requisicao(requisicao)
                    conexao.sendall(resposta.encode('utf-8'))
                    print('  Resposta enviada\n')
                
            except Exception as e:
                print(f'  Erro ao processar requisição: {e}\n')
            
            finally:
                # Fechar conexão com o cliente
                conexao.close()
    
    except KeyboardInterrupt:
        print('\n\nServidor encerrado pelo usuário')
    
    finally:
        servidor.close()
        print('Socket do servidor fechado')

if __name__ == '__main__':
    main()
