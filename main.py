import rede as rd
import Metricas as mt
import numpy
import  leitor_de_arquivos as lq

treino, treino_target = lq.lende_arquivo("C:\\Users\\Gustavo\\Desktop\\Fuzzy_cancer\\Train.txt")
analise, analise_target = lq.lende_arquivo("C:\\Users\\Gustavo\\Desktop\\Fuzzy_cancer\\Test.txt")

rede_Euclidiana = rd.Rede_Euclidiana(0.2, 0.01)
rede_Euclidiana.treinar_rede(treino, treino_target)
rede_Euclidiana.gerar_rotulos(treino_target)
print("Rótulos gerados:")
print(rede_Euclidiana.rotulos)
print(rede_Euclidiana.Ncat)
classificacoes = rede_Euclidiana.classificar(analise)
metrics = mt.metrics()
metrics.cal_all_metrics(classificacoes, analise_target)
print(metrics)

'''
rho = 0.05
while rho <= 0.5:
    rede = rd.Rede_Euclidiana(0.15,rho)
    metrics = mt.Metricas()
    rede.treinar_rede(treino, treino_target)
    resultados = rede.classificar(analise)
    metrics.calcular_valores(resultados, analise_target)
    print("____Para rho = {}___".format(str(rho)))
    print(" ACRT     TP__    TN__     FP__     FN__     ACC_     Esp_     Sens     MCC_  ")
    print(str(metrics))
    print(rede.Ncat)
    print("\n\n\n")
    rho += 0.01
'''



'''Criando objetos'''
'''
rede = rd.Rede_Euclidiana(0.1, 0.09)
metrics = mt.Metricas()

rede.treinar_rede(treino,treino_target)
resultados = rede.classificar(analise)
metrics.calcular_valores(resultados,analise_target)
print(" ACRT     TP__     TN__     FP__     FN__     ACC_     Esp_     Sens     MCC_     FSOC")
print(str(metrics))
print(resultados)
'''

'''
for i in range(0,10):
    treino,treino_target,analise,analise_target = lq.lendo_kfold("C:\\Users\\Gustavo\\Desktop\\ic2.0\\Dataset10fold\\", i)
    rede.treinar_rede(treino,treino_target)
    resultados = rede.classificar(analise)
    metrics.calcular_valores(resultados,analise_target)
    print("RESULTADOS PARA O FOLD {} DE VALIDAÇÃO".format(str(i)))
    print(str(metrics))
'''