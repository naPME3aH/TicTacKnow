import tkinter as tk
from tkinter import messagebox

# База знаний: хранит выигрышные комбинации и запрещённые состояния
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
    "recent_changes": []    # Последние изменения
}

# Глобальные переменные
current_player = "X"  # Начинает игрок "X"
board = [["" for _ in range(3)] for _ in range(3)]  # Игровое поле 3x3

# Проверка победителя
def check_winner():
    for combination in BASE_KNOWLEDGE["winning_combinations"]:
        if all(board[row][col] == current_player for row, col in combination):
            return True
    return False

# Проверка ничьи
def check_draw():
    for row in board:
        if "" in row:
            return False
    return True

# Добавление нового правила (выигрышной комбинации)
def is_valid_combination(new_combination):
    # Проверяем, что комбинация в одной линии (горизонталь, вертикаль, диагональ)
    rows = [r for r, c in new_combination]
    cols = [c for r, c in new_combination]

    if len(set(rows)) == 1 or len(set(cols)) == 1:  # Все в одной строке или столбце
        return True

    if sorted(new_combination) in [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]:  # Диагонали
        return True

    return False

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

def is_winning_combination(combination):
    """
    Проверяет, образует ли комбинация выигрышную линию.
    Линия может быть горизонтальной, вертикальной или диагональной.
    """
    # Проверяем горизонтальную линию
    rows = [r for r, c in combination]
    if all(row == rows[0] for row in rows):  # Все клетки находятся в одной строке
        return True

    # Проверяем вертикальную линию
    cols = [c for r, c in combination]
    if all(col == cols[0] for col in cols):  # Все клетки находятся в одном столбце
        return True

    # Проверяем диагональ (главная и побочная)
    if sorted(combination) == [(0, 0), (1, 1), (2, 2)] or sorted(combination) == [(0, 2), (1, 1), (2, 0)]:
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
            # Получаем введённую строку и пытаемся преобразовать её в список
            new_combination = eval(entry.get())
            
            # Проверяем, что это список и он содержит только кортежи
            if not isinstance(new_combination, list):
                raise ValueError("Новое правило должно быть списком кортежей.")

            if not all(isinstance(c, tuple) and len(c) == 2 for c in new_combination):
                raise ValueError("Каждый элемент правила должен быть кортежем с двумя числами.")

            # Проверяем, что все координаты находятся в пределах игрового поля
            for r, c in new_combination:
                if not (0 <= r < 3 and 0 <= c < 3):
                    raise ValueError("Координаты должны быть в диапазоне от 0 до 2 включительно.")

            # Проверка на повторы
            if new_combination in BASE_KNOWLEDGE["winning_combinations"]:
                raise ValueError("Такое правило уже существует в базе знаний.")

            # Проверяем, является ли комбинация выигрышной
            if not is_winning_combination(new_combination):
                raise ValueError("Комбинация не может быть выигрышной, так как она не образует линию.")

            # Если все проверки пройдены, добавляем комбинацию в базу знаний
            BASE_KNOWLEDGE["winning_combinations"].append(new_combination)
            BASE_KNOWLEDGE["recent_changes"].append(f"Добавлено: {new_combination}")
            messagebox.showinfo("Информация", "Новая комбинация добавлена.")
            entry.delete(0, tk.END)
            open_expert_interface()  # Обновляем окно

        except ValueError as ve:
            # Выводим окно с описанием ошибки
            messagebox.showwarning("Ошибка в правиле", str(ve))
        except Exception:
            # Обрабатываем другие ошибки
            messagebox.showwarning(
                "Ошибка",
                "Неверный формат. Убедитесь, что вы вводите правило как список кортежей."
            )

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
