import numpy as np
import math

class Rede_Euclidiana():
    def __init__(self, beta, rho):
        self.beta = beta
        self.rho = rho
        self.Ncat = 0
        '''Matriz que contém os valores de cada cluster.'''
        self.matrizPeso = []
        '''Lista q armazena para qual cluster cada instância do treinamento foi. Se no index 2 armazenar o valor 1, significa que a instância 2 do treinamento foi para o cluster 1'''
        self.vencedores = []
        '''Armazena o rótulo de cada cluster. feito após o treinamento.'''
        self.rotulos = []
        self.quantidade = []
        self.somaRotulos = []

    '''Método responsável por fazer a ressonância adaptativa. Modifica a matrizPeso (reoresenta os clusters) do objeto.'''
    def ressonancia_adaptativa(self, index_categoria_vencedora, entrada_atual):
        '''Método para multiplicar um vetor por uma constante. Ela retorna um lista, com tds os valores do vetor multiplicados pela constante'''
        def mult_vetor_const(const, vetor):
            mult = []
            for i in vetor:
                mult.append(const * i)

            return mult

        '''Método para somar dois vetores. Retorna uma lista com os valores do índice referente dos dois vetores.'''
        def soma_de_vetores(vetorI, vetorII):
            soma = []
            for i in range(0, len(vetorI)):
                soma.append(vetorI[i] + vetorII[i])

            return soma

        '''Beta vezes a entrada atual.'''
        beta_x_entrada = mult_vetor_const(self.beta, entrada_atual)
        '''(1 -  beta) multiplicado pelo cluster candidato '''
        beta_x_W = mult_vetor_const(1 - self.beta, self.matrizPeso[index_categoria_vencedora])
        '''Atualizando a matriz dos clusters com a soma dos vetores calculados a cima.'''
        self.matrizPeso[index_categoria_vencedora] = soma_de_vetores(beta_x_entrada, beta_x_W)

    '''Método responsável por calcular o peso Mj. Retorna um float (o peso Mj)'''
    '''Categoria = lista q armazena todos os Tj de cada categoria.'''
    def calculo_de_similaridade(self, categoria, index_categoira_vencedora, entrada_atual):
        '''Método responsável por fazer o somatório de todos os valores de um vetor ao quadrado. Retorna um número real.'''
        def somatoria_vetor_ao_quadrado(vetor):
            somatorio = 0
            for i in vetor:
                somatorio += i ** 2
            return somatorio

        '''Somatório dos valores da entrada atual ao quadrado.'''
        somatorio_da_entrada = somatoria_vetor_ao_quadrado(entrada_atual)
        '''Somatório dos valores do cluster cadidato ao quadrado.'''
        somatorio_do_neuronio = somatoria_vetor_ao_quadrado(self.matrizPeso[index_categoira_vencedora])
        '''Fazendo o cálculo de Mj com o menor somatório.'''
        return categoria[index_categoira_vencedora]/max(math.sqrt(somatorio_da_entrada), math.sqrt(somatorio_do_neuronio))

    '''Método responsável pela criação do array T. Retorna um vetor'''
    def montagem_das_categorias(self, entrada_atual):
        '''Método responsável por fazer a diferença de dois vetores ao quadrado. Retorna um vetor'''
        def diferenca_vetores_ao_quadrado(vetorI, vetorII):
            diferenca_quadrada = []
            for i in range(0,len(vetorI)):
                diferenca_quadrada.append((vetorI[i] - vetorII[i]) ** 2)
            return diferenca_quadrada

        categorias = []
        '''Montagem das categorias, usando cada uma delas q estão na MatrizPeso do objeto.'''
        for i in self.matrizPeso:
            categorias.append(math.sqrt(sum(diferenca_vetores_ao_quadrado(entrada_atual, i))))
        return categorias

    '''Método responsável pela iniciação do treinamento.'''
    '''Primeira_Entrada = uma lista com os valores da primeira instância do treinamento.'''
    def inicializacao_Pesos(self, primeira_Entrada, primeiro_target):
        self.matrizPeso.append(primeira_Entrada)
        self.Ncat += 1
        self.vencedores.append(0)
        self.somaRotulos.append(primeiro_target)
        self.quantidade.append(1)

    '''Método responsável por realizar o treinamento da rede.'''
    '''Treino = lista de listas, possui todo os valores do dataset de treinamento. Treino_target = lista que armazena o rótulo de tds as instâncias do dataset de treinamento'''
    def treinar_rede(self, treino, treino_target):
        #Inicialização dos pesos com a primeira entrada;
        '''Iniciando o treinamento.'''
        self.inicializacao_Pesos(treino[0], treino_target[0])

        '''Para todas as entradas do dataset de treinamento faça. A primeira instância foi usada para o primeiro cluster, por isso o for começa com 1.'''
        k = 1
        for i in treino[1:]:
            Ncont = 1
            categorias = self.montagem_das_categorias(i)
            flag = True
            while (flag):
                index_categoria_vencedora = categorias.index(min(categorias))
                similaridade_peso_M = self.calculo_de_similaridade(categorias,index_categoria_vencedora,i)
                '''Teste de vigilância.'''
                if(similaridade_peso_M < self.rho):
                    self.ressonancia_adaptativa(index_categoria_vencedora, i)
                    self.vencedores.append(index_categoria_vencedora)
                    self.quantidade[index_categoria_vencedora] += 1
                    self.somaRotulos[index_categoria_vencedora] += treino_target[k]
                    flag = False
                else:
                    '''Caso o cluster cadidato não passe no teste de vigilância'''
                    if Ncont < self.Ncat:
                        '''Existem outras categorias que ainda não foram testadas:'''
                        Ncont += 1
                        categorias[index_categoria_vencedora] = 1000000.0
                    else:
                        '''Caso for preciso criar uma nova categoria'''
                        self.Ncat += 1
                        self.matrizPeso.append(i)
                        self.vencedores.append(len(self.matrizPeso) - 1)
                        self.quantidade.append(1)
                        self.somaRotulos.append(treino_target[k])
                        flag = False
            k += 1

    '''Mpetodo responsável pela geração de rótulos após o treinamento. É o mesmo método do vitão.'''
    def gerar_rotulos(self, treino_target: list) -> list:
        """"Gera o rotulo de cada neuronio, rotulos de treino e vencedores são na ordem das entradas para treino"""
        excesao = []
        quantidade = []
        for i in range(len(self.vencedores)):
            """Este for constroi a quantidade de vezes que cada neuronio foi o vencedor"""
            if self.vencedores[i] not in excesao:
                quantidade.append(1)
                excesao.append(self.vencedores[i])
                for j in range(i + 1, len(self.vencedores)):
                    if self.vencedores[i] == self.vencedores[j]:
                        quantidade[self.vencedores[i]] += 1

        excesao.clear()  # Limpa o lista de excessao para uso abaixo
        for i in range(len(self.vencedores)):
            """O for de i percorre a lista de vencedores até o final"""
            if self.vencedores[i] not in excesao:  # se é um valor ainda nao encontrado buscamos rotular
                cont = treino_target[i]  # cont = valor de rotulo do novo neuronio
                for j in range(i + 1, len(self.vencedores)):
                    """percorre o restante da lista de vencedores buscando por novos elementos iguais"""
                    if self.vencedores[i] == self.vencedores[j]:
                        cont += treino_target[j]
                if cont >= quantidade[self.vencedores[i]] / 2:
                    self.rotulos.append(1)
                else:
                    self.rotulos.append(0)
                excesao.append(self.vencedores[i])

    def gerar_RotulosII(self):
        for i in range(len(self.quantidadeDe)):
            if self.soma_Rotulos[i] < (self.quantidadeDe[i]/2):
                self.rotulos.append(0.0)
            else:
                self.rotulos.append(1.0)

    '''Método responsável pela análise.'''
    def classificar(self, entrada_analise):
        classificacoes = []
        for i in entrada_analise:
            lista_categoria = self.montagem_das_categorias(i)
            indice_w = lista_categoria.index(min(lista_categoria))
            classificacoes.append(self.rotulos[indice_w])
        return classificacoes


