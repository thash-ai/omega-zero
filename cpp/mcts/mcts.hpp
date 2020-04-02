#pragma once

#include <random>

#include "board.hpp"
#include "node.hpp"


#define N_SAMPLING_MOVES 15
#define C_PUCT 2
#define EXPLORATION_FRAC 0.25
#define DIRICHLET_ALPHA 1.0

void play_game(int n_simulation, int server_sock, std::vector<GameNode*>& history, std::default_random_engine& engine);
GameNode *run_mcts(GameNode *current_node, int n_simulation, int server_sock, std::default_random_engine& engine, bool stochastic);
