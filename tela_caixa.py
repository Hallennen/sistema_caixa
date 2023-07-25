from tkinter import * 
from tkinter import ttk as tk
import psycopg2

#acumulador de preços
valores=[]
nome_sistema = 'MERCADINHO SEU ZÉ'

#função de confimar o codigo digitado
def confirma(event=None):
    try:
        connect = psycopg2.connect(database="user", user="postgres", password="xxxx")
        cursor = connect.cursor()
        sintaxe = "SELECT * FROM produtos WHERE id_produto = '{}' ".format(codigo_item_entry.get())
        cursor.execute(sintaxe)
        produtos = cursor.fetchone()

        item.insert('',index=0,values=(produtos[0],produtos[1],produtos[2]))

        print('PRODUTO: ', produtos[1], '\t\t\t\t\t PREÇO: ', produtos[2])
        valores.append(float(produtos[2]))
        codigo_item_entry.delete(0,END)

        total_compra.insert('',index=0, values=float(sum(valores)))

    except:
        codigo_item_entry.delete(0,END)
        print('codigo incorreto')
    

#função de tela de itens geral
def tela_de_busca():
    global tela_consulta
    tela_consulta = Tk()
    tela_consulta.title('Base de itens')
    tela_consulta.geometry('600x500+180+60')
    tela_consulta.minsize(height='400', width='500')
    tela_consulta.config(bg= '#1e3743')


    nome_sistema = tk.Label(tela_consulta, text='MERCADINHO SEU ZÉ', foreground= 'white',
                             background='#1e3743', font=('arial', 18))
    nome_sistema.place(relx= 0.29 , rely= 0.1)
    tabela_de_consulta()


    return tela_consulta.mainloop()


#função formatação da tabela
def tabela_de_consulta():
    connect = psycopg2.connect(database="user", user="postgres", password="xxxx")
    cursor = connect.cursor()
    sintaxe = "SELECT * FROM produtos order by id_produto ASC "
    cursor.execute(sintaxe)
    produtos = cursor.fetchall()


    tabela =tk.Treeview(tela_consulta, columns=('codigo','descrição','preço'), show='headings')
    tabela.column('codigo', minwidth=50, width=140, anchor='center')
    tabela.column('descrição', minwidth=40, width=240, anchor='center')
    tabela.column('preço', minwidth=50, width=140, anchor='center')
    tabela.heading('codigo', text='CODIGO')
    tabela.heading('descrição', text='DESCRIÇÃO')
    tabela.heading('preço', text='PREÇO')
    tabela.place(rely=0.22, relx=0.06 ,relwidth=0.88, relheight=0.7)

    for i in range (int(len(produtos))):
        tabela.insert('',END,values=(produtos[i][0],produtos[i][1],produtos[i][2]))
        i += 1


#função salvar item novo na base 
def salvar_item():
    connect = psycopg2.connect(database="user", user="postgres", password="xxxx")
    cursor = connect.cursor()
    #primeiro valida se já existe o item na base 
    try:
        sintaxe = """ SELECT id_produto FROM produtos WHERE id_produto = '{}' """.format(codigo_entry.get())
        cursor.execute(sintaxe)
        retorno = cursor.fetchone()

        if int(codigo_entry.get()) == retorno[0]:
            print(str(retorno[0]) + 'item já cadastro')
        Frame_error = Frame(tela_cadastro,bg='red')
        Frame_error.place(y=0,height=30, width=400)
        frase_frame = Label(tela_cadastro, text='Codigo já cadastrado',bg='red', font=('arial', 12))
        frase_frame.place( x=5, y=2)

    #cadastrando o item na base
    except:
        print('sem cadastro, cadastrando')

        sintaxe = """INSERT INTO produtos (id_produto, name_produto, valor_produto)
                    VALUES ('{}','{}','{}') """.format(codigo_entry.get() ,descrição_entry.get().upper(), preço_entry.get())
        cursor.execute(sintaxe)
        connect.commit()
        connect.close()
        print('cadastrado')
        Frame1 = Frame(tela_cadastro,bg='green')
        Frame1.place(y=0,height=30, width=400)
        frase_frame = Label(tela_cadastro, text='Operação concluida!',bg='green', font=('arial', 12))
        frase_frame.place( x=5, y=2)

        codigo_entry.delete(0,END)
        descrição_entry.delete(0, END)
        preço_entry.delete(0, END)
        Entry.focus(codigo_entry)

    return

