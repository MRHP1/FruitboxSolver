# Fruitbox Solver

A Python-based interactive puzzle game inspired by the original "Fruitbox" web game, integrated with multiple Algorithm solvers (Greedy, DFS, Dijkstra) to automatically solve the puzzle and compare their performance.

Built as a Quiz 2 Group Project for the Design and Analysis of Algorithms course.

**Authors:**

- Aryaka Leorgi Epridaka — 5025231117
- Muhammad Risyad Himawan Putra — 5025231205
- Yahya Ayyash Ashdaqi — 5025231210

---

## How to Play

A grid is filled with random numbers from 1 to 9. Your goal is to click and drag to select a rectangle of cells whose numbers sum to exactly 10. Valid selections turn green and are cleared. The game ends when no valid move remains or the timer runs out.

---

## How to Run

### Step 1 — Download This Project

**Option A — via Git (if Git is installed):**

```
git clone https://github.com/your-repo/FruitboxSolver.git
cd FruitboxSolver
```

**Option B — Download ZIP:**

1. Download the project as a `.zip` file
2. Extract it to any folder (e.g., `C:\Users\YourName\FruitboxSolver`)

---

### Step 3 — Install Required Library

This project only needs one external library: **pygame-ce**. Install it by running:

```
pip install pygame-ce
```

Wait until the installation finishes. You only need to do this **once**.

---

### Step 4 — Run the Game

Inside the project folder, run:

```
python main.py
```

The game window will open.

---

## Algorithm Solver Panel

During gameplay, a panel on the **right side** of the screen lets you test the AI solvers:

| Button                             | Function                                             |
| ---------------------------------- | ---------------------------------------------------- |
| **Greedy / DFS / Dijkstra** | Select which algorithm to use                        |
| **Run Solver**               | Solve the current board using the selected algorithm |
| **Benchmark All**            | Run all 4 algorithms and compare their performance   |
| **Auto-Play**                | Watch the solver execute its moves one by one        |
| **Stop**                     | Cancel the auto-play                                 |
