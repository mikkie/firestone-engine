import cmath
import numpy as np

class TopsisUtil(object):
    
    
    @staticmethod
    def commonCalc(df, columnName, weight, positive):
        temp = cmath.sqrt((df[columnName] * df[columnName]).sum())  
        #wi*ri
        if temp == 0:
            df[columnName + '_vi'] = weight * 0
        else:
            df[columnName + '_vi'] = weight * df[columnName] / temp
        #vi+, vi-
        if positive == True:
            df[columnName + '_best'] = df[columnName + '_vi'].max()
            df[columnName + '_worst'] = df[columnName + '_vi'].min()
        else:          
            df[columnName + '_best'] = df[columnName + '_vi'].min()
            df[columnName + '_worst'] = df[columnName + '_vi'].max()


    @staticmethod
    def calcDi(row, columnList, best_worst):
        temp = 0
        for column in columnList:
            temp = temp + np.square(row[column + '_vi'] - row[column + best_worst])
        row['Di' + best_worst] = cmath.sqrt(temp)
        return row['Di' + best_worst]

    
    @staticmethod
    def calcCi(row):
        if (row['Di_best'] + row['Di_worst']) == 0:
            row['ci'] = 0 
            return 0
        else:    
            row['ci'] = row['Di_worst'] / (row['Di_best'] + row['Di_worst'])  
            return row['ci']