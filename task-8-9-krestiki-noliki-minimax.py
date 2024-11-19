import tkinter as tk
from tkinter import messagebox

# База знаний: выигрышные комбинации
BASE_KNOWLEDGE = {
    "winning_combinations": [
        [(0, 0), (0, 1), (0, 2)],  # Первая строка
        [(1, 0), (1, 1), (1, 2)],  # Вторая строка
        [(2, 0), (2, 1), (2, 2)],  # Третья строка
        [(0, 0), (1, 0), (2, 0)],  # Первый столбец
        [(0, 1), (1, 1), (2, 1)],  # Второй столбец
        [(0, 2), (1, 2), (2, 2)],  # Третий столбец
        [(0, 0), (1, 1), (2, 2)],  # Главная диагональ
        # Добавить для показа работы
        # [(0, 2), (1, 1), (2, 0)]   # Побочная диагональ
    ],
    "recent_changes": []  # Последние изменения
}

# Глобальные переменные
current_player = "X"  # Начинает игрок "X"
board = [["" for _ in range(3)] for _ in range(3)]  # Игровое поле 3x3

# Проверка победителя
def check_winner_for_player(player):
    for combination in BASE_KNOWLEDGE["winning_combinations"]:
        if all(board[row][col] == player for row, col in combination):
            return True
    return False

# Проверка победителя для текущего игрока
def check_winner():
    return check_winner_for_player(current_player)

# Проверка ничьи
def check_draw():
    for row in board:
        if "" in row:
            return False
    return True

# Минимакс: Вычисление лучшего хода
def minimax(board, depth, is_maximizing):
    if check_winner_for_player("O"):
        return 10 - depth
    if check_winner_for_player("X"):
        return depth - 10
    if check_draw():
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    board[row][col] = "O"
                    score = minimax(board, depth + 1, False)
                    board[row][col] = ""
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    board[row][col] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col] = ""
                    best_score = min(best_score, score)
        return best_score

# Поиск лучшего хода
def find_best_move():
    best_score = float('-inf')
    move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                board[row][col] = "O"
                score = minimax(board, 0, False)
                board[row][col] = ""
                if score > best_score:
                    best_score = score
                    move = (row, col)
    return move

# Обновление GUI
def update_board_gui():
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text=board[row][col])

# Сброс игрового поля
def reset_board():
    global board, current_player
    current_player = "X"
    board = [["" for _ in range(3)] for _ in range(3)]
    update_board_gui()

# Ход игрока
def make_move(row, col):
    global current_player

    if board[row][col] != "":
        messagebox.showwarning("Ошибка", "Эта клетка уже занята!")
        return

    board[row][col] = current_player
    update_board_gui()

    if check_winner():
        messagebox.showinfo("Победа!", f"Игрок {current_player} выиграл!")
        reset_board()
    elif check_draw():
        messagebox.showinfo("Ничья", "Игра закончилась вничью!")
        reset_board()
    else:
        current_player = "O" if current_player == "X" else "X"
        if current_player == "O":
            computer_move()

# Ход компьютера
def computer_move():
    move = find_best_move()
    if move:
        make_move(move[0], move[1])

# Проверка, является ли комбинация выигрышной
def is_winning_combination(new_combination):
    rows = [r for r, c in new_combination]
    cols = [c for r, c in new_combination]

    if len(set(rows)) == 1 or len(set(cols)) == 1:  # Горизонталь или вертикаль
        return True

    if sorted(new_combination) in [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]:  # Диагонали
        return True

    return False

# Интерфейс эксперта
def open_expert_interface():
    expert_window = tk.Toplevel(root)
    expert_window.title("Интерфейс эксперта")

    # Вывод текущих правил
    tk.Label(expert_window, text="Текущие выигрышные комбинации:").pack()
    winning_frame = tk.Frame(expert_window)
    winning_frame.pack()

    for combination in BASE_KNOWLEDGE["winning_combinations"]:
        tk.Label(winning_frame, text=str(combination)).pack()

    # Добавление новых правил
    tk.Label(expert_window, text="Добавить новую выигрышную комбинацию:").pack()
    entry = tk.Entry(expert_window)
    entry.pack()

    def add_combination():
        try:
            new_combination = eval(entry.get())

            if not isinstance(new_combination, list) or not all(isinstance(c, tuple) and len(c) == 2 for c in new_combination):
                raise ValueError("Новое правило должно быть списком кортежей (r, c).")

            if not all(0 <= r < 3 and 0 <= c < 3 for r, c in new_combination):
                raise ValueError("Координаты должны быть от 0 до 2 включительно.")

            if new_combination in BASE_KNOWLEDGE["winning_combinations"]:
                raise ValueError("Такое правило уже существует.")

            if not is_winning_combination(new_combination):
                raise ValueError("Комбинация не образует выигрышную линию.")

            BASE_KNOWLEDGE["winning_combinations"].append(new_combination)
            BASE_KNOWLEDGE["recent_changes"].append(f"Добавлено: {new_combination}")
            messagebox.showinfo("Успех", "Новая комбинация добавлена!")
            entry.delete(0, tk.END)
            open_expert_interface()  # Перезапуск интерфейса

        except Exception as e:
            messagebox.showwarning("Ошибка", str(e))

    tk.Button(expert_window, text="Добавить", command=add_combination).pack()

    # Просмотр последних изменений
    tk.Label(expert_window, text="Последние изменения:").pack()
    changes_frame = tk.Frame(expert_window)
    changes_frame.pack()

    for change in BASE_KNOWLEDGE["recent_changes"]:
        tk.Label(changes_frame, text=change).pack()

# Инициализация интерфейса Tkinter
root = tk.Tk()
root.title("Крестики-нолики")

# Поле игры
buttons = [[None for _ in range(3)] for _ in range(3)]
for row in range(3):
    for col in range(3):
        buttons[row][col] = tk.Button(root, text="", font=("Arial", 20), width=5, height=2,
                                      command=lambda r=row, c=col: make_move(r, c))
        buttons[row][col].grid(row=row, column=col)

# Кнопки управления
control_frame = tk.Frame(root)
control_frame.grid(row=3, column=0, columnspan=3)

tk.Button(control_frame, text="Сбросить", command=reset_board).pack(side=tk.LEFT, padx=10)
tk.Button(control_frame, text="Интерфейс эксперта", command=open_expert_interface).pack(side=tk.RIGHT, padx=10)

root.mainloop()
