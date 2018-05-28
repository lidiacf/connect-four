# SOCKETFILE
from collections import namedtuple
import socket

GameConnection = namedtuple('GameConnection', ['socket', 'inp', 'output'])

GameMove = namedtuple('GameMove', ['move', 'column'])

class GameError(Exception):
    pass

def connect(host: str, port: int) -> GameConnection:
    '''connects to a server
    '''
    game_socket = socket.socket()

    game_socket.connect((host, port))
    
    game_input = game_socket.makefile('r')
    game_output = game_socket.makefile('w')
    print('Connected.')
    return GameConnection(socket = game_socket,
                      inp = game_input,
                      output = game_output)

##--------------------------------------------

def specify_username(connection: GameConnection):
    '''takes user input for a username, and sends to the server
    '''
    while True:
        username = input("Enter username:")
        if ' ' not in username:
            break
        elif ' ' in username:
            print('Invalid Username, please try again.')
            pass
    _writeline(connection,'I32CFSP_HELLO' + ' ' + username)
    result = _expectline(connection, 'WELCOME' + ' ' + username)
    print (result)

def requestgame(connection: GameConnection) -> None:
    '''starts the game with user input, sends it to the server and checks what the server sends back
    '''
    while True:
        startgame = input("Type 'AI_GAME' to start a new game:")
        startgame.upper()
        if startgame != 'AI_GAME':
            print('Invalid Input, please try again.')
            pass
        elif startgame == 'AI_GAME':
            break
    _writeline(connection, 'AI_GAME')
    result = _expectline(connection, 'READY')
    print (result)

def sendmove(connection:GameConnection, player_input: GameMove) -> None:
    '''sends a move to the serve and returns the move the server sends back
    '''
    _writeline(connection, player_input.move + ' ' + str(player_input.column))
    result = _expectline(connection, 'OKAY')
    print(result)
    nextmove = _readline(connection)
    _readline(connection)
    return nextmove

def close(connection: GameConnection) -> None:
    '''closes the connection
    '''
    connection.inp.close()
    connection.output.close()
    connection.socket.close()
    print ("Connection is now closed.")

##----------------------------------------------

def _readline(connection: GameConnection) -> str:
    '''reads the last line from the server
    '''
    line = connection.inp.readline()[:-1]
    return line

def _expectline(connection: GameConnection, expected: str) -> str:
    '''checks if the line read from the server is what is expected, if not it closes the connection
    '''
    line = _readline(connection)
    if line != expected:
        connection.socket.close()
    return line

def _writeline(connection: GameConnection, line: str) -> None:
    '''writes a line to the server
    '''
    connection.output.write(line + '\r\n')
    connection.output.flush()


