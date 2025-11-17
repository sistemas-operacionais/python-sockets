# python-sockets
Notas de aula sobre sockets em Python

## 📚 Tutorial Completo

Veja o [Tutorial de Sockets em Python para Iniciantes](TUTORIAL.md) com explicações detalhadas sobre:
- Conceitos básicos de sockets
- Arquitetura cliente-servidor
- Protocolo TCP
- Exemplos práticos comentados
- Boas práticas e dicas
- Próximos passos

## 🚀 Exemplos Práticos

### 1. Servidor e Cliente Básico
Exemplo simples de conexão e troca de mensagem única.

**Executar:**
```bash
# Terminal 1
python servidor_basico.py

# Terminal 2
python cliente_basico.py
```

### 2. Servidor e Cliente Echo
Servidor que devolve as mensagens recebidas (echo).

**Executar:**
```bash
# Terminal 1
python servidor_echo.py

# Terminal 2
python cliente_echo.py
```

### 3. Servidor e Cliente de Chat
Sistema de chat com múltiplos clientes usando threads.

**Executar:**
```bash
# Terminal 1
python servidor_chat.py

# Terminais 2, 3, 4... (múltiplos clientes)
python cliente_chat.py
```

## 📋 Estrutura do Repositório

```
python-sockets/
├── README.md              # Este arquivo
├── TUTORIAL.md            # Tutorial completo
├── servidor_basico.py     # Servidor TCP básico
├── cliente_basico.py      # Cliente TCP básico
├── servidor_echo.py       # Servidor echo
├── cliente_echo.py        # Cliente echo
├── servidor_chat.py       # Servidor de chat multi-cliente
└── cliente_chat.py        # Cliente de chat
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

## 🔧 Requisitos

- Python 3.6 ou superior
- Nenhuma biblioteca externa necessária (usa apenas biblioteca padrão)

## 📖 Recursos Adicionais

- [Documentação oficial do módulo socket](https://docs.python.org/3/library/socket.html)
- [Python Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)

## 📝 Licença

Este projeto está sob a licença GPL v3. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
