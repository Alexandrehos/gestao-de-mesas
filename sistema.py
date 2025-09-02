import json
import csv
import os

class ItemCardapio:
    def __init__(self, codigo, nome, descricao, valor):
        self.codigo = codigo
        self.nome = nome
        self.descricao = descricao
        self.valor = valor

class Cardapio:
    def __init__(self, arquivo='repositorio/cardapio.json'):
        self.arquivo = arquivo
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(self.arquivo), exist_ok=True)
        self.itens = self.carregar()

    def gerar_codigo_automatico(self):
        """Gera um código automático para o produto no formato sequencial: 1, 2, 3, etc."""
        if not self.itens:
            return "1"
        
        # Buscar todos os códigos que são números
        codigos_numericos = []
        for item in self.itens:
            if item.codigo.isdigit():
                codigos_numericos.append(int(item.codigo))
        
        if not codigos_numericos:
            return "1"
        
        # Retorna o próximo número sequencial
        proximo_numero = max(codigos_numericos) + 1
        return str(proximo_numero)

    def adicionar_item(self, item):
        self.itens.append(item)
        self.salvar()

    def adicionar_item_com_codigo_auto(self, nome, descricao, valor):
        """Adiciona um item com código gerado automaticamente"""
        codigo_auto = self.gerar_codigo_automatico()
        item = ItemCardapio(codigo_auto, nome, descricao, valor)
        self.adicionar_item(item)
        return codigo_auto

    def remover_item(self, codigo):
        self.itens = [item for item in self.itens if item.codigo != codigo]
        self.salvar()

    def listar_itens(self):
        return self.itens

    def salvar(self):
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump([item.__dict__ for item in self.itens], f, ensure_ascii=False, indent=2)

    def carregar(self):
        if not os.path.exists(self.arquivo):
            return []
        with open(self.arquivo, 'r', encoding='utf-8') as f:
            itens = json.load(f)
            return [ItemCardapio(**item) for item in itens]

class Mesa:
    def __init__(self, numero):
        self.numero = numero
        self.itens_consumidos = {}  # codigo: quantidade
        self.aberta = True

    def adicionar_item(self, codigo, quantidade=1):
        self.itens_consumidos[codigo] = self.itens_consumidos.get(codigo, 0) + quantidade

    def remover_item(self, codigo, quantidade=1):
        if codigo in self.itens_consumidos:
            self.itens_consumidos[codigo] -= quantidade
            if self.itens_consumidos[codigo] <= 0:
                del self.itens_consumidos[codigo]

    def listar_consumo(self):
        return self.itens_consumidos

    def fechar(self):
        self.aberta = False

class Restaurante:
    def __init__(self):
        self.cardapio = Cardapio()
        self.mesas = self.carregar_mesas()
        self.vendas = self.carregar_vendas()

    def abrir_mesa(self, numero):
        if numero in self.mesas and self.mesas[numero].aberta:
            print('Mesa já está aberta.')
            return
        self.mesas[numero] = Mesa(numero)
        self.salvar_mesas()

    def adicionar_item_mesa(self, numero, codigo, quantidade=1):
        if numero not in self.mesas or not self.mesas[numero].aberta:
            print('Mesa não está aberta.')
            return
        self.mesas[numero].adicionar_item(codigo, quantidade)
        self.salvar_mesas()

    def remover_item_mesa(self, numero, codigo, quantidade=1):
        if numero not in self.mesas or not self.mesas[numero].aberta:
            print('Mesa não está aberta.')
            return
        self.mesas[numero].remover_item(codigo, quantidade)
        self.salvar_mesas()

    def listar_consumo_mesa(self, numero):
        if numero not in self.mesas:
            print('Mesa não existe.')
            return {}
        return self.mesas[numero].listar_consumo()

    def fechar_mesa(self, numero):
        if numero not in self.mesas or not self.mesas[numero].aberta:
            print('Mesa não está aberta.')
            return
        self.mesas[numero].fechar()
        # Adiciona itens consumidos à venda total
        for codigo, quantidade in self.mesas[numero].itens_consumidos.items():
            self.vendas[codigo] = self.vendas.get(codigo, 0) + quantidade
        self.salvar_mesas()
        self.salvar_vendas()

    def salvar_mesas(self):
        mesas_data = {}
        for num, mesa in self.mesas.items():
            mesas_data[str(num)] = {
                'numero': mesa.numero,
                'itens_consumidos': mesa.itens_consumidos,
                'aberta': mesa.aberta
            }
        # Criar diretório se não existir
        os.makedirs('repositorio', exist_ok=True)
        with open('repositorio/mesas.json', 'w', encoding='utf-8') as f:
            json.dump(mesas_data, f, ensure_ascii=False, indent=2)

    def carregar_mesas(self):
        if not os.path.exists('repositorio/mesas.json'):
            return {}
        with open('repositorio/mesas.json', 'r', encoding='utf-8') as f:
            mesas_data = json.load(f)
            mesas = {}
            for num_str, dados in mesas_data.items():
                num = int(num_str)
                mesa = Mesa(num)
                mesa.itens_consumidos = dados.get('itens_consumidos', {})
                mesa.aberta = dados.get('aberta', True)
                mesas[num] = mesa
            return mesas

    def salvar_vendas(self):
        # Criar diretório se não existir
        os.makedirs('repositorio', exist_ok=True)
        with open('repositorio/vendas.json', 'w', encoding='utf-8') as f:
            json.dump(self.vendas, f, ensure_ascii=False, indent=2)

    def carregar_vendas(self):
        if not os.path.exists('repositorio/vendas.json'):
            return {}
        with open('repositorio/vendas.json', 'r', encoding='utf-8') as f:
            return json.load(f)

