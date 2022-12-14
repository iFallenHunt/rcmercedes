import re
import sqlite3
import tkinter as tk
import tkinter.ttk as tkk
from tkinter import messagebox


class ConectarDB:
    def __init__(self):
        self.con = sqlite3.connect('db.sqlite3')
        self.cur = self.con.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        try:
            self.cur.execute('''CREATE TABLE IF NOT EXISTS Recall (
                VIN TEXT,
                MODEL TEXT,
                DATA TEXT,                
                PRODUTO TEXT,
                A_FABRICACAO TEXT,
                CODCONTA TEXT,
                DESCRCONTA TEXT,
                CPF_CNPJ TEXT,
                CLIENTE TEXT,
                CEP TEXT,
                CIDADE TEXT,
                UF TEXT,
                DDD TEXT,
                TELEFONE TEXT,
                POSSE TEXT)''')
        except Exception as e:
            print('[x] Falha ao criar tabela: %s [x]' % e)
        else:
            print('\n[!] Tabela criada com sucesso [!]\n')

    def inserir_registro(self, vin, model, data, produto, anofabricacao, codconta, descrconta, cpf_cnpj, cliente, cep, cidade, uf, ddd, telefone, posse):
        try:
            self.cur.execute(
                '''INSERT INTO Recall VALUES (?, ?, ?, ? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?)''', (vin, model, data, produto, anofabricacao, codconta, descrconta, cpf_cnpj, cliente, cep, cidade, uf, ddd, telefone, posse,))
        except Exception as e:
            print('\n[x] Falha ao inserir registro [x]\n')
            print('[x] Revertendo operação (rollback) %s [x]\n' % e)
            self.con.rollback()
        else:
            self.con.commit()
            print('\n[!] Registro inserido com sucesso [!]\n')

    def consultar_registros(self):
        return self.cur.execute('SELECT rowid, * FROM Recall').fetchall()

    def consultar_ultimo_rowid(self):
        return self.cur.execute('SELECT MAX(rowid) FROM Recall').fetchone()

    def remover_registro(self, rowid):
        try:
            self.cur.execute("DELETE FROM Recall WHERE rowid=?", (rowid,))
        except Exception as e:
            print('\n[x] Falha ao remover registro [x]\n')
            print('[x] Revertendo operação (rollback) %s [x]\n' % e)
            self.con.rollback()
        else:
            self.con.commit()
            print('\n[!] Registro removido com sucesso [!]\n')


