def lende_arquivo(path):
    arq = open(path, 'r')
    train = []
    train_target = []

    for i in arq:
        words = i.split()
        train.append(words[0:len(words) - 1])
        train_target.append(float(words[len(words) - 1]))

    for i in range(0, len(train)):
        for j in range(0, len(train[i])):
            train[i][j] = float(train[i][j])

    return train, train_target

def lendo_kfold(path, index_valid):
    train = []
    train_target = []
    analise = []
    analise_target = []

    for i in range(0,10):
        arq = open(path + str(i) + '.csv', 'r')
        if i != index_valid:
            for j in arq:
                words = j.split(",")
                train.append(words[0:len(words) - 1])
                train_target.append(float(words[len(words) - 1]))
        else:
            for j in arq:
                words = j.split(",")
                analise.append(words[0:len(words) - 1])
                analise_target.append(float(words[len(words) - 1]))

    for i in range(0, len(train)):
        for j in range(0, len(train[i])):
            train[i][j] = float(train[i][j])

    for i in range(0, len(analise)):
        for j in range(0, len(analise[i])):
            analise[i][j] = float(analise[i][j])

    return train, train_target, analise, analise_target