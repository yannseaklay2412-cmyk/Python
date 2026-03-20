
import customtkinter as ctk
import os
import threading
# from questionmaker import load_registry #to read the test registry JSON file and find test info by code from questionmaker
# from questionmaker import get_grade #convert a percentage score to grade (A/B/C/D/F)
# from questionmaker import timerset #countdown timer based on time limit set
import csv # write tester result in csv file
import  json #read and write questions in json file
from datetime import datetime



class Tester:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.REGISTRY_FILE = os.path.join(BASE_DIR, '..', 'test_registry.json')
        self.name = ""
        self.score = 0
        self.answers_given = []
        self.test_info = None
        self.questions = []
        self._timer_running = False
        self.timer_thread = None
        self.remaining_seconds = 0

# ── helper ────────────────────────────────────────────
    def load_registry(self):
     print(f"Looking for registry at: {os.path.abspath(self.REGISTRY_FILE)}")
     print(f"Current working directory: {os.getcwd()}")
    
     if not os.path.exists(self.REGISTRY_FILE):
        print("Fail to load registry file")
        return {}
     with open(self.REGISTRY_FILE, 'r') as f:
        return json.load(f)

    def get_grade(self, percentage):
        if percentage >= 90:
            return 'A', "Excellent work! "
        elif percentage >= 80:
            return 'B', "Great job! "
        elif percentage >= 70:
            return 'C', "Good effort! "
        elif percentage >= 60:
            return 'D', "Keep trying! "
        else:
            return 'F', "Don't give up! "

    def timerset(self, minutes, tick_callback=None, time_up_callback=None):
        self.remaining_seconds = minutes * 60
        self._timer_running = True

        def countdown():
            while self.remaining_seconds > 0 and self._timer_running:
                if tick_callback:
                    tick_callback(self.remaining_seconds)
                threading.Event().wait(1)
                self.remaining_seconds -= 1
            if self._timer_running and self.remaining_seconds <= 0:
                if time_up_callback:
                    time_up_callback()

        self.timer_thread = threading.Thread(target=countdown, daemon=True)
        self.timer_thread.start()

    def stop_timer(self):
        self._timer_running = False

    def save_result(self):
        total = len(self.questions)
        if total == 0:
            return
        percentage = round((self.score / total) * 100, 1)
        grade, _ = self.get_grade(percentage)
        taken_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        results_file = self.test_info['results_file']
        if not os.path.isabs(results_file):
            base_dir = os.path.dirname(os.path.abspath(self.REGISTRY_FILE))
            results_file = os.path.join(base_dir, results_file)

        with open(results_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'name', 'score', 'total', 'percentage',
                'grade', 'answers_given', 'taken_at'
            ])
            writer.writerow({
                'name':          self.name,
                'score':         self.score,
                'total':         total,
                'percentage':    f"{percentage}%",
                'grade':         grade,
                'answers_given': str(self.answers_given),
                'taken_at':      taken_at
            })
        print(f"   Result saved to: {results_file}\n")

    def tester_menu(self):
        print("\n  ┌─────────────────────────────┐")
        print("  │           TESTER            │")
        print("  └─────────────────────────────┘")

        self.name = input("  Enter your name: ").strip()
        if not self.name:
            self.name = "Unknown"

        code = input("  Enter test code: ").strip().upper()
        registry = self.load_registry()

        if code not in registry:
            print(f"\n   Code '{code}' not found. Please check and try again.\n")
            return

        self.test_info = registry[code]
        minutes = self.test_info.get('time limit', 10)

        with open(self.test_info['questions_file'], 'r') as f:
            self.questions = json.load(f)

        print(f"""
  ══════════════════════════════════════
   Test  : {self.test_info['title']}
   Name  : {self.name}
   Total : {len(self.questions)} question(s)
  ══════════════════════════════════════
  """)
        input("  Press Enter to start...")
        print()

        def time_up_terminal():
            print("""
  ╔══════════════════════════════════════╗
  ║            TIME IS UP!               ║
  ║   Your answers have been submitted!  ║
  ╚══════════════════════════════════════╝
            """)
            os._exit(0)

        self.timerset(minutes, time_up_callback=time_up_terminal)
        print(f" You have {minutes} minute(s) to complete the test!\n")

        self.score = 0
        self.answers_given = []

        for i, q in enumerate(self.questions, start=1):
            print(f"  Q{i}: {q['question']}")
            for letter in ['A', 'B', 'C', 'D']:
                print(f"       {letter}) {q['options'][letter]}")
            while True:
                ans = input("  Your answer (A/B/C/D): ").strip().upper()
                if ans in ['A', 'B', 'C', 'D']:
                    break
                print("    Please enter A, B, C, or D.")

            if ans == q['answer']:
                print("   Correct!\n")
                self.score += 1
            else:
                print(f"   Wrong! Correct answer: {q['answer']}\n")
            self.answers_given.append(ans)

        total = len(self.questions)
        percentage = round((self.score / total) * 100, 1)
        grade, msg = self.get_grade(percentage)
        taken_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(msg)
        print(f"""
  ╔══════════════════════════════════════╗
  ║           YOUR RESULT                ║
  ╠══════════════════════════════════════╣
  ║  Name  : {self.name[:28]:<28}  ║
  ║  Score : {str(self.score)+'/'+str(total)+' ('+str(percentage)+'%)':<28}  ║
  ║  Grade : {grade:<28}  ║
  ║  Time  : {taken_at:<28}  ║
  ╚══════════════════════════════════════╝
        """)
        self.save_result()
        self.stop_timer()



