


#vou reutilizar o Estudo Dirigido anterior 
# 2 padrões da aula: 
# Singleton (criar classe Pedido) -> Pedido guarda a única instância em _instancia e a entrega por get_instance()
# Factory Method (if e else) -> FábricaBebida.criar() concentra a escolha de uma classe em um só lugar e devolve a bebida

# Domínio: Cafeteria 
# Superclasse: Bebidas
#Subclasse: Quentes e frias 

#Método abstrato: preparar()
#Método Sobrescrito: calcular_preco()

import tkinter as tk
from tkinter import messagebox

from abc import ABC, abstractmethod

#crias as excessões
class BebidaInvalidaError(ValueError):
    """Base: Qualquer dado inválido de bebida"""
class NomeInvalidoError(BebidaInvalidaError): pass
class PrecoInvalidoError(BebidaInvalidaError): pass
class TemperaturaInvalidaError(BebidaInvalidaError): pass
class GeloInvalidoError(BebidaInvalidaError): pass


# Classe abstrata: não gera objetos; existe para as filhas herdarem
class Bebida(ABC):

    def __init__ (self, nome, preco_base):
        self.nome = nome
        self.preco_base = preco_base

    @abstractmethod
    def preparar(self):
        ... #vazio, só declara o método

    def calcular_preco(self):
        return self.preco_base

    @property #segurança
    def nome(self):
            return self._nome
    @nome.setter
    def nome(self, n):
            if not n or not n.strip():
                raise NomeInvalidoError ("O nome da bebida não pode ficar vazio\n")
            self._nome = n.strip()

    @property
    def preco_base (self):
        return self._preco_base

    @preco_base.setter
    def preco_base (self, p):
        if p <= 0:
            raise PrecoInvalidoError ("O preço deve ser maior que zero\n")
        self._preco_base = p

class BebidaQuente (Bebida): 

    def __init__(self, nome, preco_base, temperatura):
        super().__init__(nome, preco_base)
        self.temperatura = temperatura 

    @property #segurança
    def temperatura(self):
        return self._temperatura

    @temperatura.setter
    def temperatura(self, temp):
        if not (50 <= temp <= 100):
            raise TemperaturaInvalidaError ("A temperatura deve ficar entre 50 e 100°\n")
        self._temperatura = temp

    def preparar(self):
        return f"{self.nome} está sendo preparada a {self.temperatura} °C\n"

class BebidaGelada (Bebida): 

    def __init__(self, nome, preco_base, qtd_gelo):
        super().__init__(nome, preco_base)
        self.qtd_gelo = qtd_gelo 

    @property #segurança
    def qtd_gelo(self):
        return self._qtd_gelo

    @qtd_gelo.setter #segurança
    def qtd_gelo(self, gelo):
        if not (gelo >= 0):
            raise GeloInvalidoError ("Não pode ter número negativo de gelo\n")
        self._qtd_gelo = gelo

    def preparar(self):
        return f"{self.nome} está sendo preparada com {self.qtd_gelo:g} cubos de gelo\n"

    def calcular_preco(self): 
         return super().calcular_preco() + 2.00 #inserindo gelo é adicional de 2 reais

class Pedido ():
    _instancia = None #guarda a única instância, para garantir que só exista um Pedido no programa

    def __init__(self):
        self.bebidas = [] 

    @classmethod
    def get_instance(cls):
        if cls._instancia is None: #porta de entrada para o pedido
            cls._instancia = Pedido()
        return cls._instancia

    def adicionar (self, bebida): #adiciona um pedido na lista
        self.bebidas.append(bebida)

    def total(self): #calcula o preço total 
        soma = 0
        for b in self.bebidas:
            soma = soma + b.calcular_preco()
        return soma

class FabricaBebida:

    @staticmethod
    def criar (tipo, nome, preco, extra):
        if tipo == "Quente":
            return BebidaQuente (nome, preco, extra)
        if tipo == "Gelada":
            return BebidaGelada (nome, preco, extra)
        raise ValueError("Tipo desconhecido: " + tipo)

class JanelaCafeteria(): #interface gráfica

    def __init__ (self, janela):
        self.janela = janela
        janela.title ("Cafeteria")

        #Formulário montado com grid()
        tk.Label (janela, text = "Tipo:").grid(row=0, column=0,sticky="e",padx=5,pady=5)
        self.tipo = tk.StringVar(value="Quente")
        tk.OptionMenu(janela, self.tipo, "Quente", "Gelada").grid(row=0, column=1, sticky="w")

        tk.Label (janela, text = "Nome:").grid(row=1, column=0, sticky ="e", padx=5, pady=5)
        self.nome = tk.Entry(janela)
        self.nome.grid(row=1, column=1, padx=5)

        tk.Label (janela, text = "Preço:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.preco = tk.Entry(janela)
        self.preco.grid(row=2,column=1,padx=5)

        tk.Label(janela, text="Temperatura/Gelo: ").grid(row=3,column=0,sticky="e", padx=5,pady=5)
        self.extra = tk.Entry(janela)
        self.extra.grid(row=3, column=1, padx=5)

        tk.Button(janela, text = "Adicionar", command=self.adicionar_clicado).grid(row=4, column=0, columnspan=2, pady=8)

        self.lista = tk.Listbox(janela, width=45)
        self.lista.grid(row=5, column=0, columnspan=2, padx=5)

        self.lbl_total = tk.Label(janela, text="Total: R$ 0.00")
        self.lbl_total.grid(row=6, column=0, columnspan=2, pady=5)

    def adicionar_clicado(self):
        try:
            bebida = FabricaBebida.criar(
                self.tipo.get(), self.nome.get(),
                float(self.preco.get()), float(self.extra.get()))
            Pedido.get_instance().adicionar(bebida) 
            self.lista.insert(tk.END, bebida.preparar().strip())
            self.lbl_total.config(
                text = f"Total: R$ {Pedido.get_instance().total():.2f}")
        except ValueError as e:
            messagebox.showerror("Dado inválido", str(e).strip())

if __name__ == "__main__":

    janela = tk.Tk()
    JanelaCafeteria(janela)
    janela.mainloop()
