# Tutorial: Servidor e Cliente HTTP em Python

## 📖 Índice
1. [Introdução](#introdução)
2. [O que é HTTP?](#o-que-é-http)
3. [Como Executar os Exemplos](#como-executar-os-exemplos)
4. [Servidor HTTP](#servidor-http)
5. [Cliente HTTP](#cliente-http)
6. [Entendendo o Protocolo HTTP](#entendendo-o-protocolo-http)
7. [Código Detalhado](#código-detalhado)
8. [Experimentos e Modificações](#experimentos-e-modificações)
9. [Limitações e Próximos Passos](#limitações-e-próximos-passos)

## Introdução

Este tutorial apresenta exemplos básicos de servidor e cliente HTTP implementados usando sockets TCP em Python. O objetivo é educacional: entender como o protocolo HTTP funciona "por baixo dos panos".

**O que você vai aprender:**
- Como funciona o protocolo HTTP
- Como criar um servidor HTTP básico usando sockets
- Como fazer requisições HTTP usando sockets
- Estrutura de requisições e respostas HTTP

## O que é HTTP?

**HTTP (HyperText Transfer Protocol)** é o protocolo de comunicação usado na World Wide Web. Ele define como mensagens são formatadas e transmitidas entre clientes (navegadores) e servidores web.

### Características do HTTP:
- **Baseado em texto**: Requisições e respostas são texto legível
- **Cliente-Servidor**: Clientes fazem requisições, servidores enviam respostas
- **Stateless**: Cada requisição é independente (sem "memória")
- **TCP/IP**: HTTP usa TCP como protocolo de transporte

### Métodos HTTP Comuns:
- **GET**: Solicitar dados do servidor
- **POST**: Enviar dados para o servidor
- **PUT**: Atualizar dados no servidor
- **DELETE**: Remover dados do servidor

Nosso exemplo implementa apenas o método **GET**, o mais básico e comum.

## Como Executar os Exemplos

### Pré-requisitos
- Python 3.6 ou superior
- Dois terminais abertos
- Navegador web (opcional, mas recomendado)

### Passo 1: Iniciar o Servidor

**Terminal 1:**
```bash
cd exemplos/http
python3 servidor_http.py
```

Você verá:
```
Servidor HTTP escutando em http://localhost:8080
Pressione Ctrl+C para encerrar
```

### Passo 2: Testar com Navegador (Recomendado)

Abra seu navegador e acesse:
- http://localhost:8080/ - Página inicial
- http://localhost:8080/sobre - Página sobre
- http://localhost:8080/contato - Página de contato
- http://localhost:8080/teste - Página não encontrada (404)

### Passo 3: Testar com o Cliente Python

**Terminal 2:**
```bash
cd exemplos/http
python3 cliente_http.py
```

O cliente apresentará um menu interativo:
```
==================================================
Cliente HTTP Básico em Python
==================================================

Servidor padrão: localhost:8080
(Certifique-se de que o servidor está rodando)

Escolha uma opção:
1. Página inicial (/)
2. Sobre (/sobre)
3. Contato (/contato)
4. Página customizada
5. Sair

Opção:
```

Digite um número para fazer a requisição correspondente.

### Exemplo de Saída do Cliente

Ao escolher a opção 1 (Página inicial):
```
==================================================
Conectando a localhost:8080...
Conectado!

Enviando requisição:
----------------------------------------
GET / HTTP/1.1
Host: localhost:8080
User-Agent: Cliente-HTTP-Python/1.0
Accept: text/html
Connection: close

Resposta recebida:
========================================
Status: 200

Cabeçalhos:
  Content-Type: text/html; charset=utf-8
  Content-Length: 456
  Connection: close

Corpo da resposta:
----------------------------------------
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Servidor HTTP Python</title>
</head>
<body>
    <h1>Bem-vindo ao Servidor HTTP!</h1>
    ...
</body>
</html>
----------------------------------------
```

## Servidor HTTP

### Funcionalidades

O servidor implementa:
1. **Roteamento básico**: Diferentes respostas para diferentes URLs
2. **Geração de páginas HTML**: Conteúdo dinâmico
3. **Códigos de status HTTP**: 200 (OK), 404 (Not Found), 405 (Method Not Allowed)
4. **Cabeçalhos HTTP**: Content-Type, Content-Length, Connection

### Páginas Disponíveis

| URL | Descrição |
|-----|-----------|
| `/` ou `/index.html` | Página inicial com links |
| `/sobre` | Página sobre o servidor |
| `/contato` | Página com informações de contato |
| Qualquer outra | Página 404 (não encontrada) |

### Fluxo de Funcionamento

1. Servidor cria socket e escuta na porta 8080
2. Aguarda conexão de cliente
3. Recebe requisição HTTP
4. Analisa método e caminho
5. Gera resposta HTML apropriada
6. Envia resposta com cabeçalhos HTTP
7. Fecha conexão
8. Volta ao passo 2

## Cliente HTTP

### Funcionalidades

O cliente implementa:
1. **Construção de requisições HTTP GET**
2. **Envio de requisições ao servidor**
3. **Recebimento e parsing de respostas**
4. **Extração de código de status, cabeçalhos e corpo**
5. **Interface interativa por menu**

### Como Usar

1. Execute o cliente
2. Escolha uma opção do menu
3. Veja a requisição sendo enviada
4. Veja a resposta recebida
5. Repita ou saia (opção 5)

## Entendendo o Protocolo HTTP

### Estrutura de uma Requisição HTTP

```
GET /sobre HTTP/1.1
Host: localhost:8080
User-Agent: Cliente-HTTP-Python/1.0
Accept: text/html
Connection: close

```

**Componentes:**
1. **Linha de requisição**: `GET /sobre HTTP/1.1`
   - Método: `GET`
   - Caminho: `/sobre`
   - Versão: `HTTP/1.1`
2. **Cabeçalhos**: Pares chave-valor com metadados
3. **Linha em branco**: Indica fim dos cabeçalhos
4. **Corpo** (opcional): Dados enviados (não usado em GET)

### Estrutura de uma Resposta HTTP

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 456
Connection: close

<!DOCTYPE html>
<html>
...
</html>
```

**Componentes:**
1. **Linha de status**: `HTTP/1.1 200 OK`
   - Versão: `HTTP/1.1`
   - Código: `200`
   - Mensagem: `OK`
2. **Cabeçalhos**: Metadados da resposta
3. **Linha em branco**: Separador
4. **Corpo**: Conteúdo HTML

### Códigos de Status HTTP Comuns

| Código | Significado |
|--------|-------------|
| 200 | OK - Sucesso |
| 404 | Not Found - Página não encontrada |
| 405 | Method Not Allowed - Método não permitido |
| 500 | Internal Server Error - Erro no servidor |

## Código Detalhado

### Servidor: Construindo Resposta HTTP

```python
def construir_resposta_http(codigo, mensagem, conteudo):
    """Constrói uma resposta HTTP válida."""
    resposta = f"HTTP/1.1 {codigo} {mensagem}\r\n"
    resposta += "Content-Type: text/html; charset=utf-8\r\n"
    resposta += f"Content-Length: {len(conteudo.encode('utf-8'))}\r\n"
    resposta += "Connection: close\r\n"
    resposta += "\r\n"  # Linha em branco (importante!)
    resposta += conteudo
    return resposta
```

**Pontos importantes:**
- `\r\n` é o terminador de linha HTTP (CRLF)
- Linha em branco separa cabeçalhos do corpo
- Content-Length é o tamanho em bytes do corpo

### Servidor: Processando Requisição

```python
def processar_requisicao(requisicao):
    """Processa requisição e retorna resposta."""
    # Extrair primeira linha
    linhas = requisicao.split('\r\n')
    primeira_linha = linhas[0].split()
    
    metodo = primeira_linha[0]  # GET
    caminho = primeira_linha[1]  # /sobre
    
    # Roteamento
    if caminho == "/":
        return construir_resposta_http(200, "OK", html_home)
    elif caminho == "/sobre":
        return construir_resposta_http(200, "OK", html_sobre)
    else:
        return construir_resposta_http(404, "Not Found", html_404)
```

### Cliente: Fazendo Requisição

```python
def fazer_requisicao_http(host, porta, caminho='/'):
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
    resposta = cliente.recv(4096).decode('utf-8')
    
    cliente.close()
    return resposta
```

## Experimentos e Modificações

### 1. Adicionar Nova Página

No `servidor_http.py`, adicione um novo caso no roteamento:

```python
elif caminho == "/ajuda":
    conteudo = """
<!DOCTYPE html>
<html>
<body>
    <h1>Ajuda</h1>
    <p>Esta é uma página de ajuda!</p>
</body>
</html>
"""
    return construir_resposta_http(200, "OK", conteudo)
```

### 2. Mudar a Porta do Servidor

Em `servidor_http.py`, linha 170:
```python
porta = 9000  # Mude de 8080 para 9000
```

Em `cliente_http.py`, linha 116:
```python
porta = 9000  # Mude para a mesma porta
```

### 3. Adicionar Timestamp às Páginas

Importe datetime e adicione ao HTML:
```python
from datetime import datetime

conteudo = f"""
<html>
<body>
    <h1>Página Inicial</h1>
    <p>Gerada em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</body>
</html>
"""
```

### 4. Implementar Método POST

Desafio: Modificar o servidor para aceitar POST e processar dados.

### 5. Servir Arquivos Estáticos

Desafio: Ler arquivos HTML do disco e servi-los.

### 6. Adicionar CSS

Crie uma página com estilos:
```python
conteudo = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial; background: #f0f0f0; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <h1>Página Estilizada</h1>
</body>
</html>
"""
```

## Limitações e Próximos Passos

### Limitações deste Exemplo

Nosso servidor é **muito básico** e tem limitações:
- ❌ Suporta apenas GET (sem POST, PUT, DELETE)
- ❌ Não serve arquivos estáticos (imagens, CSS, JS)
- ❌ Não tem suporte a HTTPS (sem criptografia)
- ❌ Processa um cliente por vez (sem concorrência)
- ❌ Não tem cache, compressão ou otimizações
- ❌ Parsing de HTTP é simplificado

**Para produção, use bibliotecas estabelecidas!**

### Bibliotecas Python para HTTP

#### Para Servidores:
- **http.server**: Módulo built-in para servidores simples
- **Flask**: Framework web minimalista
- **Django**: Framework web completo
- **FastAPI**: Framework moderno e rápido

#### Para Clientes:
- **urllib**: Módulo built-in
- **requests**: Biblioteca popular e fácil de usar
- **httpx**: Cliente HTTP moderno com async

### Exemplo com http.server (Built-in)

Servidor em uma linha:
```python
python3 -m http.server 8080
```

### Exemplo com requests (Cliente)

```python
import requests

resposta = requests.get('http://localhost:8080/')
print(resposta.status_code)
print(resposta.text)
```

### Próximos Passos no Aprendizado

1. **HTTP/2 e HTTP/3**: Versões modernas do protocolo
2. **HTTPS/TLS**: Comunicação segura
3. **REST APIs**: Arquitetura para web services
4. **WebSockets**: Comunicação bidirecional em tempo real
5. **Cookies e Sessões**: Gerenciamento de estado
6. **Autenticação**: Basic, Bearer, OAuth
7. **CORS**: Cross-Origin Resource Sharing

## Recursos Adicionais

### Documentação:
- [RFC 2616 - HTTP/1.1](https://tools.ietf.org/html/rfc2616)
- [MDN Web Docs - HTTP](https://developer.mozilla.org/pt-BR/docs/Web/HTTP)
- [Python http.server](https://docs.python.org/3/library/http.server.html)
- [Python urllib](https://docs.python.org/3/library/urllib.html)

### Tutoriais:
- [HTTP Made Really Easy](https://www.jmarshall.com/easy/http/)
- [How HTTP Works](https://howhttps.works/)

### Ferramentas Úteis:
- **curl**: Cliente HTTP de linha de comando
- **Postman**: GUI para testar APIs
- **DevTools**: Ferramentas de desenvolvedor do navegador

## Solução de Problemas

### Erro: "Address already in use"

```
OSError: [Errno 98] Address already in use
```

**Solução:**
- Aguarde alguns segundos
- Ou mude a porta no servidor e cliente
- Ou encerre o processo usando a porta:
```bash
lsof -ti:8080 | xargs kill
```

### Erro: "Connection refused"

**Causas:**
- Servidor não está rodando
- Porta incorreta
- Firewall bloqueando

**Solução:**
- Certifique-se de iniciar o servidor primeiro
- Verifique se a porta está correta em ambos os programas

### Navegador não exibe a página

**Verifique:**
- URL correta: `http://localhost:8080/`
- Servidor está rodando
- Não está usando HTTPS (use HTTP)

### Cliente não recebe resposta completa

O servidor fecha a conexão, então use um loop:
```python
resposta = b''
while True:
    dados = cliente.recv(4096)
    if not dados:
        break
    resposta += dados
```

## Conclusão

Parabéns! Você implementou um servidor e cliente HTTP básico usando apenas sockets TCP. Agora você entende:

✅ Como o protocolo HTTP funciona fundamentalmente  
✅ Estrutura de requisições e respostas HTTP  
✅ Como construir um servidor web simples  
✅ Como fazer requisições HTTP manualmente  
✅ A base para trabalhar com web services e APIs  

Este conhecimento é fundamental para entender frameworks web modernos e trabalhar com APIs REST!

---

**Voltar para:** [Exemplos principais](../README.md) | [Tutorial completo](../../TUTORIAL.md) | [README principal](../../README.md)
