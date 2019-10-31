import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
'''
 PASSOS PARA CRIAR DADOS:
 Carregar os dados necessarios: Review_text e Sentimet"
 Criar dados de treinamento e de teste
 Criar um Set para evitar criar palavras repetidas
 Criar array a partir do Set para organizalo
 Organizar array
 
 
 Foi necessario nomear todas as colunas para que conseguisse pegar od dados de forma mais facil, todas as colunas 
foram nomeadas de acordo com os dados do site https://www.kaggle.com/ranjitha1/hotel-reviews-city-chennai a qual baixamos
o csv, as categorias criadas foram:
    Hotel_name
    Review_Title
    Review_Text
    Sentiment
    Rating_Percentage
'''
class generateDataSet:
    def __init__(self, datasetName):
        self.datasetName = datasetName
        xTrain, yTrain, xTest, yTest  = self.ManagerData()

    def ManagerData(self):
        text = pd.read_csv(self.datasetName)
        #Cria conjunto de dados para treino e para test
        train, test = train_test_split(text, test_size=0.20)

        #Cria o dado que serão utilizados para treinameto somente com as infomações necessarias no caso Review_Text
        xTrain = train.Review_Text
        yTrain = train.Sentiment
        #Cria o dado que serão utilizados para teste somente com as infomações necessarias no caso Sentiment
        xTest = test.Review_Text
        yTest = test.Sentiment
        return xTrain,yTrain,xTest,yTest



value = generateDataSet("chennai_reviews.csv")