class GUI:
    def __init__(self):
        self.tester = Tester()     

        self.app = ctk.CTk()
        self.app.title("SMART TEST")
        self.app.geometry("600x500")
        self.app.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.timer_label = None

        self.show_home()            
        self.app.mainloop()        

    def clear_screen(self):
        for widget in self.app.winfo_children():
            widget.destroy()

    # ══════════════════════════════
    #  PAGE 1 — HOME
    # ══════════════════════════════
    def show_home(self):
        self.clear_screen()

        ctk.CTkLabel(self.app,text="🧠 SMART TEST",font=ctk.CTkFont(size=28, weight="bold")).pack(pady=30)

        self.name_entry = ctk.CTkEntry(self.app,placeholder_text="Enter your name",width=200, height=45,font=ctk.CTkFont(size=16))
        self.name_entry.pack(pady=14)

        self.code_entry = ctk.CTkEntry(self.app,placeholder_text="Enter your code",width=200, height=45,font=ctk.CTkFont(size=16))
        self.code_entry.pack(pady=14)

        self.error_lbl = ctk.CTkLabel(self.app,text="",text_color="red",font=ctk.CTkFont(size=14))
        self.error_lbl.pack()

        ctk.CTkButton(self.app,text="Start Quiz",width=200, height=50,font=ctk.CTkFont(size=18, weight="bold"),command=self.start_quiz).pack(pady=10)

    # ══════════════════════════════
    #  PAGE 2 — QUESTION
    # ══════════════════════════════
    def show_question(self):
        self.clear_screen()
        t = self.tester

        if t.current >= len(t.questions):
            self.finish_quiz()
            return

        q = t.questions[t.current]
        total = len(t.questions)

        bar = ctk.CTkFrame(self.app, fg_color="#1a1a2e", corner_radius=0, height=50)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        ctk.CTkLabel(bar, text=f"Q {t.current+1} / {total}",font=ctk.CTkFont(size=14, weight="bold"),text_color="#00c8ff").pack(side="left", padx=16)
        ctk.CTkLabel(bar, text=f"❤️{t.score} pts",font=ctk.CTkFont(size=14, weight="bold"),text_color="#00ff99").pack(side="right", padx=16)
        self.timer_label = ctk.CTkLabel(bar,font=ctk.CTkFont(size=14, weight="bold"),text_color="#ffc93c")
        self.timer_label.pack(side="right", padx=4)

        prog = ctk.CTkProgressBar(self.app, height=4, progress_color="#00c8ff")
        prog.pack(fill="x")
        prog.set(t.current / total)

        q_box = ctk.CTkFrame(self.app, fg_color="#1a1a2e", corner_radius=10)
        q_box.pack(padx=30, pady=16, fill="x")
        ctk.CTkLabel(q_box, text=q['question'],font=ctk.CTkFont(size=16, weight="bold"),wraplength=500, justify="left").pack(padx=20, pady=14)

        btn_colors = {
            'A': ("#1bd9c9", "#1347E3"),
            'B': ("#f47adf", "#1347E3"),
            'C': ("#84822a", "#1347E3"),
            'D': ("#AA4BF8", "#1347E3"),
        }
        
        for letter in ['A', 'B', 'C', 'D']:
            fg, hv = btn_colors[letter]
            ctk.CTkButton(self.app,text=f"  {letter})  {q['options'][letter]}",height=44, font=ctk.CTkFont(size=14),anchor="w", corner_radius=8,fg_color=fg, hover_color=hv,command=lambda l=letter: self.answer_selected(l)).pack(padx=30, pady=4, fill="x")

    # ══════════════════════════════
    #  PAGE 3 — RESULTS
    # ══════════════════════════════
    def show_results(self, timed_out=False):
        self.clear_screen()
        t     = self.tester
        total = len(t.questions)
        pct   = round((t.score / total) * 100, 1) if total else 0
        grade, msg = t.get_grade(pct)

        grade_color = {'A': "#00ff99", 'B': "#66ccff",'C': "#ffc93c", 'D': "#ff8800", 'F': "#ff4466"}.get(grade, "white")

        title = "TIME'S UP!" if timed_out else "Quiz Complete!"
        ctk.CTkLabel(self.app, text=title,font=ctk.CTkFont(size=26, weight="bold"),text_color="#ff4466" if timed_out else "#00c8ff").pack(pady=(30, 4))
        ctk.CTkLabel(self.app, text=msg,font=ctk.CTkFont(size=14), text_color="gray").pack()
        ctk.CTkLabel(self.app, text=grade,font=ctk.CTkFont(size=72, weight="bold"),text_color=grade_color).pack(pady=8)

        card = ctk.CTkFrame(self.app, fg_color="#1a1a2e", corner_radius=12)
        card.pack(padx=60, pady=4, fill="x")
        for lbl, val in [
            ("Name",  t.name),
            ("Test",  t.test_info.get('title', '—')),
            ("Score", f"{t.score} / {total}  ({pct}%)"),
            ("Saved", t.test_info.get('results_file', '—')),
        ]:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=2)
            ctk.CTkLabel(row, text=lbl, font=ctk.CTkFont(size=12), text_color="gray", width=55, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=val, font=ctk.CTkFont(size=13), text_color="white", anchor="w").pack(side="left", padx=8)

        btn_row = ctk.CTkFrame(self.app, fg_color="transparent")
        btn_row.pack(pady=16)
        ctk.CTkButton(btn_row, text="Try Again", width=160, height=44,command=self.show_home).pack(side="left", padx=8)
        ctk.CTkButton(btn_row, text="Exit", width=120, height=44,fg_color="#3a0010", hover_color="#280009",command=self.app.destroy).pack(side="left", padx=8)


    def load_questions(self, code):
        """Loads registry and questions for the given code into self.tester.
           Returns True if successful, False if code not found."""
        registry = self.tester.load_registry()
        normalized_registry = {k.strip().upper(): (k, v) for k, v in registry.items()}

        if code not in normalized_registry:
            return False

        t = self.tester
        t.test_info = normalized_registry[code][1]

        with open(t.test_info['questions_file'], 'r') as f:
            t.questions = json.load(f)

        return True

    def start_quiz(self):
        """Called when the Start Quiz button is clicked."""
        name = self.name_entry.get().strip()
        code = self.code_entry.get().strip().upper()

        if not name:
            self.error_lbl.configure(text="⚠ Please enter your name.")
            return
        if not code:
            self.error_lbl.configure(text="⚠ Please enter the test code.")
            return

        if not self.load_questions(code):
            self.error_lbl.configure(text=f"⚠ Code '{code}' not found.")
            return

        t               = self.tester
        t.name          = name
        t.score         = 0
        t.current       = 0
        t.answers_given = []

        minutes = t.test_info.get('time limit', 10)
        t.timerset(minutes,tick_callback=self._tick,time_up_callback=lambda: self.app.after(0, self._time_up))

        self.show_question()

    def answer_selected(self, letter):
        t = self.tester
        if letter == t.questions[t.current]['answer']:
            t.score += 1
        t.answers_given.append(letter)
        t.current += 1
        self.show_question()

    def finish_quiz(self):
        self.tester.stop_timer()
        try:
            self.tester.save_result()
        except Exception:
            pass
        self.show_results(timed_out=False)

    def _time_up(self):
        self.tester.stop_timer()
        try:
            self.tester.save_result()
        except Exception:
            pass
        self.show_results(timed_out=True)

    def _tick(self, remaining):
        mins  = remaining // 60
        secs  = remaining % 60
        color = "#ff4466" if remaining <= 30 else "#ffc93c"
        try:
            self.app.after(0, lambda: self.timer_label and
                           self.timer_label.configure(text=f"{mins:02d}:{secs:02d}",text_color=color))
        except Exception:
            pass


#  ONLY this at the bottom — no gui.show_home() or gui.start_quiz()
if __name__ == '__main__':
    GUI()