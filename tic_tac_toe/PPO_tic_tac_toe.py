from itertools import chain

import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from tqdm import trange

from two_player_game import TwoPlayerGameAgent
from .minimax_tic_tac_toe import TicTacToeMiniMaxAgent
from .tic_tac_toe_game import TicTacToeBoard, TicTacToeMove, X, O


class DiscreteStatePolicyMLP(nn.Module):
    def __init__(self, n_states, hidden_layer_sizes, n_actions):
        super().__init__()

        modules = []
        activation = nn.ReLU()
        modules.append(nn.Embedding(n_states, hidden_layer_sizes[0]))
        for size_in, size_out in zip(hidden_layer_sizes[:-1], hidden_layer_sizes[1:]):
            modules.append(nn.Linear(size_in, size_out))
            modules.append(activation)
        modules.append(nn.Linear(hidden_layer_sizes[-1], n_actions))
        modules.append(nn.Softmax(dim=1))

        self.net = nn.Sequential(*modules)

    def forward(self, x):
        return self.net(x)


class DiscreteStateValueMLP(nn.Module):
    def __init__(self, n_states, hidden_layer_sizes):
        super().__init__()

        modules = []
        activation = nn.ReLU()
        modules.append(nn.Embedding(n_states, hidden_layer_sizes[0]))
        for size_in, size_out in zip(hidden_layer_sizes[:-1], hidden_layer_sizes[1:]):
            modules.append(nn.Linear(size_in, size_out))
            modules.append(activation)
        modules.append(nn.Linear(hidden_layer_sizes[-1], 1))

        self.net = nn.Sequential(*modules)

    def forward(self, x):
        return self.net(x)


class ListDataset(Dataset):
    def __init__(self, data):
        super().__init__()
        self.data = list(data)

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)


class TicTacToePPOTrainer:
    def __init__(self, device=torch.device("cpu")):
        self.memory = []
        self.board = TicTacToeBoard()
        self.policy_network = DiscreteStatePolicyMLP(3 ** 9, (8, 8, 8), 9).to(device)
        self.value_network = DiscreteStateValueMLP(3 ** 9, (8, 8, 8)).to(device)
        self.value_criterion = nn.MSELoss()
        self.device = device

    def _add_rollout_to_memory(self, rollout, gamma):
        total_discounted_reward = 0
        for transition in reversed(rollout):
            state, action, action_dist, reward = transition
            total_discounted_reward = reward + gamma * total_discounted_reward
            self.memory.append((state, action, action_dist, total_discounted_reward))

    def _clear_memory(self):
        self.memory = []

    def _get_move(self):
        with torch.inference_mode():
            state = torch.tensor([hash(self.board)]).long().to(self.device)
            action_dist = self.policy_network(state)
            action = int(torch.multinomial(action_dist, num_samples=1))
            row, column = action // 3, action % 3
            return row, column, action_dist

    def _learn_ppo(self, optimizer, dataloader, epsilon, policy_epochs):
        for epoch in range(policy_epochs):
            for states, actions, old_action_dists, total_discounted_rewards in dataloader:
                states = states.long().to(self.device)
                actions = actions.unsqueeze(0).to(self.device)
                old_action_dists = old_action_dists.squeeze(1).float().to(self.device)
                total_discounted_rewards = total_discounted_rewards.float().to(self.device)

                # Calculate value loss
                values = self.value_network(states).squeeze(1)
                value_loss = self.value_criterion(total_discounted_rewards, values)

                # Calculate policy loss
                advantage = total_discounted_rewards - values
                advantage = advantage.unsqueeze(1).detach()
                current_action_dists = self.policy_network(states)
                policy_ratio = current_action_dists.gather(dim=1, index=actions) / old_action_dists.gather(dim=1,
                                                                                                           index=actions)
                policy_gradient = policy_ratio * advantage
                clipped_policy_gradient = torch.clamp(policy_ratio, 1 - epsilon, 1 + epsilon) * advantage
                policy_loss = -torch.mean(torch.min(policy_gradient, clipped_policy_gradient))

                loss = value_loss + policy_loss

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

    def train_PPO_for_tictactoe(self,
                                epochs,
                                policy_epochs=10,
                                n_games_per_epoch=500,
                                opponent=TicTacToeMiniMaxAgent("").get_move,
                                lr=3e-4,
                                gamma=0.9,
                                epsilon=0.2,
                                batch_size=500,
                                silent=True):
        optimizer = torch.optim.Adam(chain(self.policy_network.parameters(), self.value_network.parameters()),
                                     lr=lr)

        for epoch_number in (loop := trange(epochs, disable=silent)):
            self._clear_memory()

            # Begin experience loop: X, then O
            for player in (X, O):
                for game_number in (inner_loop := trange(n_games_per_epoch, disable=silent, leave=False)):
                    self.board.reset()
                    rollout = []

                    while not self.board.is_game_over:
                        # Handle opponent's first move as X
                        if self.board.next_player != player:
                            opponent_move = opponent(self.board)
                            self.board.play_move(opponent_move)
                            continue

                        # Play a move
                        row, column, action_dist = self._get_move()
                        state = hash(self.board)
                        try:
                            self.board.play_move(TicTacToeMove(row, column))
                        # Major negative penalty if invalid move
                        except AssertionError:
                            reward = -15
                        else:
                            # If the game is over, check the score
                            if self.board.is_game_over:
                                reward = 0 if self.board.winning_player is None else 10 - self.board.depth()
                            # If not, let the opponent move and check the score
                            else:
                                opponent_move = opponent(self.board)
                                self.board.play_move(opponent_move)
                                if not self.board.is_game_over:
                                    reward = 0
                                else:
                                    reward = 0 if self.board.winning_player is None else -10 + self.board.depth()

                        # Add move to memory
                        rollout.append((state, 3 * row + column, action_dist, reward))

                    self._add_rollout_to_memory(rollout, gamma)

            # Learn from experience
            dataset = ListDataset(self.memory)
            dataloader = DataLoader(dataset, batch_size=batch_size)
            self._learn_ppo(optimizer, dataloader, epsilon, policy_epochs)


class TicTacToePPOAgent(TwoPlayerGameAgent):
    def __init__(self, name, device=torch.device("cpu"), silent_training=True):
        self.name = name
        self.device = device
        trainer = TicTacToePPOTrainer(device)
        trainer.train_PPO_for_tictactoe(epochs=10, silent=silent_training)
        self.net = trainer.policy_network
        self.net.eval()

    def get_move(self, board):
        with torch.inference_mode():
            state = torch.tensor([hash(board)]).long().to(self.device)
            distribution = self.net(state).flatten()
            valid_moves = [3 * move.row + move.column for move in board.get_possible_moves()]
            for move in range(9):
                if move not in valid_moves:
                    distribution[move] = 0.0
            action = int(torch.multinomial(distribution, num_samples=1))
            return TicTacToeMove(action // 3, action % 3)


if __name__ == "__main__":
    trainer = TicTacToePPOTrainer(device=torch.device("cpu"))
    trainer.train_PPO_for_tictactoe(epochs=1)