class Janela(tk.Frame):
    """Janela principal"""

    def __init__(self, master=None):
        """Construtor"""
        super().__init__(master)
        # Coletando informações do monitor
        largura = round(self.winfo_screenwidth() / 2)
        altura = round(self.winfo_screenheight() / 2)
        tamanho = ('%sx%s' % (largura, altura))

        # Título da janela principal.
        master.title('Recall')

        # Tamanho da janela principal.
        master.geometry(tamanho)

        # Instanciando a conexão com o banco.
        self.banco = ConectarDB()

        # Gerenciador de layout da janela principal.
        self.pack()

        # Criando os widgets da interface.
        self.criar_widgets()

    def criar_widgets(self):
        # Containers.
        frame1 = tk.Frame(self)
        frame1.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

        frame2 = tk.Frame(self)
        frame2.pack(fill=tk.BOTH, expand=True, pady=5)

        frame3 = tk.Frame(self)
        frame3.pack(side=tk.BOTTOM, padx=5)

        # Labels.
        label_documento = tk.Label(frame1, text='Vin')
        label_documento.grid(row=0, column=0)

        label_recebido = tk.Label(frame1, text='Data recebimento')
        label_recebido.grid(row=2, column=0)

        label_assunto = tk.Label(frame1, text='Modelo')
        label_assunto.grid(row=0, column=1)        

        label_recebido = tk.Label(frame1, text='Produto')
        label_recebido.grid(row=0, column=2)

        label_recebido = tk.Label(frame1, text='Ano de fabricação')
        label_recebido.grid(row=0, column=3)

        label_recebido = tk.Label(frame1, text='Cod. conta')
        label_recebido.grid(row=0, column=4)

        label_recebido = tk.Label(frame1, text='Desc. conta')
        label_recebido.grid(row=0, column=5)

        label_recebido = tk.Label(frame1, text='Cpf/Cnpj')
        label_recebido.grid(row=2, column=1)

        label_recebido = tk.Label(frame1, text='Cliente')
        label_recebido.grid(row=2, column=2)

        label_recebido = tk.Label(frame1, text='Cep')
        label_recebido.grid(row=2, column=3)

        label_recebido = tk.Label(frame1, text='Cidade')
        label_recebido.grid(row=2, column=4)

        label_recebido = tk.Label(frame1, text='UF')
        label_recebido.grid(row=2, column=5)

        label_recebido = tk.Label(frame1, text='DDD')
        label_recebido.grid(row=4, column=1)

        label_recebido = tk.Label(frame1, text='Telefone')
        label_recebido.grid(row=4, column=2)

        label_recebido = tk.Label(frame1, text='Posse')
        label_recebido.grid(row=4, column=3  )


        # Entrada de texto.
        self.entry_vin = tk.Entry(frame1)
        self.entry_vin.grid(row=1, column=0)

        self.entry_data = tk.Entry(frame1)
        self.entry_data.grid(row=3, column=0)

        self.entry_model = tk.Entry(frame1)
        self.entry_model.grid(row=1, column=1, padx=10)
    
        self.entry_produto = tk.Entry(frame1)
        self.entry_produto.grid(row=1, column=2)

        self.entry_anofabricacao = tk.Entry(frame1)
        self.entry_anofabricacao.grid(row=1, column=3)

        self.entry_codconta = tk.Entry(frame1)
        self.entry_codconta.grid(row=1, column=4)

        self.entry_descrconta = tk.Entry(frame1)
        self.entry_descrconta.grid(row=1, column=5)

        self.entry_cpf_cnpj = tk.Entry(frame1)
        self.entry_cpf_cnpj.grid(row=3, column=1)

        self.entry_cliente = tk.Entry(frame1)
        self.entry_cliente.grid(row=3, column=2)

        self.entry_cep = tk.Entry(frame1)
        self.entry_cep.grid(row=3, column=3)

        self.entry_cidade = tk.Entry(frame1)
        self.entry_cidade.grid(row=3, column=4)

        self.entry_uf = tk.Entry(frame1)
        self.entry_uf.grid(row=3, column=5)

        self.entry_ddd = tk.Entry(frame1)
        self.entry_ddd.grid(row=6, column=1)

        self.entry_telefone = tk.Entry(frame1)
        self.entry_telefone.grid(row=6, column=2)

        self.entry_posse = tk.Entry(frame1)
        self.entry_posse.grid(row=6, column=3)

        # Botão para adicionar um novo registro.
        button_adicionar = tk.Button(frame1, text='Adicionar', bg='blue', fg='white')
        # Método que é chamado quando o botão é clicado.
        button_adicionar['command'] = self.adicionar_registro
        button_adicionar.grid(row=7, column=6, rowspan=2, padx=10)

        # Treeview.
        self.treeview = tkk.Treeview(frame2, columns=('Vin', 'Model', 'Data', 'Produto', 'Ano fabricação', 'Cod. Conta', 'Descrição Conta', 'Cpf/Cnpj', 'Cliente', 'Cep', 'Cidade', 'UF', 'DDD', 'Telefone', 'Posse'))
        self.treeview.heading('#0', text='ID')
        self.treeview.heading('#1', text='Vin')
        self.treeview.heading('#2', text='Model')
        self.treeview.heading('#3', text='Data')
        self.treeview.heading('#4', text='Produto')
        self.treeview.heading('#5', text='Ano fabricação')
        self.treeview.heading('#6', text='Cod. Conta')
        self.treeview.heading('#7', text='Descrição Conta')
        self.treeview.heading("#8", text="Cpf/Cnpj")
        self.treeview.heading("#9", text="Cliente")
        self.treeview.heading("#10", text="Cep")
        self.treeview.heading("#11", text="Cidade")
        self.treeview.heading("#12", text="UF")
        self.treeview.heading("#13", text="DDD")
        self.treeview.heading("#14", text="Telefone")
        self.treeview.heading("#15", text="Posse")

        # Inserindo os dados do banco no treeview.
        for row in self.banco.consultar_registros():
            self.treeview.insert('', 'end', text=row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15]))

        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Botão para remover um item.
        button_excluir = tk.Button(frame3, text='Excluir', bg='red', fg='white')
        # Método que é chamado quando o botão é clicado.
        button_excluir['command'] = self.excluir_registro
        button_excluir.pack(pady=10)

    def adicionar_registro(self):
        # Coletando os valores.
        vin = self.entry_vin.get()
        model = self.entry_model.get()
        data = self.entry_data.get()
        produto = self.entry_produto.get()
        anofabricacao = self.entry_anofabricacao.get()
        codconta = self.entry_codconta.get()
        descrconta = self.entry_descrconta.get()
        cpf_cnpj = self.entry_cpf_cnpj.get()
        cliente = self.entry_cliente.get()
        cep = self.entry_cep.get()
        cidade = self.entry_cidade.get()
        uf = self.entry_uf.get()
        ddd = self.entry_ddd.get()
        telefone = self.entry_telefone.get()
        posse = self.entry_posse.get()

        # Validação simples (utilizar datetime deve ser melhor para validar).
        validar_data = re.search(r'(..)/(..)/(....)', data)

        # Se a data digitada passar na validação
        if validar_data:
            # Dados digitando são inseridos no banco de dados
            self.banco.inserir_registro(vin=vin, model=model, data=data, produto=produto, anofabricacao=anofabricacao, codconta=codconta, descrconta=descrconta, cpf_cnpj=cpf_cnpj, cliente=cliente, cep=cep, cidade=cidade, uf=uf, ddd=ddd, telefone=telefone, posse=posse)

            # Coletando a ultima rowid que foi inserida no banco.
            rowid = self.banco.consultar_ultimo_rowid()[0]

            # Adicionando os novos dados no treeview.
            self.treeview.insert('', 'end', text=rowid, values=(vin, model, data, produto, anofabricacao, codconta, descrconta, cpf_cnpj, cliente, cep, cidade, uf, ddd, telefone, posse))
        else:
            # Caso a data não passe na validação é exibido um alerta.
            messagebox.showerror('Erro', 'Padrão de data incorreto, utilize dd/mm/yyyy')

    def excluir_registro(self):
        # Verificando se algum item está selecionado.
        if not self.treeview.focus():
            messagebox.showerror('Erro', 'Nenhum item selecionado')
        else:
            # Coletando qual item está selecionado.
            item_selecionado = self.treeview.focus()

            # Coletando os dados do item selecionado (dicionário).
            rowid = self.treeview.item(item_selecionado)

            # Removendo o item com base no valor do rowid (argumento text do treeview).
            # Removendo valor da tabela.
            self.banco.remover_registro(rowid['text'])

            # Removendo valor do treeview.
            self.treeview.delete(item_selecionado)


root = tk.Tk()
app = Janela(master=root)
app.mainloop()
