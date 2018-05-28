# PROTCOL

from collections import namedtuple
import socket

GameConnection = namedtuple('GameConnection', ['socket', 'inp', 'output'])

GameMove = namedtuple('GameMove', ['move', 'column'])


class GameError(Exception):
    pass

def connect(host: str, port: int) -> GameConnection:
    game_socket = socket.socket()

    game_socket.connect((host, port))

    game_input = game_socket.makefile('r')
    game_output = game_socket.makefile('w')

    return GameConnection(socket = game_socket,
                      inp = game_input,
                      output = game_output)

##--------------------------------------------

def hello(connection: GameConnection, username: str) -> None:
    writeline(connection, 'ICS32FSP_HELLO' + username + "\r\n")
    expectline(connection, 'WELCOME' + username + "\r\n")

def requestgame(connection: GameConnection, AI_GAME: str) -> None:
    writeline(connection, AI_GAME + "\r\n")
    expectline(connection, 'READY' + "\r\n")

def sendmove(connection:GameConnection, player_input: GameMove) -> None:
    writeline(connection, player_input.move +  player_input.column + "\r\n")
    expectline(connection, 'OKAY' + "\r\n")

def close(connection: GameConnection) -> None:
    connection.inp.close()
    connection.output.close()
    connection.socket.close()
    print ("connection is now closed")

##----------------------------------------------

def readline(connection: GameConnection) -> str:
    return connection.inp.readline()[:-1]

def expectline(connection: GameConnection, expected: str) -> None:
    line = readline(connection)
    if line != expected:
        connection.socket.close()

def writeline(connection: GameConnection, line: str) -> None:
    connection.output.write(line + '\r\n')
    connection.output.flush()


