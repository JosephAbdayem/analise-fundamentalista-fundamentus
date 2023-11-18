import sys
import threading
import time
from itertools import cycle

class WaitingBar:
    '''
    Classe para exibir uma barra de espera animada durante a execução de tarefas demoradas.

    Uso:
    barra = WaitingBar('Sua mensagem aqui')
    # Realizar uma tarefa lenta aqui
    barra.stop()

    Autor: phoemur - 2016
    '''

    def __init__(self, mensagem='[*] Aguarde até o carregamento ser concluído...'):
        self.mensagem = ' ' + str(mensagem)
        self.ciclos = cycle('-\\|/')
        self.evento = threading.Event()
        self.barra = threading.Thread(target=self.iniciar)
        self.barra.start()

    def iniciar(self):
        for _ in cycle(self.mensagem):
            if self.evento.is_set():
                break
            sys.stdout.write(self.mensagem + next(self.ciclos) + '\r')
            time.sleep(0.05)
            sys.stdout.flush()

    def stop(self):
        self.evento.set()
        self.barra.join()
        sys.stdout.write(self.mensagem + '\n')

if __name__ == '__main__':
    # Exemplo de uso
    barra = WaitingBar('[*] Calculando algo demorado...')
    # Finalizando a barra e continuando o programa
    barra.stop()
