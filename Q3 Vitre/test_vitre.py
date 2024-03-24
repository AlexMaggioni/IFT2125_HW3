#CE FICHIER NE SERT QU'A APPELER ET TESTER VOTRE CODE. 
#VOUS NE DEVRIEZ PAS AVOIR BESOIN DE LE MODIFIER, SAUF POUR 
#AJOUTER VOUS-MÊME D'AUTRES TESTS SI VOUS LE VOULEZ.
#NE PAS REMETTRE SUR STUDIUM. REMETTEZ SEULEMENT vitre.py

#THIS FILE IS ONLY USED TO CALL AND TEST YOUR CODE.
#YOU SHOULD NOT HAVE TO MODIFY IT, EXCEPT FOR ADDING 
#NEW CUSTOM TESTS IF YOU WISH TO DO SO.
#DO NOT SUBMIT ON STUDIUM. ONLY SUBMIT vitre.py

import vitre

def verifyAns(answer, ExpectedVal):
    if(answer != ExpectedVal):
        raise Exception("got " + str(answer) + ", expected " + str(ExpectedVal))

if __name__ == '__main__':
    inputs = [(2,1),
              (4,1),
              (4,2),
              (4,3),
              (25,1),
              (25,2),
              (25,3),
              (25,10),
              (25, 50),
              (100,10),
              (1000,10),
              (2000,10)]
    expected = [1,3,2,2,24,7,5,5,5,7,10,11]
    for i in range(len(expected)):
        try:
            answer = vitre.vitre(inputs[i][0], inputs[i][1])
            verifyAns(answer, expected[i])
            print("Test " + str(i+1) + "/" + str(len(expected)) + " OK\n")
        except Exception as e: 
            print("Test " + str(i+1) + "/" + str(len(expected)) + " Fail\n")
            print(e)
            print()
    

    
    