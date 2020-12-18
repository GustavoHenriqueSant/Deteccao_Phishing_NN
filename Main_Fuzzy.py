import Rede_ART_Fuzzy_Modificada as RedeArtFuzzy
import Arquivo as leitor_arquivo
import metrics

#treino, treino_target = leitor_arquivo.lende_arquivo("/home/2018.1.08.014/Fuzzy_ART_modificada_Phishing_SemCodi/Train.txt")
#teste, teste_target = leitor_arquivo.lende_arquivo("/home/2018.1.08.014/Fuzzy_ART_modificada_Phishing_SemCodi/Test.txt")

#treino, treino_target = leitor_arquivo.lende_arquivo("C:\\Users\\Gustavo\\Desktop\\Fuzzy_ART_modificada_PhishingII\\Train.txt")
#teste, teste_target = leitor_arquivo.lende_arquivo("C:\\Users\\Gustavo\\Desktop\\Fuzzy_ART_modificada_PhishingII\\Test.txt")

#treino, treino_target = leitor_arquivo.lende_arquivo("C:\\Users\\Gustavo\\Desktop\\Fuzzy_cancer\\Train.txt")
#teste, teste_target = leitor_arquivo.lende_arquivo("C:\\Users\\Gustavo\\Desktop\\Fuzzy_cancer\\Test.txt")

#treino, treino_target = leitor_arquivo.lende_arquivo("C:\\Users\\Gustavo\\Desktop\\ic2.0\\DatasetPhishing\\train_data.txt")
#teste, teste_target = leitor_arquivo.lende_arquivo("C:\\Users\\Gustavo\\Desktop\\ic2.0\\DatasetPhishing\\test_data.txt")

'''
alpha = 0.3
beta = 0.1
rho = 0.99
rede = RedeArtFuzzy.Rede_ART_Fuzzy_Modificada(alpha, beta, rho)
rede.treina_rede(treino, treino_target)
rede.gerar_RotulosII()
rede.classificar(teste)
metrica = metrics.metrics()
metrica.cal_all_metrics(rede.classificacoes, teste_target)
print(metrica)
'''

alpha = 0.05
beta = 0.9
rho = 0.85
metrica = metrics.metrics()
for i in range(0, 10):
    treino, treino_target, teste, teste_target = leitor_arquivo.lendo_kfold("C:\\Users\\Gustavo\\Desktop\\ic2.0\\DatasetPhishing\\10Fold\\", i)
    rede = RedeArtFuzzy.Rede_ART_Fuzzy_Modificada(alpha, beta, rho)
    rede.treina_rede(treino, treino_target)
    rede.gerar_RotulosII()
    rede.classificar(teste)
    metrica.cal_all_metrics(rede.classificacoes, teste_target)
    print(metrica)


''' Fazendo a busca exaustiva do 10-fold:
metrica = metrics.metrics()
alpha = 0.05
while alpha < 1.0:
    arq_result = open(str(alpha) + ".txt", "a")
    print('\n___________________________________' + str(alpha) + '_______________________________________')
    beta = 0.05
    while beta < 1.0:
        rho = 0.05
        arq_result.write('\n_______BETA = ' + str(beta) + ' _______\n')
        print('\n_______BETA = ' + str(beta) + ' _______\n')
        while rho < 1.0:
            arq_result.write('rho = ' + str(rho))
            print('rho = ' + str(rho))
            lista_media_result_Kfold = []
            for i in range(0,10):
                treino, treino_target, teste, teste_target = leitor_arquivo.lendo_kfold("/home/2018.1.08.014/Fuzzy_ART_Modificada_10Fold_Phishing_SemNorm/10Fold/", i)
                rede = RedeArtFuzzy.Rede_ART_Fuzzy_Modificada(alpha, beta, rho)
                rede.treina_rede(treino, treino_target)
                rede.gerar_RotulosII()
                rede.classificar(teste)
                metrica.cal_all_metrics(rede.classificacoes, teste_target)
                metrica.add_metrics_in_listen(lista_media_result_Kfold)
            strin_10_fold = metrica.strin_10fold(lista_media_result_Kfold)
            arq_result.write(strin_10_fold + '\n\n')
            print(strin_10_fold)
            rho += 0.05
        beta += 0.05
    alpha += 0.05
'''

'''
alpha = 0.05
while alpha < 1.0:
    arq_result = open(str(alpha) + ".txt", "a")
    print('\n___________________________________' + str(alpha) + '_______________________________________')
    beta = 0.05
    while beta < 1.0:
        rho = 0.05
        arq_result.write('\n_______BETA = ' + str(beta) + ' _______\n')
        print('\n_______BETA = ' + str(beta) + ' _______\n')
        while rho < 1.0:
            arq_result.write('rho = ' + str(rho))
            print('rho = ' + str(rho))
            rede = RedeArtFuzzy.Rede_ART_Fuzzy_Modificada(alpha, beta, rho)
            rede.treina_rede(treino, treino_target)
            rede.gerar_RotulosII()
            rede.classificar(teste)
            metrica = metrics.metrics(rede.classificacoes, teste_target)
            metrica.cal_all_metrics()
            arq_result.write(metrica.__str__() + '\n\n')
            print(metrica)
            rho += 0.05
        beta += 0.05
    alpha += 0.05'''