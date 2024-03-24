// CE FICHIER NE SERT QU'A APPELER ET TESTER VOTRE CODE. 
// VOUS NE DEVRIEZ PAS AVOIR BESOIN DE LE MODIFIER, SAUF POUR 
// AJOUTER VOUS-MÊME D'AUTRES TESTS SI VOUS LE VOULEZ.
// NE PAS REMETTRE SUR STUDIUM. REMETTEZ SEULEMENT ClimbingDifficultyCalculator.cpp/.h

// THIS FILE IS ONLY USED TO CALL AND TEST YOUR CODE.
// YOU SHOULD NOT HAVE TO MODIFY IT, EXCEPT FOR ADDING 
// NEW CUSTOM TESTS IF YOU WISH TO DO SO.
// DO NOT SUBMIT ON STUDIUM. ONLY SUBMIT ClimbingDifficultyCalculator.cpp/.h


#include <iostream> // pour l'affichage dans la console // for display in console
#include "ClimbingDifficultyCalculator.h" // pour la classe principale de l'exercice // for the main class of the exercise
#include <vector> // pour utiliser les vecteurs de la librairie standard // to use vectors from the standard library
#include <cstdlib> // pour convertir le input en int // to convert input to int
#include <string> // pour le nom de fichier // for the file name

// commandes / command (PowerShell) :
//  g++ -o climbing_difficulty.exe .\climbing_difficulty.cpp .\ClimbingDifficultyCalculator.cpp
// .\climbing_difficulty.exe wall2.txt



bool TestPrimeCalculator();

int main(int argc, char *argv[])
{
    std::cout << "Calculateur de difficulte de mur d'escalade / Climbing wall difficulty calculator" << std::endl;

    std::string filename = "wall1.txt";
    if (argc >= 2){
        filename = argv[1];   
    }
    ClimbingDifficultyCalculator Calculator = ClimbingDifficultyCalculator();
    int answer = Calculator.CalculateClimbingDifficulty(filename);
    std::cout << answer << std::endl;

    // tests
    if (TestPrimeCalculator()){
        std::cout << "Tests reussis / Tests passed !" << std::endl;
    } else {
        std::cout << "Tests echoues / Failed tests :(" << std::endl;
    }

}

bool TestPrimeCalculator(){
    std::vector<int> ExpectedReturns;
    ClimbingDifficultyCalculator Calculator = ClimbingDifficultyCalculator();
    ExpectedReturns.push_back(10);
    ExpectedReturns.push_back(4);
    ExpectedReturns.push_back(1);
    ExpectedReturns.push_back(5);
    ExpectedReturns.push_back(264881);
    ExpectedReturns.push_back(260324);

    for (int idx = 0; idx < ExpectedReturns.size(); idx++){
        std::string basename = "wall";
        std::string extension = ".txt";
        std::string filename = basename + std::to_string(idx + 1) + extension;
        int ReceivedReturn = Calculator.CalculateClimbingDifficulty(filename);
        if (ReceivedReturn != ExpectedReturns[idx])
            return false;
    }
    
    return true;
}
