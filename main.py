import sys
import hmac
import getopt
import hashlib
from guarda import Guarda


def md5(caminhoArquivo):
    hash_md5 = hashlib.md5()
    with open(caminhoArquivo, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def hmacc(caminhoArquivo, senha):
    m = hmac.new(senha.encode(), digestmod=hashlib.blake2s)
    with open(caminhoArquivo, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            m.update(chunk)
    return m.hexdigest()

metodo = ''
opcao = ''
pasta = ''
saida = ''
senha = ''

opcoes, restantes = getopt.getopt(sys.argv[1:], 'i:t:x:o:', ['hash', 'hmac='])
for opt, args in opcoes:
    if opt in ('--hash', '--hmac'):
        metodo = [opt, args]
    elif opt in ('-i', '-t', '-x'):
        opcao = opt
        pasta = args
    elif opt == '-o':
        saida = args

if (opcao in ('-i', '-t') and metodo == '') or opcao == '' or pasta == '':
    print("""Uso: ./guarda <metodo> <opcao> <pasta> <saída>
― <metodo>: indica o método a ser utilizado ( --hash ou --hmac senha)
― <opcao>: indica a ação a ser desempenhada pelo programa
    -i: inicia a guarda da pasta indicada em <pasta>
    -t: faz o rastreio (tracking) da pasta indicada em <pasta>, inserindo informações sobre novos arquivos e indicando
        alterações detectadas/exclusões
    -x: desativa a guarda e remove a estrutura alocada
― <pasta> : indica a pasta a ser “guardada”
― <saida> : indica o arquivo de saída para o relatório (-o saída).""")
    exit(1)

algHash = ''
if opcao != '-x':
    if metodo[0] == '--hash':
        algHash = md5
    elif metodo[0] == '--hmac':
        algHash = hmacc
        senha = metodo[1]

guarda = Guarda(pasta, algHash, saida, senha)
if opcao == '-i':
    guarda.criarGuarda()
    guarda.fazerRastreio()
    guarda.salvarGuarda()
elif opcao == '-t':
    guarda.carregarGuarda()
    guarda.fazerRastreio()
    guarda.salvarGuarda()
elif opcao == '-x':
    guarda.removerGuarda()