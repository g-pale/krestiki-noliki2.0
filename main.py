import tkinter as tk
from tkinter import messagebox

class TicTacToeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Крестики-нолики 2.0")
        self.window.geometry("500x650")
        self.window.configure(bg='#2c3e50')
        self.window.resizable(False, False)
        
        # Игровые переменные
        self.current_player = "X"
        self.player1_symbol = "X"
        self.player2_symbol = "O"
        self.player1_wins = 0
        self.player2_wins = 0
        self.game_active = False
        self.buttons = []
        
        # Создание интерфейса
        self.create_header()
        self.create_player_selection()
        self.create_game_board()
        self.create_control_buttons()
        self.create_score_display()
        
    def create_header(self):
        """Создание заголовка игры"""
        header_frame = tk.Frame(self.window, bg='#2c3e50')
        header_frame.pack(pady=10)
        
        title_label = tk.Label(
            header_frame,
            text="🎮 КРЕСТИКИ-НОЛИКИ 2.0 🎮",
            font=("Arial", 20, "bold"),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title_label.pack()
        
    def create_player_selection(self):
        """Создание панели выбора символа игрока"""
        selection_frame = tk.Frame(self.window, bg='#34495e', relief='raised', bd=2)
        selection_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(
            selection_frame,
            text="Выберите символ для Игрока 1:",
            font=("Arial", 12, "bold"),
            fg='#ecf0f1',
            bg='#34495e'
        ).pack(pady=5)
        
        symbol_frame = tk.Frame(selection_frame, bg='#34495e')
        symbol_frame.pack(pady=5)
        
        self.symbol_var = tk.StringVar(value="X")
        
        x_radio = tk.Radiobutton(
            symbol_frame,
            text="❌ Крестики (X)",
            variable=self.symbol_var,
            value="X",
            font=("Arial", 11),
            fg='#e74c3c',
            bg='#34495e',
            selectcolor='#2c3e50',
            command=self.update_symbols
        )
        x_radio.pack(side='left', padx=10)
        
        o_radio = tk.Radiobutton(
            symbol_frame,
            text="⭕ Нолики (O)",
            variable=self.symbol_var,
            value="O",
            font=("Arial", 11),
            fg='#3498db',
            bg='#34495e',
            selectcolor='#2c3e50',
            command=self.update_symbols
        )
        o_radio.pack(side='left', padx=10)
        
    def create_game_board(self):
        """Создание игрового поля"""
        # Информация о текущем игроке
        self.info_frame = tk.Frame(self.window, bg='#2c3e50')
        self.info_frame.pack(pady=10)
        
        self.current_player_label = tk.Label(
            self.info_frame,
            text="Нажмите 'Новая игра' для начала",
            font=("Arial", 14, "bold"),
            fg='#f39c12',
            bg='#2c3e50'
        )
        self.current_player_label.pack()
        
        # Игровое поле
        self.game_frame = tk.Frame(self.window, bg='#34495e', relief='raised', bd=3)
        self.game_frame.pack(pady=10)
        
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(
                    self.game_frame,
                    text="",
                    font=("Arial", 24, "bold"),
                    width=4,
                    height=2,
                    bg='#ecf0f1',
                    fg='#2c3e50',
                    relief='raised',
                    bd=2,
                    command=lambda r=i, c=j: self.on_click(r, c),
                    state='disabled'
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)
            
    def create_control_buttons(self):
        """Создание кнопок управления"""
        control_frame = tk.Frame(self.window, bg='#2c3e50')
        control_frame.pack(pady=15)
        
        self.new_game_btn = tk.Button(
            control_frame,
            text="🎯 Новая игра",
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            relief='raised',
            bd=2,
            padx=20,
            pady=5,
            command=self.new_game
        )
        self.new_game_btn.pack(side='left', padx=5)
        
        self.reset_btn = tk.Button(
            control_frame,
            text="🔄 Сброс поля",
            font=("Arial", 12, "bold"),
            bg='#f39c12',
            fg='white',
            relief='raised',
            bd=2,
            padx=20,
            pady=5,
            command=self.reset_game,
            state='disabled'
        )
        self.reset_btn.pack(side='left', padx=5)
        
        self.new_tournament_btn = tk.Button(
            control_frame,
            text="🏆 Новый турнир",
            font=("Arial", 12, "bold"),
            bg='#8e44ad',
            fg='white',
            relief='raised',
            bd=2,
            padx=20,
            pady=5,
            command=self.new_tournament
        )
        self.new_tournament_btn.pack(side='left', padx=5)
        
    def create_score_display(self):
        """Создание панели отображения счета"""
        score_frame = tk.Frame(self.window, bg='#34495e', relief='raised', bd=2)
        score_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(
            score_frame,
            text="📊 ТУРНИРНАЯ ТАБЛИЦА (до 3 побед)",
            font=("Arial", 14, "bold"),
            fg='#ecf0f1',
            bg='#34495e'
        ).pack(pady=5)
        
        scores_container = tk.Frame(score_frame, bg='#34495e')
        scores_container.pack(pady=5)
        
        # Счет игрока 1
        player1_frame = tk.Frame(scores_container, bg='#e74c3c', relief='raised', bd=2)
        player1_frame.pack(side='left', padx=10, pady=5)
        
        tk.Label(
            player1_frame,
            text="Игрок 1",
            font=("Arial", 12, "bold"),
            fg='white',
            bg='#e74c3c'
        ).pack(pady=2)
        
        self.player1_score_label = tk.Label(
            player1_frame,
            text="❌: 0",
            font=("Arial", 16, "bold"),
            fg='white',
            bg='#e74c3c'
        )
        self.player1_score_label.pack(pady=2)
        
        # VS
        tk.Label(
            scores_container,
            text="VS",
            font=("Arial", 16, "bold"),
            fg='#f39c12',
            bg='#34495e'
        ).pack(side='left', padx=20)
        
        # Счет игрока 2
        player2_frame = tk.Frame(scores_container, bg='#3498db', relief='raised', bd=2)
        player2_frame.pack(side='left', padx=10, pady=5)
        
        tk.Label(
            player2_frame,
            text="Игрок 2",
            font=("Arial", 12, "bold"),
            fg='white',
            bg='#3498db'
        ).pack(pady=2)
        
        self.player2_score_label = tk.Label(
            player2_frame,
            text="⭕: 0",
            font=("Arial", 16, "bold"),
            fg='white',
            bg='#3498db'
        )
        self.player2_score_label.pack(pady=2)
        
    def update_symbols(self):
        """Обновление символов игроков"""
        if self.symbol_var.get() == "X":
            self.player1_symbol = "X"
            self.player2_symbol = "O"
            self.player1_score_label.config(text=f"❌: {self.player1_wins}")
            self.player2_score_label.config(text=f"⭕: {self.player2_wins}")
        else:
            self.player1_symbol = "O"
            self.player2_symbol = "X"
            self.player1_score_label.config(text=f"⭕: {self.player1_wins}")
            self.player2_score_label.config(text=f"❌: {self.player2_wins}")
            
    def new_game(self):
        """Начало новой игры"""
        self.game_active = True
        self.current_player = self.player1_symbol
        self.reset_btn.config(state='normal')
        
        # Очистка поля
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(
                    text="",
                    bg='#ecf0f1',
                    state='normal'
                )
        
        self.update_current_player_display()
        
    def reset_game(self):
        """Сброс текущей игры"""
        self.current_player = self.player1_symbol
        
        # Очистка поля
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(
                    text="",
                    bg='#ecf0f1',
                    state='normal'
                )
        
        self.update_current_player_display()
        
    def new_tournament(self):
        """Начало нового турнира"""
        self.player1_wins = 0
        self.player2_wins = 0
        self.update_score_display()
        self.new_game()
        
    def update_current_player_display(self):
        """Обновление отображения текущего игрока"""
        if self.current_player == self.player1_symbol:
            symbol_emoji = "❌" if self.player1_symbol == "X" else "⭕"
            self.current_player_label.config(
                text=f"Ход Игрока 1: {symbol_emoji} ({self.player1_symbol})",
                fg='#e74c3c'
            )
        else:
            symbol_emoji = "⭕" if self.player2_symbol == "O" else "❌"
            self.current_player_label.config(
                text=f"Ход Игрока 2: {symbol_emoji} ({self.player2_symbol})",
                fg='#3498db'
            )
            
    def update_score_display(self):
        """Обновление отображения счета"""
        if self.player1_symbol == "X":
            self.player1_score_label.config(text=f"❌: {self.player1_wins}")
            self.player2_score_label.config(text=f"⭕: {self.player2_wins}")
        else:
            self.player1_score_label.config(text=f"⭕: {self.player1_wins}")
            self.player2_score_label.config(text=f"❌: {self.player2_wins}")
            
    def check_winner(self):
        """Проверка победителя"""
        # Проверка строк
        for i in range(3):
            if (self.buttons[i][0]["text"] == self.buttons[i][1]["text"] == 
                self.buttons[i][2]["text"] != ""):
                return self.buttons[i][0]["text"]
        
        # Проверка столбцов
        for i in range(3):
            if (self.buttons[0][i]["text"] == self.buttons[1][i]["text"] == 
                self.buttons[2][i]["text"] != ""):
                return self.buttons[0][i]["text"]
        
        # Проверка диагоналей
        if (self.buttons[0][0]["text"] == self.buttons[1][1]["text"] == 
            self.buttons[2][2]["text"] != ""):
            return self.buttons[0][0]["text"]
        
        if (self.buttons[0][2]["text"] == self.buttons[1][1]["text"] == 
            self.buttons[2][0]["text"] != ""):
            return self.buttons[0][2]["text"]
        
        return None
        
    def check_draw(self):
        """Проверка ничьей"""
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]["text"] == "":
                    return False
        return True
        
    def disable_all_buttons(self):
        """Отключение всех кнопок поля"""
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state='disabled')
                
    def highlight_winning_line(self, winner):
        """Подсветка выигрышной линии"""
        # Проверка строк
        for i in range(3):
            if (self.buttons[i][0]["text"] == self.buttons[i][1]["text"] == 
                self.buttons[i][2]["text"] == winner):
                for j in range(3):
                    self.buttons[i][j].config(bg='#2ecc71')
                return
        
        # Проверка столбцов
        for i in range(3):
            if (self.buttons[0][i]["text"] == self.buttons[1][i]["text"] == 
                self.buttons[2][i]["text"] == winner):
                for j in range(3):
                    self.buttons[j][i].config(bg='#2ecc71')
                return
        
        # Проверка диагоналей
        if (self.buttons[0][0]["text"] == self.buttons[1][1]["text"] == 
            self.buttons[2][2]["text"] == winner):
            for i in range(3):
                self.buttons[i][i].config(bg='#2ecc71')
            return
        
        if (self.buttons[0][2]["text"] == self.buttons[1][1]["text"] == 
            self.buttons[2][0]["text"] == winner):
            for i in range(3):
                self.buttons[i][2-i].config(bg='#2ecc71')
            return
    
    def on_click(self, row, col):
        """Обработка клика по ячейке"""
        if not self.game_active or self.buttons[row][col]['text'] != "":
            return
        
        # Установка символа
        self.buttons[row][col]['text'] = self.current_player
        
        # Изменение цвета в зависимости от символа
        if self.current_player == "X":
            self.buttons[row][col].config(fg='#e74c3c', bg='#fadbd8')
        else:
            self.buttons[row][col].config(fg='#3498db', bg='#d6eaf8')
        
        # Проверка победителя
        winner = self.check_winner()
        if winner:
            self.game_active = False
            self.highlight_winning_line(winner)
            self.disable_all_buttons()
            
            # Определение победившего игрока
            if winner == self.player1_symbol:
                self.player1_wins += 1
                winner_name = "Игрок 1"
            else:
                self.player2_wins += 1
                winner_name = "Игрок 2"
            
            self.update_score_display()
            
            # Проверка окончания турнира
            if self.player1_wins == 3:
                messagebox.showinfo(
                    "🏆 ТУРНИР ОКОНЧЕН!",
                    f"🎉 ИГРОК 1 ВЫИГРАЛ ТУРНИР!\n\nФинальный счет: {self.player1_wins}:{self.player2_wins}\n\nПоздравляем с победой! 🏆"
                )
                self.current_player_label.config(
                    text="🏆 Игрок 1 - ЧЕМПИОН ТУРНИРА! 🏆",
                    fg='#f39c12'
                )
            elif self.player2_wins == 3:
                messagebox.showinfo(
                    "🏆 ТУРНИР ОКОНЧЕН!",
                    f"🎉 ИГРОК 2 ВЫИГРАЛ ТУРНИР!\n\nФинальный счет: {self.player1_wins}:{self.player2_wins}\n\nПоздравляем с победой! 🏆"
                )
                self.current_player_label.config(
                    text="🏆 Игрок 2 - ЧЕМПИОН ТУРНИРА! 🏆",
                    fg='#f39c12'
                )
            else:
                symbol_emoji = "❌" if winner == "X" else "⭕"
                messagebox.showinfo(
                    "🎯 Игра окончена!",
                    f"🎉 {winner_name} ({symbol_emoji}) победил!\n\nСчет в турнире: {self.player1_wins}:{self.player2_wins}\n\n(Играем до 3 побед)"
                )
                self.current_player_label.config(
                    text=f"🎉 {winner_name} выиграл! Нажмите 'Новая игра'",
                    fg='#2ecc71'
                )
            return
        
        # Проверка ничьей
        if self.check_draw():
            self.game_active = False
            self.disable_all_buttons()
            messagebox.showinfo(
                "🤝 Ничья!",
                f"Игра закончилась ничьей!\n\nСчет в турнире остается: {self.player1_wins}:{self.player2_wins}"
            )
            self.current_player_label.config(
                text="🤝 Ничья! Нажмите 'Новая игра'",
                fg='#95a5a6'
            )
            return
        
        # Смена игрока
        if self.current_player == self.player1_symbol:
            self.current_player = self.player2_symbol
        else:
            self.current_player = self.player1_symbol
            
        self.update_current_player_display()
        
    def run(self):
        """Запуск игры"""
        self.window.mainloop()

# Создание и запуск игры
if __name__ == "__main__":
    game = TicTacToeGame()
    game.run()
