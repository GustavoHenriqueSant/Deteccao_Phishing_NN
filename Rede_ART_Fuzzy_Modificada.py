class Rede_ART_Fuzzy_Modificada():
    def __init__(self, alpha, beta, rho):
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.matrizPeso = []
        self.Ncat = 0
        self.vencedores = []
        self.soma_Rotulos = []
        self.quantidadeDe = []
        self.rotulos = []
        self.classificacoes = []

    def modulo(self, vetor):
        modulado = 0.0
        for i in vetor:
            modulado += abs(i)
        return modulado

    def codificacao(self, entrada_atual):

        def normalizacao(vetor_modulado, vetor):
            normalizado = []

            for i in vetor:
                normalizado.append(i/vetor_modulado)

            return normalizado

        #I = normalizacao(self.modulo(entrada_atual), entrada_atual)
        I = entrada_atual
        tam_I = len(I)
        for i in range(0, tam_I):
            I.append(1 - I[i])

        return I

    def inicializacao_dos_pesos(self, treino, treino_target):
        self.matrizPeso.append(self.codificacao(treino[0]))
        self.Ncat += 1
        self.vencedores.append(0)
        self.soma_Rotulos.append(treino_target[0])
        self.quantidadeDe.append(1)

    def and_nebuloso(self, vetorI, vetorII):
        resultado = []
        try:
            for i in range(0,len(vetorI)):
                resultado.append(min(vetorI[i], vetorII[i]))
        except:
            print("O tamanho dos vetores nao sao iguais")

        return resultado

    def montagem_das_categorias(self, entrada_codificada):
        T = []
        for i in self.matrizPeso:
            modulo_nebuloso_I_W = self.modulo(self.and_nebuloso(entrada_codificada,i))
            soma_alfa_modulo_W = self.alpha + self.modulo(i)
            T.append(modulo_nebuloso_I_W/soma_alfa_modulo_W)

        return T

    def teste_de_vigilancia(self, entrada_codificada, index_vencedor):
        modulo_I_W = self.modulo(self.and_nebuloso(entrada_codificada, self.matrizPeso[index_vencedor]))
        modulo_I = self.modulo(entrada_codificada)
        return (modulo_I_W/modulo_I) >= self.rho

    def ressonancia_adaptativa(self, entrada_codificada, index_categoria_vencedora):
        '''Metodo para multiplicar um vetor por uma constante. Ela retorna um lista, com tds os valores do vetor multiplicados pela constante'''
        def mult_vetor_const(const, vetor):
            mult = []
            for i in vetor:
                mult.append(const * i)

            return mult

        '''Metodo para somar dois vetores. Retorna uma lista com os valores do indice referente dos dois vetores.'''
        def soma_de_vetores(vetorI, vetorII):
            soma = []
            for i in range(0, len(vetorI)):
                soma.append(vetorI[i] + vetorII[i])

            return soma

        and_nebuloso_I_W = self.and_nebuloso(entrada_codificada, self.matrizPeso[index_categoria_vencedora])
        beta_X_deCima = mult_vetor_const(self.beta, and_nebuloso_I_W)
        umMenosBeta_X_W = mult_vetor_const(1 - self.beta, self.matrizPeso[index_categoria_vencedora])
        self.matrizPeso[index_categoria_vencedora] = soma_de_vetores(beta_X_deCima, umMenosBeta_X_W)

    def treina_rede(self, treino, treino_target):
        self.inicializacao_dos_pesos(treino, treino_target)

        k = 1
        for i in treino[1:]:
            Ncont = 1
            I = self.codificacao(i)
            T = self.montagem_das_categorias(I)
            flag = True
            while(flag):
                indice_categoria_vencedora = T.index(max(T))
                if self.teste_de_vigilancia(I, indice_categoria_vencedora):
                    self.ressonancia_adaptativa(I, indice_categoria_vencedora)
                    self.vencedores.append(indice_categoria_vencedora)
                    self.soma_Rotulos[indice_categoria_vencedora] += treino_target[k]
                    self.quantidadeDe[indice_categoria_vencedora] += 1
                    flag = False
                else:
                    if Ncont < self.Ncat:
                        Ncont += 1
                        T[indice_categoria_vencedora] = 0
                    else:
                        self.Ncat += 1
                        self.matrizPeso.append(I)
                        self.vencedores.append(len(self.matrizPeso) - 1)
                        self.soma_Rotulos.append(treino_target[k])
                        self.quantidadeDe.append(1)
                        flag = False
            k += 1

    '''Mpetodo responsavel pela geracao de rotulos apos o treinamento. e o mesmo metodo do vitao.'''
    def gerar_rotulos(self, treino_target):
        """"Gera o rotulo de cada neuronio, rotulos de treino e vencedores sao na ordem das entradas para treino"""
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
            """O for de i percorre a lista de vencedores ata o final"""
            if self.vencedores[i] not in excesao:  # se e um valor ainda nao encontrado buscamos rotular
                cont = treino_target[i]  # cont = valor de rotulo do novo neuronio
                for j in range(i + 1, len(self.vencedores)):
                    """percorre o restante da lista de vencedores buscando por novos elementos iguais"""
                    if self.vencedores[i] == self.vencedores[j]:
                        cont += treino_target[j]
                if cont < quantidade[self.vencedores[i]] / 2:
                    self.rotulos.append(0)
                else:
                    self.rotulos.append(1)
                excesao.append(self.vencedores[i])

    def gerar_RotulosII(self):
        for i in range(0, len(self.quantidadeDe)):
            if self.soma_Rotulos[i] < (self.quantidadeDe[i]/2):
                self.rotulos.append(0.0)
            else:
                self.rotulos.append(1.0)

    '''Metodo responsavel pela analise.'''
    def classificar(self, entrada_analise):
        for i in entrada_analise:
            I = self.codificacao(i)
            lista_categoria = self.montagem_das_categorias(I)
            indice_w = lista_categoria.index(max(lista_categoria))
            self.classificacoes.append(self.rotulos[indice_w])
