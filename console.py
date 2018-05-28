# CONSOLE

import connectfour
import overlap

game_state = connectfour.new_game()

def run_user_interface():
    '''starts the game and game play, runs until a winner is found
    '''
    overlap.print_board(game_state)
    overlap.game_play(game_state)
    return game_state

if __name__ == '__main__':
    run_user_interface()
