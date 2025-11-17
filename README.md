# python-sockets
Notas de aula sobre sockets em Python

## 📚 Documentação

### [Tutorial Completo](TUTORIAL.md)
Veja o [Tutorial de Sockets em Python para Iniciantes](TUTORIAL.md) com explicações detalhadas sobre:
- Conceitos básicos de sockets
- Arquitetura cliente-servidor
- Protocolo TCP
- Exemplos práticos comentados
- Boas práticas e dicas
- Próximos passos

### [Guia de Execução](exemplos/README.md)
Consulte o [Guia de Execução dos Exemplos](exemplos/README.md) para:
- Instruções passo a passo de cada exemplo
- Solução de problemas comuns
- Dicas de modificação e experimentos

## 🚀 Exemplos Práticos

### 1. Servidor e Cliente Básico
Exemplo simples de conexão e troca de mensagem única.

**Executar:**
```bash
# Terminal 1
python exemplos/servidor_basico.py

# Terminal 2
python exemplos/cliente_basico.py
```

### 2. Servidor e Cliente Echo
Servidor que devolve as mensagens recebidas (echo).

**Executar:**
```bash
# Terminal 1
python exemplos/servidor_echo.py

# Terminal 2
python exemplos/cliente_echo.py
```

### 3. Servidor e Cliente de Chat
Sistema de chat com múltiplos clientes usando threads.

**Executar:**
```bash
# Terminal 1
python exemplos/servidor_chat.py

# Terminais 2, 3, 4... (múltiplos clientes)
python exemplos/cliente_chat.py
```

### 4. Servidor e Cliente HTTP
Implementação básica do protocolo HTTP com servidor web e cliente.

**Executar:**
```bash
# Terminal 1
python exemplos/http/servidor_http.py

# Terminal 2 (ou use navegador em http://localhost:8080)
python exemplos/http/cliente_http.py
```

**Tutorial completo:** Ver [exemplos/http/README.md](exemplos/http/README.md)

## 📋 Estrutura do Repositório

```
python-sockets/
├── README.md              # Este arquivo
├── TUTORIAL.md            # Tutorial completo
└── exemplos/              # Exemplos práticos
    ├── README.md          # Guia de execução dos exemplos
    ├── servidor_basico.py # Servidor TCP básico
    ├── cliente_basico.py  # Cliente TCP básico
    ├── servidor_echo.py   # Servidor echo
    ├── cliente_echo.py    # Cliente echo
    ├── servidor_chat.py   # Servidor de chat multi-cliente
    ├── cliente_chat.py    # Cliente de chat
    └── http/              # Exemplos HTTP
        ├── README.md      # Tutorial de HTTP
        ├── servidor_http.py # Servidor HTTP básico
        └── cliente_http.py  # Cliente HTTP
```

## 🎓 Conceitos Abordados

- ✅ Criação de sockets TCP
- ✅ Conexão cliente-servidor
- ✅ Envio e recebimento de dados
- ✅ Codificação/decodificação de strings
- ✅ Loops de comunicação
- ✅ Threading para múltiplos clientes
- ✅ Broadcast de mensagens
- ✅ Tratamento de desconexões
- ✅ Protocolo HTTP (requisições e respostas)
- ✅ Servidor web básico
- ✅ Cliente HTTP customizado

## 🔧 Requisitos

- Python 3.6 ou superior
- Nenhuma biblioteca externa necessária (usa apenas biblioteca padrão)

## 📖 Recursos Adicionais

- [Documentação oficial do módulo socket](https://docs.python.org/3/library/socket.html)
- [Python Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)

## 📝 Licença

Este projeto está sob a licença GPL v3. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
