#Nom, matricule
#Nom, matricule

#Fonction à compléter. Ne modifiez pas sa signature.
#N : Force maximale
#k : Nombre de fenêtres disponibles
#Valeur de retour : le nombre minimal de tests qu'il faut faire 
#                   en pire cas pour déterminer le seuil de solidité 
#                   d'une fenêtre
#Doit retourner la réponse comme un int.
#
#Function to complete. Do not change its signature.
#N : Maximum force
#k : Number of windows available
#return value : Minimum number of tests needed in the worst case
#               to find the solidity threshold of a window
#Must return the answer as an int. 
def vitre(N, k):
    
    return -1


#Fonction main, vous ne devriez pas avoir à modifier
#Main function, you shouldn't have to modify it
def main(args):
    N = int(args[0])
    k = int(args[1])

    answer = vitre(N,k)
    print(answer)

if __name__ == '__main__':
    main(sys.argv[1:])