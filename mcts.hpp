#include <random>

#include "board.hpp"
#include "node.hpp"


#define N_THREAD 1
#define N_GAME 1
#define N_SIMULATION 4
#define C_PUCT 2.0
#define EXPLORATION_FRAC 0.25
#define DIRICHLET_ALPHA 1.0
// #define EXPLORATION_FRAC 0.0
// #define DIRICHLET_ALPHA 0.0
// #define TAU 1.0


void collect_mldata(const char *file_name);
void play_game(int server_sock, std::vector<Node*>& history, std::default_random_engine& engine);
Node *run_mcts(Node *current_node, int server_sock, std::default_random_engine& engine);
