from tkinter import *
from tkinter import ttk
import sqlite3

root = Tk()

class funcs():
    def capitalize_name(self):
        lowercase_words = ["da", "de", "do", "dos", "das", "e"]
        name = self.nome_entry.get()
        words = name.split()  
        capitalized_words = [word.capitalize() if word.lower() not in lowercase_words else word for word in words]
        capitalized_name = ' '.join(capitalized_words)
        return capitalized_name
    
    def limpar_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.bd")
        self.cursor = self.conn.cursor(); print("Conectando ao banco de dados!")
    
    def desconecta_bd(self):
        self.conn.close(); print("Desconectando ao banco de dados 3")
    
    def montaTabelas(self):
        self.conecta_bd()

        # Criando a tabela

        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                            cod INTEGER PRIMARY KEY,
                            nome_cliente CHAR(40) NOT NULL,
                            telefone INTEGER(20),
                            cidade CHAR(40)
                );
        """)

        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd()

    def add_cliente(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.capitalize_name()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()
        self.conecta_bd()

        self.cursor.execute("""
            INSERT INTO clientes (nome_cliente, telefone, cidade)
            VALUES(?, ?, ?)

        """, (self.nome, self.telefone, self.cidade))

        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_tela()

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()
    
    def select_lista(self):
        self.lista.delete(*self.lista.get_children())
        self.conecta_bd()
        lista1 = self.cursor.execute("""
                SELECT cod, nome_cliente, telefone, cidade FROM clientes
                ORDER BY nome_cliente ASC
                """)
        for i in lista1:
            self.lista.insert("", END, values=i)
        
        self.desconecta_bd()

    def duplo_click(self, event):
        self.limpar_tela()
        self.lista.selection()

        for c in self.lista.selection():
            col1, col2, col3, col4 = self.lista.item(c, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)
        
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo, ))
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_tela()
        self.select_lista()

    def alterar_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ?
                            WHERE cod = ? """, (self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_tela()

class Application(funcs):

    def __init__(self) -> None:
        self.root = root
        self.tela()
        self.frame_da_tela()
        self.widgets_frame()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        root.mainloop()

    def tela(self):
        self.root.title("Cadastro de clientes")
        self.root.configure(background="#3b77bf")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.minsize(width=500, height=300)
        self.root.maxsize(width=900, height=700)
    
    def frame_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#dfe3ee', highlightbackground='black', highlightthickness=3)
        self.frame_1.place(relx= 0.01, rely= 0.02, relwidth=0.98, relheight=0.47)
        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee', highlightbackground='black', highlightthickness=3)
        self.frame_2.place(relx= 0.01, rely= 0.5, relwidth=0.98, relheight=0.48)
    
    def widgets_frame(self):
        
        # Botões
        
        ## Botão de limpar
        self.bt_limpar = Button(self.frame_1, text='Limpar', bd=2, bg='#107db2', fg='white', font = ('Verdana', 8, 'bold'), command=self.limpar_tela)
        self.bt_limpar.place(relx= 0.2,rely= 0.1, relwidth= 0.1, relheight=0.15)

        ## Botão de busca
        self.bt_busca = Button(self.frame_1, text='Buscar', bd=2, bg='#107db2', fg='white', font = ('Verdana', 8, 'bold'))
        self.bt_busca.place(relx= 0.3,rely= 0.1, relwidth= 0.1, relheight=0.15)

        ## Botão de novo
        self.bt_novo = Button(self.frame_1, text='Novo', bd=2, bg='#107db2', fg='white', font = ('Verdana', 8, 'bold'), command=self.add_cliente)
        self.bt_novo.place(relx= 0.6,rely= 0.1, relwidth= 0.1, relheight=0.15)

        ## Botão de alterar
        self.bt_alterar = Button(self.frame_1, text='Alterar', bd=2, bg='#107db2', fg='white', font = ('Verdana', 8, 'bold'), command=self.alterar_cliente)
        self.bt_alterar.place(relx= 0.7,rely= 0.1, relwidth= 0.1, relheight=0.15)

        ## Botão de apagar
        self.bt_apagar = Button(self.frame_1, text='Apagar', bd=2, bg='#107db2', fg='white', font = ('Verdana', 8, 'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx= 0.8,rely= 0.1, relwidth= 0.1, relheight=0.15)

        # Labels
        
        ## Label do código
        self.lb_codigo = Label(self.frame_1, text='Código', bg='#dfe3ee', fg='#107db2', font = ('Verdana', 8, 'bold'))
        self.lb_codigo.place(relx= 0.05, rely= 0.05)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx= 0.05, rely= 0.15, relwidth= 0.08)

        ## Label do nome
        self.lb_nome = Label(self.frame_1, text='Nome', bg='#dfe3ee', fg='#107db2', font = ('Verdana', 8, 'bold'))
        self.lb_nome.place(relx= 0.05, rely= 0.35)
        
        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx= 0.05, rely= 0.45, relwidth= 0.7)


        ## Label do telefone
        self.lb_telefone = Label(self.frame_1, text='Telefone', bg='#dfe3ee', fg='#107db2', font = ('Verdana', 8, 'bold'))
        self.lb_telefone.place(relx= 0.05, rely= 0.6)
        
        self.telefone_entry = Entry(self.frame_1)
        self.telefone_entry.place(relx= 0.05, rely= 0.7, relwidth= 0.4)

        ## Label da cidade
        self.lb_cidade = Label(self.frame_1, text='Cidade', bg='#dfe3ee', fg='#107db2', font = ('Verdana', 8, 'bold'))
        self.lb_cidade.place(relx= 0.5, rely= 0.6)
        
        self.cidade_entry = Entry(self.frame_1)
        self.cidade_entry.place(relx= 0.5, rely= 0.7, relwidth= 0.4)

    def lista_frame2(self):
        self.lista = ttk.Treeview(self.frame_2, height= 3, column = ('Col1', 'Col2', 'Col3', 'Col4'))
        self.lista.heading("#0", text="")
        self.lista.heading("#1", text="Código")
        self.lista.heading("#2", text="Nome")
        self.lista.heading("#3", text="Telefone")
        self.lista.heading("#4", text="Cidade")

        self.lista.column('#0', width= 1)
        self.lista.column('#1', width= 50)
        self.lista.column('#2', width= 200)
        self.lista.column('#3', width= 125)
        self.lista.column('#4', width= 125)

        self.lista.place(relx = 0.01, rely = 0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.lista.configure(yscroll = self.scroolLista.set)
        self.scroolLista.place(relx = 0.96, rely = 0.1, relheight= 0.85, relwidth= 0.04)
        self.lista.bind("<Double-1>", self.duplo_click)


Application()