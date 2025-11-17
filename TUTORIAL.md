# Tutorial de Sockets em Python para Iniciantes

## Índice
1. [O que são Sockets?](#o-que-são-sockets)
2. [Conceitos Básicos](#conceitos-básicos)
3. [Servidor Básico](#servidor-básico)
4. [Cliente Básico](#cliente-básico)
5. [Servidor Echo](#servidor-echo)
6. [Cliente Echo](#cliente-echo)
7. [Servidor de Chat](#servidor-de-chat)
8. [Cliente de Chat](#cliente-de-chat)
9. [Servidor e Cliente HTTP](#servidor-e-cliente-http)
10. [Dicas e Boas Práticas](#dicas-e-boas-práticas)
11. [Próximos Passos](#próximos-passos)

## O que são Sockets?

Sockets são pontos finais de comunicação que permitem que dois programas troquem dados através de uma rede. Pense neles como "tomadas" de rede onde você pode conectar dois programas para que eles conversem entre si.

### Tipos de Sockets

- **TCP (Transmission Control Protocol)**: Garante entrega confiável de dados, com controle de fluxo e ordenação
- **UDP (User Datagram Protocol)**: Mais rápido, mas não garante entrega ou ordem dos pacotes

Neste tutorial, vamos focar em **TCP**, que é o mais comum para aplicações que precisam de confiabilidade.

## Conceitos Básicos

### Arquitetura Cliente-Servidor

- **Servidor**: Programa que fica "escutando" por conexões em um endereço e porta específicos
- **Cliente**: Programa que se conecta ao servidor para enviar/receber dados

### Componentes Importantes

1. **Endereço IP**: Identifica o computador na rede (ex: `127.0.0.1` para localhost)
2. **Porta**: Número que identifica um serviço específico (ex: `8080`, `5000`)
3. **Socket**: Objeto Python que representa a conexão

### Fluxo de Comunicação TCP

**Servidor:**
```
1. Criar socket
2. Bind (vincular) a um endereço e porta
3. Listen (escutar) por conexões
4. Accept (aceitar) conexões de clientes
5. Enviar/Receber dados
6. Fechar conexão
```

**Cliente:**
```
1. Criar socket
2. Connect (conectar) ao servidor
3. Enviar/Receber dados
4. Fechar conexão
```

## Servidor Básico

Vamos começar com um servidor simples que aceita uma conexão e envia uma mensagem de boas-vindas.

```python
import socket

# Criar um socket TCP/IP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
```

### Explicação do Código:

- `socket.AF_INET`: Família de endereços IPv4
- `socket.SOCK_STREAM`: Tipo de socket TCP
- `bind()`: Associa o socket a um endereço específico
- `listen()`: Coloca o servidor em modo de escuta
- `accept()`: Bloqueia até que um cliente se conecte
- `encode('utf-8')`: Converte string para bytes

## Cliente Básico

Cliente que se conecta ao servidor e recebe a mensagem:

```python
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
```

### Explicação do Código:

- `connect()`: Conecta ao endereço do servidor
- `recv(1024)`: Recebe até 1024 bytes de dados
- `decode('utf-8')`: Converte bytes para string

### Como Executar:

1. Abra dois terminais
2. No primeiro, execute: `python servidor_basico.py`
3. No segundo, execute: `python cliente_basico.py`

## Servidor Echo

Um servidor mais útil que devolve qualquer mensagem que recebe:

```python
import socket

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
```

### Novidades no Código:

- Loop infinito para aceitar múltiplas conexões
- Loop interno para trocar múltiplas mensagens
- Tratamento de desconexão (`if not dados`)
- Bloco `try-finally` para garantir fechamento da conexão

## Cliente Echo

Cliente que envia mensagens e recebe respostas:

```python
import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('localhost', 5000))
print('Conectado ao servidor Echo')

try:
    while True:
        # Ler mensagem do usuário
        mensagem = input('Digite uma mensagem (ou "sair" para terminar): ')
        
        if mensagem.lower() == 'sair':
            break
            
        # Enviar mensagem
        cliente.send(mensagem.encode('utf-8'))
        
        # Receber resposta
        resposta = cliente.recv(1024)
        print(f'Resposta: {resposta.decode("utf-8")}')
        
finally:
    cliente.close()
    print('Conexão encerrada')
```

### Novidades no Código:

- Loop para enviar múltiplas mensagens
- Input do usuário
- Verificação para sair do loop

## Servidor de Chat

Um servidor mais avançado que suporta múltiplos clientes simultaneamente:

```python
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
```

### Novidades no Código:

- **Threading**: Permite múltiplos clientes simultâneos
- **Broadcast**: Envia mensagens para todos os clientes
- **Gerenciamento de clientes**: Lista de conexões ativas
- **Apelidos**: Identificação dos usuários

## Cliente de Chat

Cliente interativo que permite enviar e receber mensagens:

```python
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
```

### Novidades no Código:

- **Duas threads**: Uma para enviar, outra para receber
- **Comunicação bidirecional simultânea**: Pode enviar e receber ao mesmo tempo
- **Sistema de apelidos**: Identificação dos usuários

### Como Executar o Chat:

1. Execute o servidor: `python servidor_chat.py`
2. Em vários terminais, execute: `python cliente_chat.py`
3. Escolha um apelido para cada cliente
4. Comece a conversar!

## Servidor e Cliente HTTP

### O que é HTTP?

**HTTP (HyperText Transfer Protocol)** é o protocolo que alimenta a World Wide Web. Ele define como navegadores e servidores se comunicam. HTTP é um protocolo **baseado em texto** construído sobre TCP.

### Por que HTTP é Importante?

- Usado em toda a web (navegadores, APIs, web services)
- Base para REST APIs e web services modernos
- Protocolo simples de entender e depurar
- Fundamento para frameworks web (Flask, Django, etc.)

### Estrutura Básica do HTTP

**Requisição HTTP:**
```
GET /pagina HTTP/1.1
Host: localhost:8080
User-Agent: Navegador/1.0

```

**Resposta HTTP:**
```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 123

<html><body>Olá!</body></html>
```

### Nosso Exemplo

Criamos um **servidor HTTP básico** que:
- Aceita requisições GET
- Serve páginas HTML
- Implementa roteamento simples
- Retorna códigos de status (200, 404, 405)

E um **cliente HTTP** que:
- Constrói requisições HTTP GET
- Envia requisições ao servidor
- Faz parsing das respostas
- Exibe status, cabeçalhos e corpo

### Como Executar

**Terminal 1 (Servidor):**
```bash
python exemplos/http/servidor_http.py
```

**Terminal 2 (Cliente):**
```bash
python exemplos/http/cliente_http.py
```

**Ou use um navegador:**
Abra http://localhost:8080/ no seu navegador!

### Código Simplificado

**Servidor HTTP:**
```python
import socket

def construir_resposta_http(codigo, mensagem, conteudo):
    """Constrói resposta HTTP válida."""
    resposta = f"HTTP/1.1 {codigo} {mensagem}\r\n"
    resposta += "Content-Type: text/html; charset=utf-8\r\n"
    resposta += f"Content-Length: {len(conteudo.encode('utf-8'))}\r\n"
    resposta += "Connection: close\r\n"
    resposta += "\r\n"
    resposta += conteudo
    return resposta

# Criar e configurar servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(('localhost', 8080))
servidor.listen(5)

while True:
    conexao, endereco = servidor.accept()
    requisicao = conexao.recv(4096).decode('utf-8')
    
    # Processar requisição e enviar resposta
    if '/' in requisicao:
        html = '<h1>Bem-vindo!</h1>'
        resposta = construir_resposta_http(200, "OK", html)
    else:
        html = '<h1>404 - Não encontrado</h1>'
        resposta = construir_resposta_http(404, "Not Found", html)
    
    conexao.sendall(resposta.encode('utf-8'))
    conexao.close()
```

**Cliente HTTP:**
```python
import socket

def fazer_requisicao(host, porta, caminho='/'):
    """Faz requisição HTTP GET."""
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, porta))
    
    # Construir requisição
    requisicao = f"GET {caminho} HTTP/1.1\r\n"
    requisicao += f"Host: {host}:{porta}\r\n"
    requisicao += "Connection: close\r\n"
    requisicao += "\r\n"
    
    # Enviar e receber
    cliente.sendall(requisicao.encode('utf-8'))
    resposta = b''
    while True:
        dados = cliente.recv(4096)
        if not dados:
            break
        resposta += dados
    
    cliente.close()
    return resposta.decode('utf-8')

# Usar
resposta = fazer_requisicao('localhost', 8080, '/')
print(resposta)
```

### Conceitos Importantes

**Códigos de Status HTTP:**
- **200 OK**: Sucesso
- **404 Not Found**: Página não encontrada
- **405 Method Not Allowed**: Método não suportado
- **500 Internal Server Error**: Erro no servidor

**Cabeçalhos HTTP:**
- `Content-Type`: Tipo do conteúdo (text/html, application/json)
- `Content-Length`: Tamanho do corpo em bytes
- `Connection`: close ou keep-alive
- `Host`: Nome do servidor

**Métodos HTTP:**
- **GET**: Buscar dados
- **POST**: Enviar dados
- **PUT**: Atualizar dados
- **DELETE**: Remover dados

Nosso exemplo implementa apenas GET, o mais básico.

### Tutorial Completo

Para um tutorial detalhado sobre HTTP com muitos exemplos e explicações:

👉 **Ver [exemplos/http/README.md](exemplos/http/README.md)**

Este tutorial inclui:
- Explicações detalhadas do protocolo HTTP
- Como funciona cada parte do código
- Experimentos e modificações sugeridas
- Comparação com bibliotecas de alto nível
- Próximos passos no aprendizado

## Dicas e Boas Práticas

### 1. Sempre Feche Conexões

Use `try-finally` ou `with` para garantir fechamento:

```python
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Seu código aqui
    pass
# Socket é fechado automaticamente
```

### 2. Tratamento de Erros

```python
try:
    cliente.connect(('localhost', 5000))
except ConnectionRefusedError:
    print('Não foi possível conectar ao servidor')
except socket.timeout:
    print('Tempo limite de conexão excedido')
```

### 3. Configurar Timeout

```python
cliente.settimeout(5.0)  # 5 segundos
```

### 4. Reutilizar Endereço

```python
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

### 5. Buffer Size

- Use tamanhos de buffer adequados (1024, 4096, 8192 bytes)
- Para mensagens grandes, use loop de recebimento

### 6. Encoding

- Sempre especifique encoding ao converter strings/bytes
- UTF-8 é recomendado: `mensagem.encode('utf-8')`

### 7. Threads vs Async

Para muitos clientes:
- **Threads**: Simples, mas limitado em escala
- **asyncio**: Melhor para alta concorrência

## Próximos Passos

### Conceitos Avançados:

1. **Socket UDP**: Comunicação sem conexão
2. **asyncio**: Programação assíncrona
3. **SSL/TLS**: Conexões seguras (HTTPS)
4. **Protocolos**: FTP, SMTP, WebSocket
5. **Serialização**: JSON, pickle, protobuf
6. **Multiplexing**: select, poll, epoll
7. **HTTP/2 e HTTP/3**: Versões modernas do HTTP

### Projetos Práticos:

- Sistema de transferência de arquivos
- ✅ **Servidor HTTP simples** (já implementado em `exemplos/http/`)
- REST API básica
- Jogo multiplayer simples
- Sistema de notificações
- Proxy/Tunnel
- Web scraper customizado

### Bibliotecas de Alto Nível:

- **requests**: Cliente HTTP simplificado
- **Flask/Django**: Frameworks web
- **Twisted**: Framework de rede
- **asyncio**: I/O assíncrono

## Recursos Adicionais

- [Documentação oficial do módulo socket](https://docs.python.org/3/library/socket.html)
- [Python Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)
- [Real Python - Socket Programming](https://realpython.com/python-sockets/)

## Solução de Problemas Comuns

### "Address already in use"
```python
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

### "Connection refused"
- Verifique se o servidor está rodando
- Confirme endereço IP e porta corretos
- Verifique firewall

### Dados incompletos
```python
def receber_completo(socket, tamanho):
    dados = b''
    while len(dados) < tamanho:
        pacote = socket.recv(tamanho - len(dados))
        if not pacote:
            return None
        dados += pacote
    return dados
```

### "Broken pipe"
- Cliente desconectou antes do servidor terminar de enviar
- Use tratamento de exceções apropriado

---

## Conclusão

Sockets são a base da comunicação em rede. Com os exemplos deste tutorial, você aprendeu:

✅ Criar servidores e clientes TCP  
✅ Trocar mensagens entre programas  
✅ Trabalhar com múltiplos clientes  
✅ Implementar um chat básico  
✅ Boas práticas de programação com sockets  

Continue praticando e explorando os conceitos avançados. Boa sorte com seus projetos de rede!
