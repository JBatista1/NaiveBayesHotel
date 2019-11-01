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
 Criar arrays com cada uma das categorias
 depois 
 get array pra saber se e spam
 
 Valor sempre retorna zero devido ao fato da multiplicacao ser muito pequena
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
        trainBad, trainNeutro, trainGood = self.SplitClass(xTrain, yTrain)
        vBad = self.CreateDictionayValue(trainBad)
        vNeutro = self.CreateDictionayValue(trainNeutro)
        vGood = self.CreateDictionayValue(trainGood)
        accurracy = 0
        for i in range(0, 15):
            classse = 0
            # bad = self.CalculateProbabilityOfBelongingToClass(xTest, list(set(vNeutro).union(set(vGood))), (trainGood + trainNeutro),i)
            # good = self.CalculateProbabilityOfBelongingToClass(xTest, list(set(vNeutro).union(set(vBad))), (trainNeutro + trainBad),i)
            # neutro = self.CalculateProbabilityOfBelongingToClass(xTest, list(set(vGood).union(set(vBad))), (trainGood + trainBad),i)
            bad = self.CalculateProbabilityOfBelongingToClass(xTest, list(set(vNeutro).union(set(vGood).union(vBad))),xTrain, i)
            good = self.CalculateProbabilityOfBelongingToClass(xTest, list(set(vNeutro).union(set(vGood).union(vBad))),xTrain, i)
            neutro = self.CalculateProbabilityOfBelongingToClass(xTest, list(set(vNeutro).union(set(vGood).union(vBad))),xTrain, i)
            if bad > good and bad > neutro:
                classse = 1
            elif neutro > bad and neutro > good:
                classse = 2
            else:
                classse = 3
            if classse == yTest[i]:
                accurracy += 1
        value = accurracy/15
        value *=100
        print(value)


        # return3 = self.CalculateProbabilityOfBelongingToClass(xTest, dictionaryClass, trainDataSet)
        # print(result)
        # print(value[0])
        # for i in range(0,len(value[0])-1):
        #     print(value[0][i])
        # print(self.dictionary)
        # print(len(self.dictionary))

    def CalculateProbabilityOfBelongingToClass(self, array, dictionaryClass, xTrain,element):
        xTestNumberRepresentation = self.CreateArrayNumericRepresentation(array, dictionaryClass)
        numberOfElementsOfEachWord = self.NumberElementInTrain(xTrain, dictionaryClass)
        value = self.CalculateEstimate(xTestNumberRepresentation[element],numberOfElementsOfEachWord,len(xTrain))
        return value

    def NumberElementInTrain(self, xTrain, dic):
        sizeTrainDataser = len(xTrain)
        sizeDictionary = len(dic)-1
        numberOfElementsOfEachWord = list()
        for i in range(0,sizeDictionary):
            numberOfTimesTheWordRepeats = 0
            for j in range(0, sizeTrainDataser):
                if dic[i] in xTrain[j]:
                    numberOfTimesTheWordRepeats += 1
            numberOfElementsOfEachWord.append(numberOfTimesTheWordRepeats)

        return  numberOfElementsOfEachWord

    def CalculateEstimate(self,xTestNumberRepresentation,numberOfElementsOfEachWord, sizeDataSetTrain):
        size = len(numberOfElementsOfEachWord)-1
        toBelong = 1.0
        for i in range(0, size):
            teta = numberOfElementsOfEachWord[i] / sizeDataSetTrain
            teta = round(teta,8)
            if xTestNumberRepresentation[i] == 0:
                toBelong *= teta
                teta = round(toBelong, 8)
                if toBelong < 0.0001:
                    toBelong *=10000000
            else:
                toBelong *= (1-teta)
                teta = round(toBelong, 8)
                if toBelong < 0.0001:
                    toBelong *= 10000000

        return toBelong

    def SplitClass(self,xTrain,yTrain):
        size = len(xTrain)-1
        reviewNeutral = list()
        reviewBad = list()
        reviewGood = list()
        trainNeutral = list()
        trainBad = list()
        trainGood = list()

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


    def CreateArrayNumericRepresentation(self, array,dictionary):
        sizeDictionary = len(dictionary) - 1
        sizeXtrain = len(array) - 1
        arrayDataset = list()

        for i in range(0, sizeXtrain):
            stringComment = array[i].split()
            arrayDataset.append(self.verifyStringInDictionary(stringComment,dictionary))
        return arrayDataset

    def verifyStringInDictionary(self, array, dictionary):
        sizeArray = len(array) - 1
        sizeDictionary = len(dictionary)
        arrayValue = np.zeros(sizeDictionary, dtype=int)
        for i in range(0, sizeArray):
            if array[i] in dictionary:
                arrayValue[i] = 1
        return arrayValue


value = generateDataSet("chennai_reviews.csv")