class Relatorio:
    @staticmethod
    def gerar_relatorio(vendas, cardapio):
        """Gera relatório de vendas em arquivo .txt e retorna o conteúdo para exibição"""
        from datetime import datetime
        
        # Criar diretório se não existir
        os.makedirs('relatorio', exist_ok=True)
        
        # Gerar nome do arquivo com data e hora
        agora = datetime.now()
        nome_arquivo = f"relatorio/relatorio_vendas_{agora.strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Preparar conteúdo do relatório
        linhas = []
        linhas.append("=" * 60)
        linhas.append("RELATÓRIO DE VENDAS - SISTEMA DE GESTÃO DE RESTAURANTE")
        linhas.append("=" * 60)
        linhas.append(f"Data/Hora: {agora.strftime('%d/%m/%Y às %H:%M:%S')}")
        linhas.append("=" * 60)
        linhas.append("")
        
        if not vendas:
            linhas.append("Nenhuma venda registrada.")
        else:
            linhas.append("ITENS VENDIDOS:")
            linhas.append("-" * 60)
            linhas.append(f"{'CÓDIGO':<10} {'NOME':<30} {'QTD':<10} {'VALOR UNIT.':<15}")
            linhas.append("-" * 60)
            
            total_itens = 0
            valor_total = 0.0
            
            for codigo, quantidade in vendas.items():
                item = next((i for i in cardapio.listar_itens() if i.codigo == codigo), None)
                if item:
                    nome = item.nome[:28]  # Limitar nome para caber na tabela
                    valor_unitario = item.valor
                    valor_item = quantidade * valor_unitario
                    valor_total += valor_item
                    
                    linhas.append(f"{codigo:<10} {nome:<30} {quantidade:<10} R$ {valor_unitario:<12.2f}")
                else:
                    linhas.append(f"{codigo:<10} {'Item não encontrado':<30} {quantidade:<10} {'N/A':<15}")
                
                total_itens += quantidade
            
            linhas.append("-" * 60)
            linhas.append(f"TOTAL DE ITENS VENDIDOS: {total_itens}")
            if valor_total > 0:
                linhas.append(f"VALOR TOTAL VENDIDO: R$ {valor_total:.2f}")
        
        linhas.append("")
        linhas.append("=" * 60)
        linhas.append("Relatório gerado automaticamente pelo sistema")
        linhas.append("=" * 60)
        
        # Salvar arquivo
        conteudo = "\n".join(linhas)
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        
        return conteudo, nome_arquivo
    
    @staticmethod
    def gerar_csv(vendas, cardapio, arquivo='relatorio.csv'):
        """Mantém método CSV para compatibilidade (será removido)"""
        with open(arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Código', 'Nome', 'Quantidade Vendida'])
            for codigo, quantidade in vendas.items():
                item = next((i for i in cardapio.listar_itens() if i.codigo == codigo), None)
                nome = item.nome if item else 'Desconhecido'
                writer.writerow([codigo, nome, quantidade])
