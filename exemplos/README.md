# Guia de Execução dos Exemplos

Este documento fornece instruções detalhadas sobre como executar cada exemplo de socket.

## Pré-requisitos

- Python 3.6 ou superior instalado
- Dois ou mais terminais abertos

## 1. Servidor e Cliente Básico

### Descrição
Exemplo mais simples: servidor aceita uma conexão, envia uma mensagem e encerra.

### Como Executar

**Terminal 1 (Servidor):**
```bash
python3 servidor_basico.py
```

Você verá:
```
Servidor escutando em localhost:5000
```

**Terminal 2 (Cliente):**
```bash
python3 cliente_basico.py
```

Você verá:
```
Conectado ao servidor em localhost:5000
Mensagem recebida: Bem-vindo ao servidor!
Conexão encerrada
```

Ambos os programas encerram automaticamente após a troca de mensagens.

---

## 2. Servidor e Cliente Echo

### Descrição
Servidor que devolve qualquer mensagem recebida. Permite múltiplas mensagens em uma única conexão.

### Como Executar

**Terminal 1 (Servidor):**
```bash
python3 servidor_echo.py
```

Você verá:
```
Servidor Echo escutando em localhost:5000

Aguardando conexão...
```

**Terminal 2 (Cliente):**
```bash
python3 cliente_echo.py
```

### Interação
1. Digite mensagens no cliente
2. O servidor responde com "Echo: [sua mensagem]"
3. Digite "sair" para encerrar o cliente

**Exemplo de uso:**
```
Conectado ao servidor Echo
Digite "sair" para encerrar a conexão

Digite uma mensagem: Olá
Resposta: Echo: Olá

Digite uma mensagem: Como vai?
Resposta: Echo: Como vai?

Digite uma mensagem: sair
Conexão encerrada
```

O servidor continua rodando e pode aceitar novas conexões.

---

## 3. Servidor e Cliente de Chat

### Descrição
Sistema de chat completo com suporte a múltiplos clientes simultâneos usando threads.

### Como Executar

**Terminal 1 (Servidor):**
```bash
python3 servidor_chat.py
```

Você verá:
```
Servidor de Chat iniciado em localhost:5000
```

**Terminal 2 (Primeiro Cliente):**
```bash
python3 cliente_chat.py
```

Escolha um apelido:
```
Escolha seu apelido: Alice
Conectado ao servidor!
```

**Terminal 3 (Segundo Cliente):**
```bash
python3 cliente_chat.py
```

Escolha outro apelido:
```
Escolha seu apelido: Bob
Conectado ao servidor!
Bob entrou no chat!
```

**Terminal 4 (Terceiro Cliente - Opcional):**
```bash
python3 cliente_chat.py
```

### Interação
- Todos os clientes veem quando alguém entra ou sai
- Mensagens enviadas por um cliente são vistas pelos outros
- Use Ctrl+C para sair

**Exemplo de conversa:**

Cliente Alice digita:
```
Olá a todos!
```

Cliente Bob vê:
```
Alice: Olá a todos!
```

Cliente Bob digita:
```
Oi Alice, tudo bem?
```

Cliente Alice vê:
```
Bob: Oi Alice, tudo bem?
```

---

## Solução de Problemas

### Erro: "Address already in use"

Se você ver este erro:
```
OSError: [Errno 98] Address already in use
```

**Soluções:**
1. Aguarde alguns segundos e tente novamente
2. Verifique se outro servidor está rodando na porta 5000:
   ```bash
   netstat -tulpn | grep 5000
   ```
3. Encerre o processo que está usando a porta
4. Os exemplos já incluem `SO_REUSEADDR` para minimizar este problema

### Erro: "Connection refused"

Se você ver:
```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Causas comuns:**
- O servidor não está rodando
- Você iniciou o cliente antes do servidor
- Firewall bloqueando a conexão

**Solução:**
1. Certifique-se de que o servidor está rodando primeiro
2. Verifique que está usando a porta correta (5000)

### Cliente não recebe mensagens no chat

**Verifique:**
- Se o apelido foi enviado corretamente
- Se o servidor está rodando
- Se há mensagens de erro no terminal do servidor

### Como encerrar os servidores

Use `Ctrl+C` no terminal onde o servidor está rodando.

---

## Modificando os Exemplos

### Mudando a Porta

Para usar uma porta diferente, edite os arquivos:

Em `servidor_*.py`:
```python
servidor.bind(('localhost', 5000))  # Mude 5000 para outra porta
```

Em `cliente_*.py`:
```python
cliente.connect(('localhost', 5000))  # Mude 5000 para a mesma porta
```

### Permitindo Conexões Remotas

Para aceitar conexões de outros computadores, mude `'localhost'` para `'0.0.0.0'`:

```python
servidor.bind(('0.0.0.0', 5000))
```

No cliente, use o IP do servidor:
```python
cliente.connect(('192.168.1.100', 5000))  # IP do servidor
```

⚠️ **Atenção:** Certifique-se de que seu firewall permite conexões na porta escolhida.

---

## Próximos Experimentos

1. **Modificar o Echo Server**: Faça-o converter mensagens para maiúsculas
2. **Adicionar Comandos**: Crie comandos especiais no chat (ex: /list para listar usuários)
3. **Log de Mensagens**: Salve o histórico do chat em um arquivo
4. **Interface Gráfica**: Use tkinter para criar uma GUI
5. **Criptografia**: Adicione criptografia básica às mensagens

---

## Recursos Adicionais

- Veja o [TUTORIAL.md](TUTORIAL.md) para explicações detalhadas
- Documentação Python: https://docs.python.org/3/library/socket.html
- Para dúvidas, abra uma issue no GitHub
