from sistema import Restaurante, Relatorio, ItemCardapio
import os

def limpar_terminal():
    """Limpa o terminal baseado no sistema operacional"""
    os.system('cls' if os.name == 'nt' else 'clear')

def converter_valor(valor_str):
    """Converte string de valor aceitando tanto vírgula quanto ponto como separador decimal"""
    try:
        # Remove espaços em branco
        valor_str = valor_str.strip()
        
        # Substitui vírgula por ponto
        valor_str = valor_str.replace(',', '.')
        
        # Converte para float
        valor = float(valor_str)
        
        # Verifica se o valor é positivo
        if valor < 0:
            raise ValueError("Valor deve ser positivo")
            
        return valor
    except ValueError:
        raise ValueError("Formato de valor inválido. Use números com . ou , (ex: 10.50 ou 10,50)")

def menu_cardapio(restaurante):
    """Submenu para edição de cardápio"""
    while True:
        limpar_terminal()
        print("\n--- Editar Cardápio ---")
        print("1. Adicionar item")
        print("2. Remover item")
        print("3. Editar item")
        print("4. Listar cardápio")
        print("5. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            limpar_terminal()
            print("--- Adicionar Item ao Cardápio ---")
            print("1. Gerar código automaticamente")
            print("2. Inserir código manualmente")
            opcao_codigo = input("Escolha uma opção: ")
            
            nome = input("Nome do item: ")
            descricao = input("Descrição: ")
            try:
                valor_input = input("Valor (use . ou , para decimais): R$ ")
                valor = converter_valor(valor_input)
                
                if opcao_codigo == '1':
                    # Usar código automático
                    codigo_gerado = restaurante.cardapio.adicionar_item_com_codigo_auto(nome, descricao, valor)
                    print(f"Item adicionado com sucesso! Código gerado: {codigo_gerado}")
                elif opcao_codigo == '2':
                    # Usar código manual
                    codigo = input("Código do item: ")
                    # Verificar se código já existe
                    codigos_existentes = [item.codigo for item in restaurante.cardapio.listar_itens()]
                    if codigo in codigos_existentes:
                        print("Erro: Código já existe!")
                    else:
                        restaurante.cardapio.adicionar_item(ItemCardapio(codigo, nome, descricao, valor))
                        print("Item adicionado com sucesso!")
                else:
                    print("Opção inválida!")
                    
                input("Pressione Enter para continuar...")
            except ValueError as e:
                print(f"Erro: {e}")
                input("Pressione Enter para continuar...")
        
        elif opcao == '2':
            limpar_terminal()
            codigo = input("Código do item a remover: ")
            restaurante.cardapio.remover_item(codigo)
            print("Item removido!")
            input("Pressione Enter para continuar...")
        
        elif opcao == '3':
            limpar_terminal()
            codigo = input("Código do item a editar: ")
            # Buscar item existente
            item_existente = None
            for item in restaurante.cardapio.listar_itens():
                if item.codigo == codigo:
                    item_existente = item
                    break
            
            if item_existente:
                print(f"Item atual: {item_existente.nome} - R$ {item_existente.valor:.2f}")
                nome = input(f"Novo nome (atual: {item_existente.nome}): ") or item_existente.nome
                descricao = input(f"Nova descrição (atual: {item_existente.descricao}): ") or item_existente.descricao
                valor_input = input(f"Novo valor (atual: R$ {item_existente.valor:.2f}): ")
                
                try:
                    if valor_input:
                        valor = converter_valor(valor_input)
                    else:
                        valor = item_existente.valor
                    
                    # Remove o item antigo e adiciona o novo
                    restaurante.cardapio.remover_item(codigo)
                    restaurante.cardapio.adicionar_item(ItemCardapio(codigo, nome, descricao, valor))
                    print("Item editado com sucesso!")
                    input("Pressione Enter para continuar...")
                except ValueError as e:
                    print(f"Erro: {e}")
                    input("Pressione Enter para continuar...")
            else:
                print("Item não encontrado!")
                input("Pressione Enter para continuar...")
        
        elif opcao == '4':
            limpar_terminal()
            itens = restaurante.cardapio.listar_itens()
            if itens:
                print("\n--- CARDÁPIO ---")
                print("-" * 80)
                for item in itens:
                    print(f"Código: {item.codigo}")
                    print(f"Nome: {item.nome}")
                    print(f"Descrição: {item.descricao}")
                    print(f"Valor: R$ {item.valor:.2f}")
                    print("-" * 80)
            else:
                print("Cardápio vazio!")
            input("Pressione Enter para continuar...")
        
        elif opcao == '5':
            break
        
        else:
            print("Opção inválida!")
            input("Pressione Enter para continuar...")

def submenu_mesa_especifica(restaurante, numero_mesa):
    """Submenu para operações em uma mesa específica"""
    while True:
        limpar_terminal()
        print(f"\n--- Mesa {numero_mesa} ---")
        print("1. Adicionar item")
        print("2. Remover item")
        print("3. Listar itens")
        print("4. Fechar mesa")
        print("5. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            limpar_terminal()
            print(f"--- Adicionar Item à Mesa {numero_mesa} ---")
            # Mostrar cardápio disponível
            itens = restaurante.cardapio.listar_itens()
            if itens:
                print("\n--- Cardápio Disponível ---")
                for item in itens:
                    print(f"{item.codigo} - {item.nome} - R$ {item.valor:.2f}")
                print("-" * 50)
            
            try:
                codigo = input("Código do item: ")
                quantidade = int(input("Quantidade: "))
                restaurante.adicionar_item_mesa(numero_mesa, codigo, quantidade)
                print("Item adicionado à mesa!")
                input("Pressione Enter para continuar...")
            except ValueError:
                print("Dados inválidos!")
                input("Pressione Enter para continuar...")
        
        elif opcao == '2':
            limpar_terminal()
            print(f"--- Remover Item da Mesa {numero_mesa} ---")
            try:
                codigo = input("Código do item: ")
                quantidade = int(input("Quantidade: "))
                restaurante.remover_item_mesa(numero_mesa, codigo, quantidade)
                print("Item removido da mesa!")
                input("Pressione Enter para continuar...")
            except ValueError:
                print("Dados inválidos!")
                input("Pressione Enter para continuar...")
        
        elif opcao == '3':
            limpar_terminal()
            print(f"--- Itens Consumidos - Mesa {numero_mesa} ---")
            consumo = restaurante.listar_consumo_mesa(numero_mesa)
            if consumo:
                total_mesa = 0
                for codigo, quantidade in consumo.items():
                    item = next((i for i in restaurante.cardapio.listar_itens() if i.codigo == codigo), None)
                    if item:
                        valor_total_item = quantidade * item.valor
                        total_mesa += valor_total_item
                        print(f"{codigo} - {item.nome}: {quantidade} x R$ {item.valor:.2f} = R$ {valor_total_item:.2f}")
                    else:
                        print(f"{codigo} - Item não encontrado: {quantidade} unidades")
                print("-" * 50)
                print(f"TOTAL DA MESA: R$ {total_mesa:.2f}")
            else:
                print("Mesa não possui itens consumidos.")
            input("Pressione Enter para continuar...")
        
        elif opcao == '4':
            limpar_terminal()
            print(f"--- Fechar Mesa {numero_mesa} ---")
            # Mostrar resumo antes de fechar
            consumo = restaurante.listar_consumo_mesa(numero_mesa)
            if consumo:
                print(f"\n--- Resumo da Mesa {numero_mesa} ---")
                total_mesa = 0
                for codigo, quantidade in consumo.items():
                    item = next((i for i in restaurante.cardapio.listar_itens() if i.codigo == codigo), None)
                    if item:
                        valor_total_item = quantidade * item.valor
                        total_mesa += valor_total_item
                        print(f"{item.nome}: {quantidade} x R$ {item.valor:.2f} = R$ {valor_total_item:.2f}")
                print(f"\nTOTAL: R$ {total_mesa:.2f}")
                
                confirmar = input("Confirmar fechamento da mesa? (s/n): ")
                if confirmar.lower() == 's':
                    restaurante.fechar_mesa(numero_mesa)
                    print(f"Mesa {numero_mesa} fechada com sucesso!")
                    input("Pressione Enter para continuar...")
                    break  # Sair do submenu após fechar a mesa
                else:
                    print("Fechamento cancelado.")
                    input("Pressione Enter para continuar...")
            else:
                print("Mesa não possui itens para fechar.")
                input("Pressione Enter para continuar...")
        
        elif opcao == '5':
            break
        
        else:
            print("Opção inválida!")
            input("Pressione Enter para continuar...")

def menu_mesas(restaurante):
    """Submenu para gestão de mesas"""
    while True:
        limpar_terminal()
        print("\n--- Mesas ---")
        print("1. Abrir mesa")
        print("2. Selecionar mesa")
        print("3. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            limpar_terminal()
            try:
                numero = int(input("Número da mesa: "))
                restaurante.abrir_mesa(numero)
                print(f"Mesa {numero} aberta!")
                input("Pressione Enter para continuar...")
            except ValueError:
                print("Número da mesa inválido!")
                input("Pressione Enter para continuar...")
        
        elif opcao == '2':
            limpar_terminal()
            print("--- Selecionar Mesa ---")
            # Listar mesas abertas
            mesas_abertas = [num for num, mesa in restaurante.mesas.items() if mesa.aberta]
            if mesas_abertas:
                print("Mesas abertas:")
                for num in mesas_abertas:
                    print(f"Mesa {num}")
                print("-" * 30)
                try:
                    numero = int(input("Número da mesa: "))
                    if numero in mesas_abertas:
                        submenu_mesa_especifica(restaurante, numero)
                    else:
                        print("Mesa não está aberta ou não existe!")
                        input("Pressione Enter para continuar...")
                except ValueError:
                    print("Número da mesa inválido!")
                    input("Pressione Enter para continuar...")
            else:
                print("Nenhuma mesa aberta!")
                input("Pressione Enter para continuar...")
        
        elif opcao == '3':
            break
        
        else:
            print("Opção inválida!")
            input("Pressione Enter para continuar...")

def menu_principal():
    """Menu principal do sistema"""
    restaurante = Restaurante()
    
    while True:
        limpar_terminal()
        print("\n=== Sistema de Gestão de Restaurante ===")
        print("1. Editar Cardápio")
        print("2. Mesas")
        print("3. Gerar relatório")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_cardapio(restaurante)
        
        elif opcao == '2':
            menu_mesas(restaurante)
        
        elif opcao == '3':
            limpar_terminal()
            print("--- Gerando Relatório de Vendas ---")
            conteudo_relatorio, nome_arquivo = Relatorio.gerar_relatorio(restaurante.vendas, restaurante.cardapio)
            
            # Exibir relatório no terminal
            print(conteudo_relatorio)
            print(f"\nRelatório salvo em: {nome_arquivo}")
            input("Pressione Enter para continuar...")
        
        elif opcao == '4':
            print("Saindo do sistema...")
            break
        
        else:
            print("Opção inválida!")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    menu_principal()