#tela de cadastro
def cadastrar_item():
    global descrição_entry, codigo_entry, preço_entry,tela_cadastro


    tela_cadastro= Tk()
    tela_cadastro.geometry('400x200+700+160')
    tela_cadastro.title('cadastro de mercadoria')
    tela_cadastro.minsize(width=400 , height=200)
    tela_cadastro.maxsize(width=400 , height=200)
    tela_cadastro.configure(bg='#1e3743')


    fundo = Label(tela_cadastro, bg='#D3D3D3')
    fundo.place(relx= 0.017 , rely=0.025, height=190, width=385)

    nome_sistema = tk.Label(tela_cadastro, text='MERCADINHO SEU ZÉ', foreground= '#1e3743', background='#D3D3D3', font=('arial', 18))
    nome_sistema.place(x= 68 , y=18 )

    codigo = Label(tela_cadastro,text='Código do produto: ', font=('helvetica', 13), bg='#D3D3D3')
    codigo.place(x= 18 , y= 60 )
    codigo_entry=Entry(tela_cadastro,highlightcolor='lightblue', highlightthickness=2, borderwidth=0,justify='center')       
    codigo_entry.place(x= 190 , y= 62, width= 180 )
    Entry.focus(codigo_entry)

    descrição = Label(tela_cadastro,text='Descrição do produto: ', font=('helvetica', 13), bg='#D3D3D3')
    descrição.place(x= 18 , y= 89)
    descrição_entry=Entry(tela_cadastro,highlightcolor='lightblue', highlightthickness=2, borderwidth=0,justify='center')
    descrição_entry.place(x= 190 , y= 91, width= 180 )

    preço = Label(tela_cadastro, text='Preço do produto: ', font=('helvetica', 13), bg='#D3D3D3')
    preço.place(x= 18 , y= 118 )
    preço_entry=Entry(tela_cadastro,highlightcolor='lightblue', highlightthickness=2, borderwidth=0,justify='center')
    preço_entry.place(x= 190 , y= 120, width= 180 )

    salvar = Button(tela_cadastro, text='Salvar', command=salvar_item, bg='#F5F5F5',
                    fg='navy',font=('Garamond ',9))
    salvar.place(x= 90 , y= 160, width= 80 )

    cancelar = Button(tela_cadastro, text='Fechar', command=tela_cadastro.destroy, bg='#F5F5F5',
                        fg='navy',font=('Garamond ',9))
    cancelar.place(x= 230 , y= 160, width= 80 )

    return tela_cadastro.mainloop()
        
#função pagamento
def pagamento():
    global desconto, valor_entrada, total_a_pagar, tela_pagamento

    tela_pagamento = Tk()
    tela_pagamento.geometry('400x520+600+100')
    tela_pagamento.minsize()
    tela_pagamento.maxsize()
    tela_pagamento.title('PAGAMENTO')
    tela_pagamento.config(bg='#1e3743')

    nome_sistema = tk.Label(tela_pagamento, text='MERCADINHO SEU ZÉ', foreground= 'white', background='#1e3743', font=('arial', 18))
    nome_sistema.place(x= 68 , y=18 )


    borada= LabelFrame(tela_pagamento, text='Forma de pagamento ',fg='white',background='#274757',border=3.5)
    borada.place(x=15, y=60, height=80, width=370)

    botton_dinheiro = Checkbutton(tela_pagamento, text='Dinheiro',bg='#274757', font=('arial',12),
                                    activebackground='#274757',onvalue='true')
    botton_dinheiro.place(rely=0.18, relx=0.12)


    button_credito = Checkbutton(tela_pagamento, text='Crédito',bg='#274757', font=('arial',12), activebackground='#274757')                                    
    button_credito.place(rely=0.18, relx=0.41)

    button_debito = Checkbutton(tela_pagamento, text='Débito',bg='#274757', font=('arial',12),
                                    activebackground='#274757')#31596D
    button_debito.place(rely=0.18, relx=0.68)


    centro= LabelFrame(tela_pagamento, text='Pagamento ',fg='white',background='#274757',border=3.5)
    centro.place(x=15, y=150, height=280, width=370)


#linha 1
    subtotal= Label(tela_pagamento, text='SubTotal: ', font=('',15), bg='#274757', fg='white')
    subtotal.place(x=30 , y=180)

    subtotal_valor= Label(tela_pagamento, text='R$ ', font=('',15), bg='lightgray', fg='black')
    subtotal_valor.place(y=180 , x=150, width=200, height=30)
    subtotal_valor.config(text='R$ ' + str(sum(valores)))


#linha 2

    desconto = Label(tela_pagamento, text='Desconto: ', font=('',15), bg='orange', fg='white')
    desconto.place(x=30 , y=230)

    desconto = Entry(tela_pagamento, highlightcolor='#00CED1', highlightthickness=2, border=0,justify= 'center')
    desconto.place(y=230 , x=150, width=200, height=30)
    Entry.focus_force(desconto)
    desconto.bind('<Return>', valida_desconto)


#linha 3

    total_a_pagartxt = Label(tela_pagamento, text='Total: ', font=('',15), bg='green', fg='white')
    total_a_pagartxt.place(x=30 , y=280)

    total_a_pagar= Label(tela_pagamento,text='R$ ', font=('',15), bg='lightgray', fg='black')
    total_a_pagar.place(y=280 , x=150, width=200, height=30)
    Entry.focus_lastfor(total_a_pagar)



#linha 4

    valor_entradatxt= Label(tela_pagamento, text='Valor: ', font=('',15), bg='#274757',fg='white')
    valor_entradatxt.place( x=30, y= 350 , height=30)

    valor_entrada = Entry (tela_pagamento, font=('',17),justify='center',borderwidth= 0 ,
                            highlightthickness= 2, highlightcolor="#00CED1")
    valor_entrada.place(x= 150 , y=350, width=200  , height=60)
    valor_entrada.bind("<Return>", valida_pagamento)


