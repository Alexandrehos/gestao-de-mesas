# Sistema de Gestão de Restaurante

Sistema desenvolvido em Python para gestão de restaurantes, permitindo o controle de cardápio, mesas e vendas através de uma interface de linha de comando.

## Funcionalidades

### Editar Cardápio
- Adicionar novos itens ao cardápio (com código automático ou manual)
- Remover itens existentes
- Editar informações de itens (nome, descrição, valor)
- Listar todos os itens do cardápio com detalhes completos

#### Geração Automática de Códigos
O sistema pode gerar códigos automaticamente no formato sequencial: 1, 2, 3, 4, etc. Isso garante que não haverá códigos duplicados e facilita o cadastro de novos produtos.

#### Entrada de Valores Flexível
O sistema aceita valores monetários tanto com vírgula quanto com ponto como separador decimal:
- Formato brasileiro: 10,50
- Formato internacional: 10.50
- Validação automática para valores positivos

### Gestão de Mesas
- Abrir novas mesas
- Adicionar itens do cardápio às mesas
- Remover itens das mesas
- Visualizar itens consumidos por mesa com valores
- Fechar mesas com resumo completo da conta

### Relatórios
- Gerar relatório de vendas detalhado
- Exibição no terminal com formatação
- Salvamento automático em arquivo .txt na pasta `relatorio/`
- Nome de arquivo com data e hora para histórico

## Estrutura do Projeto

```
Carin/
├── main.py                    # Interface do usuário e menus
├── sistema.py                 # Classes principais do sistema
├── repositorio/
│   ├── cardapio.json         # Dados do cardápio (gerado automaticamente)
│   ├── mesas.json            # Dados das mesas (gerado automaticamente)
│   └── vendas.json           # Dados de vendas (gerado automaticamente)
└── relatorio/
    └── relatorio_vendas_*.txt # Relatórios de vendas com timestamp
```

## Classes

### ItemCardapio
Representa um item do cardápio com:
- Código único
- Nome
- Descrição
- Valor

### Cardapio
Gerencia a coleção de itens do cardápio:
- Adicionar/remover itens
- Persistência em arquivo JSON
- Listagem de itens

### Mesa
Representa uma mesa do restaurante:
- Número da mesa
- Itens consumidos (código: quantidade)
- Status (aberta/fechada)

### Restaurante
Classe principal que coordena:
- Cardápio
- Mesas ativas
- Vendas totais
- Persistência de dados

### Relatorio
Gera relatórios em formato CSV

## Como Usar

1. Execute o arquivo principal:
```bash
python main.py
```

2. Use o menu principal para navegar:
   - **Editar Cardápio**: Gerenciar itens do cardápio
   - **Mesas**: Gerenciar mesas e pedidos
   - **Gerar relatório**: Criar relatório de vendas
   - **Sair**: Encerrar o sistema

## Persistência de Dados

O sistema salva automaticamente na pasta `repositorio/`:
- **repositorio/cardapio.json**: Todos os itens do cardápio
- **repositorio/mesas.json**: Estado atual das mesas
- **repositorio/vendas.json**: Total de itens vendidos

Os relatórios são salvos na pasta `relatorio/`:
- **relatorio/relatorio_vendas_YYYYMMDD_HHMMSS.txt**: Relatórios detalhados com timestamp

## Requisitos

- Python 3.6 ou superior
- Módulos padrão: `json`, `csv`, `os`

## Características Técnicas

- **Paradigma**: Programação Orientada a Objetos (POO)
- **Interface**: Linha de comando com menus interativos
- **Persistência**: Arquivos JSON para dados, CSV para relatórios
- **Tratamento de erros**: Validação de entrada e tratamento de exceções
- **UX**: Limpeza automática do terminal entre operações
