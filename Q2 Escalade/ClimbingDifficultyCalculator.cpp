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

std::vector<int> best_next_path(const std::vector<int>& current, const std::vector<std::vector<int>>& matrix, int above_index) {
    int n = current.size();
    std::vector<int> temp(n, std::numeric_limits<int>::max());
    std::vector<int> left_cumulative(n), right_cumulative(n);

    // Calculate left cumulative sum for the above line
    for (int i = 0; i < n; ++i) {
        left_cumulative[i] = matrix[above_index][i] + (i > 0 ? left_cumulative[i-1] : 0);
    }

    // Calculate right cumulative sum for the above line
    for (int i = n-1; i >= 0; --i) {
        right_cumulative[i] = matrix[above_index][i] + (i < n-1 ? right_cumulative[i+1] : 0);
    }

    // For each position in current, calculate the minimum cost to move to the kth cell in the above row
    for (int k = 0; k < n; ++k) {
        // Starting from the current position
        temp[k] = std::min(temp[k], current[k] + matrix[above_index][k]);

        // Calculate cost to move to the right
        for (int j = k + 1; j < n; ++j) {
            int cost = left_cumulative[j] - (k > 0 ? left_cumulative[k-1] : 0) + current[k];
            temp[j] = std::min(temp[j], cost);
        }

        // Calculate cost to move to the left
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
    std::vector<std::vector<int>> matrix;

    while (std::getline(file, line)) {
        std::vector<int> row;
        std::stringstream ss(line);
        std::string value;
        while (getline(ss, value, ',')) {
            row.push_back(std::stoi(value));
        }
        matrix.push_back(row);
    }
    file.close();

    if (matrix.empty()) return 0;

    std::vector<int> v = matrix.back();

    for (int i = matrix.size() - 2; i >= 0; --i) {
        v = best_next_path(v, matrix, i);
    }

    int min_cost = *std::min_element(v.begin(), v.end());
    return min_cost;
}