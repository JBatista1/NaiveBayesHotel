import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import enchant
'''
 PASSOS PARA CRIAR DADOS:
 Carregar os dados necessarios: Review_text e Sentimet"
 Criar dados de treinamento e de teste
 Criar um Set para evitar criar palavras repetidas
 Criar array a partir do Set para organizalo
 Organizar array
 
 mais de 1 bilhão de interações
 
 Remover as palavras que não são em ingles
 remover as palavras pequenas 
 Bug que eu comparava cada letra com o array
 
 get array pra saber se e spam
 
 Foi necessario nomear todas as colunas para que conseguisse pegar od dados de forma mais facil, todas as colunas 
foram nomeadas de acordo com os dados do site https://www.kaggle.com/ranjitha1/hotel-reviews-city-chennai a qual baixamos
o csv, as categorias criadas foram:
    Hotel_name
    Review_Title
    Review_Text
    Sentiment
    Rating_Percentage
    
    Classify in Y
    1 = bad
    2 = normal
    3 = good    

'''
class generateDataSet:
    def __init__(self, datasetName):
        self.datasetName = datasetName

        xTrain, yTrain, xTest, yTest  = self.ManagerData()
        dicBad, dicNeutro, dicGood = self.SplitClass(xTrain, yTrain)

        print(len(dicNeutro))
        print(len(dicGood))
        print(len(dicBad))
        vBad = self.CreateDictionayValue(dicBad)

        vNeutro = self.CreateDictionayValue(dicNeutro)
        vGood = self.CreateDictionayValue(dicGood)
        teste = self.CreateDictionayValue(xTrain)
        print(vBad)
        print(vNeutro)
        print(vGood)
        print(teste)
        # value = self.createDataSEtWithArray(xTest)
        # print(value[0])
        # for i in range(0,len(value[0])-1):
        #     print(value[0][i])
        # print(self.dictionary)
        # print(len(self.dictionary))


    def SplitClass(self,xTrain,yTrain):
        size = len(xTrain)-1
        reviewNeutral = list()
        reviewBad = list()
        reviewGood = list()

        for i in range(0, size):
            # Verify if bad review
            if yTrain[i] == 1:
                reviewBad.append(xTrain[i])
            elif yTrain[i] == 2:
                reviewNeutral.append(xTrain[i])
            else:
                reviewGood.append(xTrain[i])
        return reviewBad,reviewNeutral,reviewGood

    def verifyIFExistOne(self, array):
        size = len(array)-1
        for i in range(0, size):
            if array[i] == 1:
                print("Existe 1, in position", i)

    def ManagerData(self):
        data = pd.read_csv(self.datasetName)

        #Cria conjunto de dados para treino e para test
        train, test = train_test_split(data, test_size=0.20)

        #Cria o dado que serão utilizados para treinameto somente com as infomações necessarias no caso Review_Text
        xTrain = train["Review_Text"].tolist()
        yTrain = train["Sentiment"].tolist()
        #Cria o dado que serão utilizados para teste somente com as infomações necessarias no caso Sentiment
        xTest = test["Review_Text"].tolist()
        yTest = test["Sentiment"].tolist()

        return xTrain,yTrain,xTest,yTest

    def CreateDictionayValue(self, arrayString):
        size = len(arrayString) - 1
        dataset = set()
        for i in range(0,size):
            stringSplit = arrayString[i].split()
            dataset = dataset.union(set(stringSplit))
        dictionary = list(dataset)
        sorted(dictionary)
        dictionary = self.RemoveNoise(dictionary)
        return dictionary

    def RemoveNoise(self, array):
        sizeArray = len(array) - 1
        arrayDataset = list()
        dictionary_en_US = enchant.Dict("en_US")
        for i in range(0, sizeArray):
           if len(array[i]) <= 18 and len(array[i]) >= 3 and dictionary_en_US.check(array[i]):
               arrayDataset.append(array[i])
        return arrayDataset


    def createDataSEtWithArray(self, xTrain):
        sizeDictionary = len(self.dictionary) - 1
        sizeXtrain = len(xTrain) - 1
        arrayDataset = list()

        for i in range(0, sizeXtrain):
            stringComment = xTrain[i].split()
            arrayDataset.append(self.verifyStringInDictionary(stringComment))
        return arrayDataset

    def verifyStringInDictionary(self, xTrain):
        sizeXtrain = len(xTrain) - 1
        sizeDictionary = len(self.dictionary) - 1
        arrayValue = np.zeros(sizeDictionary, dtype=int)
        for i in range(0, sizeXtrain):
            for j in range(0, sizeDictionary):
                if xTrain[i] == self.dictionary[j]:
                    arrayValue[j] = 1
        return arrayValue


value = generateDataSet("chennai_reviews.csv")
