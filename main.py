import tkinter as tk
import random
import string

class WordGridSolver:
    def __init__(self, master, grid):
        self.master = master
        self.master.title("Word Grid Solver")
        self.grid = grid
        self.words_to_find = []

        self.word_entry = tk.Entry(master)
        self.word_entry.pack()

        self.word_button = tk.Button(master, text="Add Word", command=self.add_word)
        self.word_button.pack()

        self.solve_button = tk.Button(master, text="Solve", command=self.solve_grid)
        self.solve_button.pack()
        
        self.background_image = tk.PhotoImage(file="ocean.png")

        self.canvas = tk.Canvas(master, width=600, height=600)
        self.canvas.pack()

        self.found_words_label = tk.Label(master, text="Found Words:", font=("Arial", 14, "bold"), fg="white", bg="black")
        self.found_words_label.pack()
        self.found_words_text = tk.Text(master, height=10, width=30, font=("Arial", 12), bg="black", fg="white")
        self.found_words_text.pack()

        self.used_indices = []

        self.draw_background()

    def add_word(self):
        word = self.word_entry.get().upper()
        if word not in self.words_to_find:
            self.words_to_find.append(word)

    def draw_background(self):
        image_width = self.canvas.winfo_width()
        image_height = self.canvas.winfo_height()
        self.background_image_resized = self.background_image.zoom(image_width, image_height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image_resized)

    def display_grid(self):
        for i, row in enumerate(self.grid):
            for j, letter in enumerate(row):
                cell_size = 100
                color = '#{:02x}{:02x}{:02x}'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                self.canvas.create_rectangle(j*cell_size, i*cell_size, (j+1)*cell_size, (i+1)*cell_size, fill=color, outline="")
                self.canvas.create_text(j*cell_size + cell_size//2, i*cell_size + cell_size//2, text=letter, fill='white')

    def solve_grid(self):
        found_words = []

        for word in self.words_to_find:
            found = False
            for i in range(len(self.grid)):
                for j in range(len(self.grid[0])):
                    if self.grid[i][j] == word[0]:
                        indices = [(i, j)]
                        if self.dfs_search(word, i, j, set(), indices):
                            found_words.append(f"'{word}' found")
                            self.draw_red_line(indices)
                            found = True
                            break
                if found:
                    break
            if not found:
                found_words.append(f"'{word}' not found")

        self.display_found_words(found_words)

    def dfs_search(self, word, i, j, visited, indices, index=0):
        if index == len(word):
            return True

        if i < 0 or i >= len(self.grid) or j < 0 or j >= len(self.grid[0]):
            return False
        if (i, j) in visited:
            return False
        
        if self.grid[i][j] != word[index]:
            return False

        visited.add((i, j))

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if self.dfs_search(word, i+dx, j+dy, visited, indices + [(i+dx, j+dy)], index+1):
                    return True

        visited.remove((i, j))
        return False

    def draw_red_line(self, indices):
        for idx in indices:
            i, j = idx
            self.canvas.create_rectangle(j*100, i*100, (j+1)*100, (i+1)*100, outline="red", width=3)

    def display_found_words(self, found_words):
        self.found_words_text.delete('1.0', tk.END)
        for word in found_words:
            self.found_words_text.insert(tk.END, str(word) + "\n")
       
        self.found_words_text.pack(side=tk.TOP, pady=(50, 0))

def generate_random_grid(rows, cols):
    letters = string.ascii_uppercase
    grid = [[random.choice(letters) for _ in range(cols)] for _ in range(rows)]
    return grid


def main():
    grid=generate_random_grid(6, 6)

    root = tk.Tk()
    app = WordGridSolver(root, grid)
    app.display_grid()
    root.mainloop()

if __name__ == "__main__":
    main()

