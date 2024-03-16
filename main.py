import uuid
import cmd
import time


class Node:
    def __init__(self, data):
        self.data = data
        self.edge = None

    def __repr__(self):
        return "%s(data=%s)" % (self.__class__.__name__, repr(self.data))


class Paquete(Node):
    def __init__(self, data, destinatario):
        super().__init__(data)
        self.destinatario = destinatario
        self.direccion = None
        self.fecha_envio = time.time()
        self.fecha_entrega = None
        self.estado = "no entregado"


class LinkedList:
    def __init__(self):
        self.__root = None  # Datos "privados"
        self.__edge = None  # Datos "privados"
        self.length = 0

    @property
    def root(self):
        return self.__root

    @property
    def edge(self):
        return self.__edge

    def insert(self, node, index=-1):
        if index == -1:
            self.insert_node(node, self.insert_edge)
        elif index == 0:
            self.insert_node(node, self.insert_begin)
        else:
            raise NotImplementedError

    def insert_node(self, node, callback):
        if self.root is None and self.edge is None:
            self.__edge = self.__root = node
        else:
            callback(node)
        self.length += 1

    def insert_edge(self, node):
        self.__edge.edge = node
        self.__edge = node

    def insert_begin(self, node):
        node.edge = self.__root
        self.__root = node

    def get_by_data(self, data, field='data'):
        node = self.root
        index = 0
        while node is not None:
            if getattr(node, field) == data:
                return index, node
            node = node.edge
            index += 1

    def del_by_data(self, data, field='data'):
        if self.root is None:
            return False
        elif self.root is self.edge:
            if getattr(self.root, field) == data:
                self.__root = None
                self.__edge = None
                self.length -= 1
                return True
            return False
        elif getattr(self.root, field) == data:
            self.__root = self.__root.edge
            self.length -= 1
            return True
        elif self.root.edge is None:
            return False

        before = self.root  # antes
        current = self.root.edge
        index = 0
        while index <= self.length - 1:
            if current is None:
                break
            elif getattr(current, field) == data:
                before.edge = current.edge
                return True
            else:
                before = current
                current = current.edge
            index += 1
        return False


class Menu(cmd.Cmd):
    ll = LinkedList()

    def do_nuevo_envio(self, arg):
        destinatario = input("Destinatario: ")
        posicion = input("Posicion (inicio/fin): ")
        index = 0 if posicion == "inicio" else -1
        identificador = uuid.uuid4().hex[:8]

        self.ll.insert(Paquete(identificador, destinatario), index)
        print("Paquete insertado al %s bajo el numero de guia '%s'" % (posicion, identificador))

    def do_eliminar(self, arg):
        identificador = input("Numero de guia: ")
        if self.ll.del_by_data(identificador):
            print("Eliminado con exito")
        else:
            print("No se encontro el paquete a eliminar")

    def do_buscar(self, arg):
        criterio = input("Criterio de busqueda (numero de guia/destinatario): ")
        valor = input("Buscar: ")
        if criterio == "numero de guia":
            field = "data"
        elif criterio == "destinatario":
            field = "destinatario"
        else:
            print("Error: Criterio invalido")
            return

        resultado = self.ll.get_by_data(data=valor, field=field)
        if resultado is None:
            print("No se encontro el %s: '%s'" % (criterio, valor))
        else:
            print('Numero de guia: %s' % resultado[1].data)
            print('Destinatario: %s' % resultado[1].destinatario)
            print('Posicion en la lista: %s' % resultado[0])


menu = Menu()
menu.cmdloop()