# botão pagar

    button_pagar = Button(tela_pagamento,text='Pagar', command=valida_pagamento)
    button_pagar.place(x=120, y=450, width=180, height=50)      


    print('passou aqui')

    return tela_pagamento.mainloop()



def valida_desconto(event=None):
    global valor_com_desconto
    if int(desconto.get()) <= 99:
        print(desconto.get())
        desconto_real = int(desconto.get()) /100
        valor_com_desconto = int(sum(valores)) - (int(sum(valores))* desconto_real) 
        total_a_pagar.config(text='R$ ' + str(valor_com_desconto))
        # desconto.delete(0,END)
        # valor_entrada.delete(0, END)

    else:
        print('Desconto não pode ser maior do que "99".')
        desconto.delete(0,END)
        valor_entrada.delete(0, END)

    return valida_desconto



def valida_pagamento(event=None):

    info_troco= Message(window,text='troco: ')
    info_troco.place(relx=0.10 , rely=0.50)

  
    conta = float(valor_entrada.get()) - float(valor_com_desconto)
    print('Troco: ',conta)

    desconto.delete(0,END)
    valor_entrada.delete(0, END)
    tela_pagamento.destroy()
    limpar()
    


    return valida_pagamento
    

def limpar():
    valores.clear()
    window.update()
    window.destroy()
    tela_inicial()    

    return limpar


def tela_inicial():
    global codigo_item_entry, item, total_compra, window
    #configuração da tela principal 
    window = Tk()
    window.title('Caixa')
    window.geometry('600x500+140+90')
    window.minsize(width='500', height='400')
    window.configure(bg= '#1e3743' )
    window.resizable(True, True)
    style = tk.Style()
    style.configure('Treeview', background='lightblue')
    window.focus_force()

    window.columnconfigure(0,weight=1)
    window.columnconfigure(1,weight=1)


    #titulo do sistema
    nome_sistema = tk.Label(window, text='MERCADINHO SEU ZÉ', foreground= 'white', background='#1e3743', font=('arial', 18))
    nome_sistema.grid(row=0, columnspan=2, pady=20 )


    #titulo do label
    codigo_item = tk.Label(text='Código: ', foreground='white', background='#1e3743', font=('helvetica',15))
    codigo_item.place (relx=0.12 , rely= 0.141)



    #entry principal
    codigo_item_entry = Entry(highlightcolor='#00CED1',highlightthickness='1',borderwidth=0)
    codigo_item_entry.place(relwidth=0.35, rely=0.15, relx=0.41)
    Entry.focus(codigo_item_entry)
    codigo_item_entry.bind('<Return>', confirma)


    #botão confirmar item
    confirmar_item= Button(window,text=' CONFIRMAR ', command=confirma, bg='#F5F5F5',
                            fg='navy',font=('Garamond ',9))
    confirmar_item.place(relx=0.795 , rely=0.143, relheight=0.05)

    #tabela de dados
    item = tk.Treeview(window,columns=('codigo','nome','preço'),show='headings')
    item.column('codigo', minwidth=50, width=140, anchor='center')
    item.column('nome', minwidth=40, width=240, anchor='center')
    item.column('preço', minwidth=50, width=140, anchor='center')
    item.heading('codigo', text='CODIGO')
    item.heading('nome', text='DESCRIÇÃO')
    item.heading('preço', text='PREÇO')



    item.place(rely=0.22, relx=0.06 ,relwidth=0.88, relheight=0.45)


    #botão buscar item
    buscar= Button(window, text=' Buscar itens ',command=tela_de_busca, bg='#F5F5F5', fg='navy' )
    buscar.place(relx=0.2, rely=0.7)


    #botão NOVO ITEM
    resultado = Button(text='  Novo item  ', command=cadastrar_item, bg='#F5F5F5', fg='navy')
    resultado.place(relx= 0.45 , rely=0.7)

    #BOTÃO PAGAMENTO 
    botão_pagamento = Button(window,text='Pagamento', command=pagamento, bg='#F5F5F5', fg='navy')
    botão_pagamento.place(relx=0.7, rely=0.7 )

    #BOTÃO LIMPAR TUDO

    botao_limpar = Button(window, text='Limpar', bg='#F5F5F5', fg='navy', command=limpar )
    botao_limpar.place( relx=0.85 , rely=0.7 )



    #TABELA TOTAL
    total_compra = tk.Treeview(window, column='total',show='headings')
    total_compra.heading('total', text='TOTAL')
    total_compra.column('total',minwidth=10 ,width=520, anchor='center')
    total_compra.place(rely=0.8, relx=0.06 ,relwidth=0.88)
    total_compra.config(height=1)


    #INFORMAÇOES DE NAVEGAÇÃO
    informações = Label(window,text='F1= CONSULTA     F2= PAGAMENTO     ENTER= CONFIRMAR',
                        background='#1e3743', fg='red',font='bold' )
    informações.place(relx=0.12 , rely=0.92)


    return window.mainloop()

tela_inicial()