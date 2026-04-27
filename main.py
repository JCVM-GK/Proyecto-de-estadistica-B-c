import tkinter as tk
import random
from typing import List, Dict, Tuple

class GameEngine:
    """Modelo: Maneja la lógica pura, mazo y estadísticas."""
    def __init__(self):
        self.deck: List[int] = []
        self.history: List[str] = []
        self.score: int = 0
        self.streak: int = 0
        self.current_card: int = 0
        self.reset_deck()

    def reset_deck(self):
        self.deck = [v for v in range(1, 14)] * 4
        random.shuffle(self.deck)

    def start_new_game(self):
        self.history = []
        self.score = 0
        self.streak = 0
        self.reset_deck()
        self.current_card, _ = self.draw_card()

    def draw_card(self) -> Tuple[int, bool]:
        was_reset = False
        if not self.deck:
            self.reset_deck()
            was_reset = True
        return self.deck.pop(), was_reset

    def calculate_probabilities(self) -> Dict[str, float]:
        if not self.deck:
            return {"higher": 0.0, "lower": 0.0, "equal": 0.0}

        total = len(self.deck)
        higher = sum(1 for c in self.deck if c > self.current_card)
        lower = sum(1 for c in self.deck if c < self.current_card)
        equal = sum(1 for c in self.deck if c == self.current_card)

        return {
            "higher": (higher / total) * 100,
            "lower": (lower / total) * 100,
            "equal": (equal / total) * 100
        }

    def check_guess(self, guess: str) -> Tuple[int, bool, bool]:
        # Antes de sacar la carta, calculamos la probabilidad de la elección para el score
        probs = self.calculate_probabilities()
        prob_success = probs[guess]

        next_card, was_reset = self.draw_card()
        is_win = False

        # Lógica de comparación correcta
        if guess == "higher" and next_card > self.current_card:
            is_win = True
        elif guess == "lower" and next_card << self.current_card:
            is_win = True

        if is_win:
            # Score ponderado: más puntos si la probabilidad era baja
            points = 1 + int((100 - prob_success) / 10)
            self.score += points
            self.streak += 1
        elif next_card == self.current_card:
            # Empate: no hace nada al score ni a la racha
            pass
        else:
            self.streak = 0

        self.current_card = next_card
        return next_card, is_win, was_reset

class GameView:
    """Vista y Controlador: Maneja la interfaz Tkinter."""
    def __init__(self, root: tk.Tk):
        self.root = root
        self.engine = GameEngine()
        self.root.title("High or Low v2.0 - Lead Engineer Edition")
        self.root.geometry("450x650")
        self.root.configure(bg="#1A472A") # Verde Casino

        self.value_map = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
        self.suits = ['♠', '♥', '♦', '♣']

        self.setup_ui()
        self.start_new_game()

    def setup_ui(self):
        # Labels de info superior
        self.lbl_score = tk.Label(self.root, text="Score: 0", font=("Consolas", 18, "bold"), bg="#1A472A", fg="white")
        self.lbl_score.pack(pady=10)

        self.lbl_streak = tk.Label(self.root, text="Racha: 0", font=("Consolas", 12), bg="#1A472A", fg="#FFD700")
        self.lbl_streak.pack()

        # Visual de la carta
        self.card_frame = tk.Frame(self.root, bg="white", highlightbackground="black", highlightthickness=2, width=150, height=220)
        self.card_frame.pack_propagate(False)
        self.card_frame.pack(pady=30)

        self.lbl_card = tk.Label(self.card_frame, text="?", font=("Arial", 60, "bold"), bg="white", fg="black")
        self.lbl_card.place(relx=0.5, rely=0.5, anchor="center")

        # Probabilidades
        self.lbl_prob = tk.Label(self.root, text="", font=("Consolas", 10), bg="#1A472A", fg="#E0E0E0")
        self.lbl_prob.pack()

        self.lbl_deck_count = tk.Label(self.root, text="", font=("Consolas", 9), bg="#1A472A", fg="#A0A0A0")
        self.lbl_deck_count.pack(pady=5)

        # Botones
        self.btn_frame = tk.Frame(self.root, bg="#1A472A")
        self.btn_frame.pack(pady=20)

        self.btn_higher = tk.Button(self.btn_frame, text="MAYOR ↑", command=lambda: self.handle_play("higher"),
                                   width=10, height=2, font=("Arial", 12, "bold"), bg="#2E7D32", fg="white")
        self.btn_higher.grid(row=0, column=0, padx=10)

        self.btn_lower = tk.Button(self.btn_frame, text="MENOR ↓", command=lambda: self.handle_play("lower"),
                                  width=10, height=2, font=("Arial", 12, "bold"), bg="#C62828", fg="white")
        self.btn_lower.grid(row=0, column=1, padx=10)

        # Status y Historial
        self.lbl_status = tk.Label(self.root, text="¡Suerte!", font=("Arial", 12, "italic"), bg="#1A472A", fg="#FFEB3B")
        self.lbl_status.pack(pady=10)

        self.lbl_history = tk.Label(self.root, text="Historial: ", font=("Consolas", 10), bg="#1A472A", fg="white", wraplength=400)
        self.lbl_history.pack(side="bottom", pady=20)

        # Bind tecla R
        self.root.bind('<r>', lambda e: self.start_new_game())
        self.root.bind('<R>', lambda e: self.start_new_game())

    def format_card_val(self, val: int) -> str:
        return f"{self.value_map.get(val, str(val))}{random.choice(self.suits)}"

    def update_ui(self, message=""):
        # Actualizar carta
        self.lbl_card.config(text=self.format_card_val(self.engine.current_card))

        # Actualizar textos
        self.lbl_score.config(text=f"Score: {self.engine.score}")
        self.lbl_streak.config(text=f"Racha: {self.engine.streak}")
        self.lbl_deck_count.config(text=f"Cartas restantes: {len(self.engine.deck)}/52")

        # Calcular y colorear probabilidades
        p = self.engine.calculate_probabilities()
        self.lbl_prob.config(text=f"P(Mayor): {p['higher']:.1f}% | P(Menor): {p['lower']:.1f}% | P(Igual): {p['equal']:.1f}%")

        if message:
            self.lbl_status.config(text=message)

        # Historial (últimos 8)
        self.lbl_history.config(text="Historial: " + " ".join(self.engine.history[-8:]))

    def handle_play(self, guess: str):
        prev_card = self.engine.current_card
        next_card, is_win, was_reset = self.engine.check_guess(guess)

        card_repr = self.format_card_val(next_card)

        if next_card == prev_card:
            msg = "⚖️ ¡EMPATE! No pierdes racha"
            self.engine.history.append(f"{card_repr}=")
        elif is_win:
            msg = "✨ ¡CORRECTO!"
            self.engine.history.append(f"{card_repr}✓")
        else:
            msg = f"💥 GAME OVER (Era {next_card}). Pulsa R"
            self.engine.history.append(f"{card_repr}✗")
            self.btn_higher.config(state="disabled")
            self.btn_lower.config(state="disabled")

        if was_reset:
            msg += " | 🔀 Mazo Reiniciado"

        self.update_ui(msg)

    def start_new_game(self):
        self.engine.start_new_game()
        self.btn_higher.config(state="normal")
        self.btn_lower.config(state="normal")
        self.update_ui("¡Nueva partida! Elige:")

if __name__ == "__main__":
    app_root = tk.Tk()
    game = GameView(app_root)
    app_root.mainloop()
