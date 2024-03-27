#Alex Maggioni, 20266243
#Canelle Wagner, 20232321

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
    moves = 0
    dp = [[0] * (k + 1) for _ in range(N + 1)]
    
    # Construire dp[][] jusqu'à ce que dp[moves][k] >= N
    while dp[moves][k] < N:
        moves += 1
        for window in range(1, k + 1):
            dp[moves][window] = dp[moves - 1][window - 1] + dp[moves - 1][window] + 1

    # Ajuster pour éviter le dernier test si inutile
    upper_bound = N  # Limite supérieure initiale
    for move in range(moves, 0, -1):
        # Vérifier si le dernier test est redondant
        if dp[move - 1][k] + 1 == upper_bound:
            return move - 1
        upper_bound = dp[move - 1][k] + 1
    
    return moves

#Fonction main, vous ne devriez pas avoir à modifier
#Main function, you shouldn't have to modify it
def main(args):
    N = int(args[0])
    k = int(args[1])

    answer = vitre(N,k)
    print(answer)

if __name__ == '__main__':
    main(sys.argv[1:])
