import math


class metrics():
    def __init__(self):
        self.total_acertos = 0
        self.true_positive = 0
        self.false_positive = 0
        self.true_negative = 0
        self.false_negative = 0
        self.acuracia = 0.0
        self.especificidade = 0.0
        self.sensitividade = 0.0
        self.MCC = 0.0
        self.F_score = 0.0

    def cal_total_acertos(self, resultado_analise, test_target):
        try:
            self.total_acertos = 0
            for i in range(0, len(test_target)):
                if test_target[i] == resultado_analise[i]:
                    self.total_acertos += 1
        except:
            print('Erro na classificacao, a lista de resultado e target nao possuem o mesmo tamanho.')

    def cal_decision_matrix(self, resultado_analise, test_target):
        self.true_negative = 0
        self.true_positive = 0
        self.false_negative = 0
        self.false_positive = 0
        for i in range(0, len(test_target)):
            if test_target[i] == resultado_analise[i]:
                if test_target[i] == 1:
                    self.true_positive += 1
                else:
                    self.true_negative += 1
            else:
                if test_target[i] == 1:
                    self.false_negative += 1
                else:
                    self.false_positive += 1

    def cal_acuracia(self, resultado_analise):
        try:
            self.acuracia = self.total_acertos / len(resultado_analise)
        except:
            self.acuracia = 0.0

    def cal_sensibilidade(self):
        try:
            self.sensitividade = self.true_positive / (self.true_positive + self.false_negative)
        except:
            self.sensitividade = 0.0

    def cal_especificidade(self):
        try:
            self.especificidade = self.true_negative / (self.false_positive + self.true_negative)
        except:
            self.especificidade = 0.0

    def cal_MCC(self):
        try:
            TP = self.true_positive
            TN = self.true_negative
            FP = self.false_positive
            FN = self.false_negative
            dividendo = ((TP * TN) - (FP * FN))
            divisor = (math.sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN)))
            self.MCC = dividendo / divisor
        except:
            self.MCC = 0.0

    def cal_F_Score(self):
        def cal_precision():
            try:
                return self.true_positive / (self.true_positive + self.false_positive)
            except:
                return 0.0

        precision = cal_precision()
        try:
            self.F_score = 2 * ((precision * self.sensitividade) / (precision + self.sensitividade))
        except:
            self.F_score = 0.0

    def __str__(self):
        string = 'TA:' + str(self.total_acertos)
        string += ' ACC:' + str(round(self.acuracia, 4))
        string += ' TP:' + str(self.true_positive)
        string += ' TN:' + str(self.true_negative)
        string += ' FP:' + str(self.false_positive)
        string += ' FN:' + str(self.false_negative)
        string += ' ESP:' + str(round(self.especificidade, 4))
        string += ' Sens:' + str(round(self.sensitividade, 4))
        string += ' MCC:' + str(round(self.MCC, 4))
        string += ' FS:' + str(round(self.F_score, 4)) + '\n'

        return string

    def cal_all_metrics(self, resultado_analise, test_target):
        self.cal_total_acertos(resultado_analise, test_target)
        self.cal_decision_matrix(resultado_analise, test_target)
        self.cal_acuracia(resultado_analise)
        self.cal_sensibilidade()
        self.cal_especificidade()
        self.cal_MCC()
        self.cal_F_Score()

    def add_metrics_in_listen(self, lista):
        lista_auxiliar = []
        lista_auxiliar.append(self.total_acertos)
        lista_auxiliar.append(self.true_positive)
        lista_auxiliar.append(self.true_negative)
        lista_auxiliar.append(self.false_positive)
        lista_auxiliar.append(self.false_negative)
        lista_auxiliar.append(self.acuracia)
        lista_auxiliar.append(self.sensitividade)
        lista_auxiliar.append(self.especificidade)
        lista_auxiliar.append(self.MCC)
        lista_auxiliar.append(self.F_score)

        lista.append(lista_auxiliar)

    def strin_10fold(self, lista_media_10fold):
        lista_soma_metricas = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        for i in lista_media_10fold:
            for j in range(0,len(i)):
                lista_soma_metricas[j] += i[j]

        for i in range(len(lista_soma_metricas)):
            lista_soma_metricas[i] = lista_soma_metricas[i]/10

        string = 'TA:' + str(lista_soma_metricas[0])
        string += ' TP:' + str(lista_soma_metricas[1])
        string += ' TN:' + str(lista_soma_metricas[2])
        string += ' FP:' + str(lista_soma_metricas[3])
        string += ' FN:' + str(lista_soma_metricas[4])
        string += ' ACC:' + str(round(lista_soma_metricas[5], 4))
        string += ' Sens:' + str(round(lista_soma_metricas[6], 4))
        string += ' ESP:' + str(round(lista_soma_metricas[7], 4))
        string += ' MCC:' + str(round(lista_soma_metricas[8], 4))
        string += ' FS:' + str(round(lista_soma_metricas[9], 4)) + '\n'

        return string