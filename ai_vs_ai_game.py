import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style
import pandas as pd
from training_model import make_prevision, convert_board_to_numeric

collected_data = []

def save_game_state(row, col, player):
    flattened_board = [cell for row in game for cell in row]
    numeric_board = convert_board_to_numeric(flattened_board)
    collected_data.append(numeric_board + [f'{row},{col}', player])

def export_data_to_csv():
    columns = [f'cell_{i}' for i in range(9)] + ['move', 'player']
    df = pd.DataFrame(collected_data, columns=columns)
    
    try:
        with open('collected_data.csv', 'r') as f:
            df.to_csv('collected_data.csv', mode='a', header=False, index=False)
    except FileNotFoundError:
        df.to_csv('collected_data.csv', mode='w', header=True, index=False)

def make_ai_move():
    global current_player

    flattened_board = [cell for row in game for cell in row]

    while True:
        predicted_move = make_prevision(flattened_board)

        row, col = map(int, predicted_move.split(','))

        if game[row][col] == '': 
            save_game_state(row, col, current_player)
            game[row][col] = current_player
            buttons[row][col].configure(text=current_player)
            check_winner()

            current_player = "O" if current_player == "X" else "X"
            break

def check_winner():
    winning_combinations = (game[0], game[1], game[2],
                            [game[i][0] for i in range(3)],
                            [game[i][1] for i in range(3)],
                            [game[i][2] for i in range(3)],
                            [game[i][i] for i in range(3)],
                            [game[i][2 - i] for i in range(3)])

    for combination in winning_combinations:
        if combination[0] == combination[1] == combination[2] != '':
            show_result(combination[0])
            return

    if all(game[i][j] != '' for i in range(3) for j in range(3)):
        show_result("Draw")
        return

    window.after(500, make_ai_move)

def show_result(player):
    if player == "Draw":
        message = "Jogo empatado!"
    else:
        message = f"Jogador {player} venceu!"
    
    messagebox.showinfo("Resultado", message)
    export_data_to_csv()

def reset_game():
    global game, current_player
    game = [['', '', ''] for _ in range(3)]
    current_player = "X"
    for row in buttons:
        for button in row:
            button.configure(text='')

def start_auto_game():
    reset_game()
    make_ai_move()

window = tk.Tk()
window.title("Jogo da Velha")
style = Style(theme="flatly")

buttons = []
for i in range(3):
    row = []
    for j in range(3):
        button = tk.Button(window, text='', width=20, height=10)
        button.grid(row=i, column=j, padx=5, pady=5)
        row.append(button)
    buttons.append(row)

game = [['', '', ''] for _ in range(3)]
current_player = "X"

start_auto_game()

window.mainloop()
