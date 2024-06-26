// Alex Maggioni, 20266243
// Canelle Wagner, 20232321

#include "ClimbingDifficultyCalculator.h"
#include <fstream>
#include <vector> 
#include <limits> 
#include <algorithm> 
#include <sstream> 

// ce fichier contient les definitions des methodes de la classe ClimbingDifficultyCalculator
// this file contains the definitions of the methods of the ClimbingDifficultyCalculator class

ClimbingDifficultyCalculator::ClimbingDifficultyCalculator() {}

std::vector<int> update_path_with_new_row(const std::vector<int>& current, const std::vector<int>& next_row) {
    int n = current.size();
    std::vector<int> temp(n, std::numeric_limits<int>::max());
    std::vector<int> left_cumulative(n), right_cumulative(n);

    // Calcule la somme cumulative gauche pour la nouvelle ligne
    for (int i = 0; i < n; ++i) {
        left_cumulative[i] = next_row[i] + (i > 0 ? left_cumulative[i-1] : 0);
    }

    // Calcule la somme cumulative droite pour la nouvelle ligne
    for (int i = n-1; i >= 0; --i) {
        right_cumulative[i] = next_row[i] + (i < n-1 ? right_cumulative[i+1] : 0);
    }

    // Pour chaque position dans l'actuelle, calcule le coût minimum pour se déplacer vers la k-ième cellule dans la nouvelle ligne
    for (int k = 0; k < n; ++k) {
        // En partant de la position actuelle
        temp[k] = std::min(temp[k], current[k] + next_row[k]);

        // Calcule le coût pour se déplacer à droite
        for (int j = k + 1; j < n; ++j) {
            int cost = left_cumulative[j] - (k > 0 ? left_cumulative[k-1] : 0) + current[k];
            temp[j] = std::min(temp[j], cost);
        }

        // Calcule le coût pour se déplacer à gauche
        for (int j = k - 1; j >= 0; --j) {
            int cost = right_cumulative[j] - (k < n-1 ? right_cumulative[k+1] : 0) + current[k];
            temp[j] = std::min(temp[j], cost);
        }
    }

    return temp;
}

int ClimbingDifficultyCalculator::CalculateClimbingDifficulty(std::string filename) {
    std::ifstream file(filename);
    std::string line;
    std::vector<int> current_row;
    bool isFirstRow = true;

    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string value;
        std::vector<int> next_row;

        while (getline(ss, value, ',')) {
            next_row.push_back(std::stoi(value));
        }

        if (isFirstRow) {
            current_row = next_row;
            isFirstRow = false;
        } else {
            current_row = update_path_with_new_row(current_row, next_row);
        }
    }
    file.close();

    if (current_row.empty()) return 0;

    int min_cost = *std::min_element(current_row.begin(), current_row.end());
    return min_cost;
}