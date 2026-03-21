# 🧠 Smart Quiz Application

A Python-based quiz application that allows teachers to create tests and students to take them through a simple graphical interface.

---

## 📌 Project Overview

The Smart Quiz Application consists of two main components:

- **Question Maker** — allows teachers to create tests by uploading a `.txt` file or typing questions manually. Each test is assigned a unique code and saved to a central registry.
- **Tester** — allows students to enter a test code, answer questions within a time limit, and receive an automatic grade. Results are saved to a CSV file.

---

## 🗂️ Project Structure

```
Quiz_System/
├── src/
│   ├── QuestionMaker/
│   │   └── Create_question.py   # Question Maker GUI
│   ├── Tester/
│   │   └── tester.py            # Tester GUI
│   ├── Data/                    # Stores question JSON files
│   ├── Result/                  # Stores student result CSV files
│   ├── Main.py                  # Entry point
│   └── test_registry.json       # Registry of all created tests
└── Tests/
    └── sample_questions.txt     # Sample question file
```

---

## ⚙️ Dependencies and Installation

### Requirements
- Python 3.10 or higher
- CustomTkinter

### Install Dependencies

```bash
pip install customtkinter
```

### All Required Libraries

| Library | Purpose | Built-in? |
|---|---|---|
| `customtkinter` | GUI framework | No — install via pip |
| `tkinter` | Base GUI | Yes |
| `json` | Read/write question files | Yes |
| `csv` | Save student results | Yes |
| `os` | File path management | Yes |
| `threading` | Countdown timer | Yes |
| `pathlib` | Path handling | Yes |
| `datetime` | Record result timestamps | Yes |
| `random`, `string` | Generate unique test codes | Yes |

---

## ▶️ Steps to Run the Code

### 1. Clone or download the project

```bash
git clone <your-github-link>
cd Quiz_System
```

### 2. Install dependencies

```bash
pip install customtkinter
```

### 3. Run the Question Maker (Teacher)

```bash
python src/QuestionMaker/Create_question.py
```

### 4. Run the Tester (Student)

```bash
python src/Tester/tester.py
```

---

## 📄 Sample Question File Format

When uploading questions from a `.txt` file, use this format:

```
What is the capital of France?
A) Paris
B) London
C) Berlin
D) Rome
ANSWER: A

What is 2 + 2?
A) 3
B) 4
C) 5
D) 6
ANSWER: B
```

---

## 🔗 GitHub Link

> https://github.com/yannseaklay2412-cmyk/Python.git

---

## 👤 Author

> _Yann Laiey & Mai Sreynuth_
