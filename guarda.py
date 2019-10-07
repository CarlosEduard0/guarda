import os
import pickle


class Guarda:
    def __init__(self, pasta, algHash, saida, senha):
        self.pasta = pasta
        self.algHash = algHash
        self.saida = saida
        self.hashs = {}
        self.senha = senha
        self.relatorio = list()
    
    def criarGuarda(self):
        if os.path.isfile(self.arquivoGuarda()):
            print('Pasta já está protegida pelo guarda.')
            exit(1)

    def carregarGuarda(self):
        if not os.path.isfile(self.arquivoGuarda()):
            print('Pasta não está sendo protegida pelo guarda.')
            exit(0)
        with open(self.arquivoGuarda(), 'rb') as f:
            self.hashs = pickle.load(f)

    def fazerRastreio(self):
        for root, dirs, files in os.walk(self.pasta):
            for file in files:
                if file != '.guarda':
                    caminhoArquivo = '{}/{}'.format(root, file)
                    hashArquivo = self.algHash(caminhoArquivo) if self.senha == '' else self.algHash(caminhoArquivo, self.senha)
                    statusArquivo = self.getStatusArquivo(caminhoArquivo, hashArquivo)
                    if statusArquivo != None:
                        self.relatorio.append(statusArquivo)
                    self.hashs[caminhoArquivo] = hashArquivo
        self.verificarArquivosDeletados()
        self.imprimirRelatorio()

    def salvarGuarda(self):
        with open(self.arquivoGuarda(), 'wb') as f:
            pickle.dump(self.hashs, f)

    def removerGuarda(self):
        if os.path.isfile(self.arquivoGuarda()):
            os.remove(self.arquivoGuarda())
            print('Guarda removido.')
        else:
            print('Essa pasta não está protegida pelo Guarda.')

    def verificarArquivosDeletados(self):
        registrosParaDeletar = list()
        for chave, valor in self.hashs.items():
            if not os.path.isfile(chave):
                registrosParaDeletar.append(chave)
                self.relatorio.append('[R] {}'.format(chave))
        for i in registrosParaDeletar:
            del self.hashs[i]

    def imprimirRelatorio(self):
        if self.saida != '':
            with open(saida, 'w') as f:
                for i in self.relatorio:
                    f.write(i)
        else:
            # print(self.relatorio)
            for i in self.relatorio:
                print(i)


    def getStatusArquivo(self, caminhoArquivo, hash):
        if caminhoArquivo not in self.hashs:
            return '[N] {}'.format(caminhoArquivo)
        elif self.hashs[caminhoArquivo] != hash:
            return '[A] {}'.format(caminhoArquivo)
        else:
            return None

    def arquivoGuarda(self):
        return '{}/.guarda'.format(self.pasta)
