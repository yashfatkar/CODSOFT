import math

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # Create the board
        self.current_winner = None  # Keep track of the winner

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # Tells us what number corresponds to what box
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check the row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        # Check the column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        # Check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]  # Top-left to bottom-right diagonal
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]  # Top-right to bottom-left diagonal
            if all([spot == letter for spot in diagonal2]):
                return True
        return False


def minimax(game, max_player):
    # Base cases - check if game is over
    if game.current_winner:
        if game.current_winner == 'O':  # AI
            return (None, 1 * (game.num_empty_squares() + 1))  # The AI maximizes its own score
        else:
            return (None, -1 * (game.num_empty_squares() + 1))  # The human player minimizes the AI's score
    elif not game.empty_squares():  # Game is a draw
        return (None, 0)

    # Initialize the best move and best score
    if max_player:  # Maximizing player
        best_move = None
        best_score = -math.inf  # Initialize to negative infinity
    else:  # Minimizing player
        best_move = None
        best_score = math.inf  # Initialize to positive infinity

    for possible_move in game.available_moves():
        # Make a move
        game.make_move(possible_move, 'O' if max_player else 'X')
        # Get the score from this move
        score = minimax(game, not max_player)[1]
        # Undo the move
        game.board[possible_move] = ' '
        game.current_winner = None
        # Update the best score and best move
        if max_player:
            if score > best_score:
                best_score = score
                best_move = possible_move
        else:
            if score < best_score:
                best_score = score
                best_move = possible_move

    return best_move, best_score


def play_game():
    game = TicTacToe()
    print("Welcome to Tic Tac Toe!")
    game.print_board_nums()
    print("To play, enter a number corresponding to the position on the board.")

    # Set up AI turn
    ai_turn = False
    if input("Do you want to go first? (y/n): ").lower() == 'n':
        ai_turn = True
    while game.empty_squares():
        if ai_turn:
            move, score = minimax(game, True)  # AI's turn
            game.make_move(move, 'O')
            print(f"AI placed an 'O' at position {move}")
            if game.current_winner:
                print("AI wins!")
                break
            ai_turn = False
        else:
            move = None
            while move is None:
                try:
                    move = int(input("Your turn! (Enter position 0-8): "))
                    if move not in game.available_moves():
                        print("Invalid move. Try again.")
                        move = None
                except ValueError:
                    print("Invalid input. Please enter a number.")
            game.make_move(move, 'X')
            if game.current_winner:
                print("You win!")
                break
            ai_turn = True

        game.print_board()
        print()

    if not game.current_winner:
        print("It's a tie!")


if __name__ == '__main__':
    play_game()
