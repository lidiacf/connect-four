# UI

import socketfile
import overlap

GAME_HOST = 'woodhouse.ics.uci.edu'
GAME_PORT = 4444

def run_user_interface() -> str:
    '''initiates the connection, starts the games, closes the connection at theznd
    '''
    try:
        connection = socketfile.connect(GAME_HOST, GAME_PORT)
        socketfile.specify_username(connection)
        socketfile.requestgame(connection)
        game_state = overlap.connectfour.new_game()
        game_play(connection, game_state)
    finally:
        socketfile.close(connection)


def game_play(connection: socketfile.GameConnection, game_state: overlap.connectfour.GameState) -> None:
    '''takes a connection and a game state and initiates the game until a winner is found
    '''
    while overlap.find_winner(game_state):
        try:
            move = overlap.player_input()
            column = overlap.column_input()
            if move.upper() == 'DROP':
                game_state = overlap.connectfour.drop(game_state, column) 
                overlap.print_board(game_state)
            elif move.upper() == 'POP':
                game_state = overlap.connectfour.pop(game_state, column) 
                overlap.print_board(game_state)

            if overlap.find_winner(game_state) == False:
                break
        
            column = column + 1
            currentmove = socketfile.GameMove(move, column)
    
            server_move = socketfile.sendmove(connection, currentmove)

            server_move = str(server_move)
            server_split = server_move.split()
            print(server_split, '---------')
            move = server_split[0]
            column = int(server_split[1]) - 1

            if move.upper() == 'DROP':
                game_state = overlap.connectfour.drop(game_state, column) 
                overlap.print_board(game_state)
            elif move.upper() == 'POP':
                game_state = overlap.connectfour.pop(game_state, column) 
                overlap.print_board(game_state)

            if overlap.find_winner(game_state) == False:
                break
        except: 
             print ("Invalid move, please try again.")

            
if __name__ == '__main__':
    run_user_interface()
