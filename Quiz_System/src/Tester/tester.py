# from questionmaker import load_registry
# from questionmaker import get_grade
# from timeset import Timer
# import csv
# import  json
# from datetime import datetime
# class Tester:
#  def tester_menu():
#     print("\n ─────────────────────────────┐")
#     print("  │           TESTER            │")
#     print("  └─────────────────────────────┘")

#     name = input("  Enter your name: ").strip()
#     if not name:
#         name = "Unknown"

#     code = input("  Enter test code: ").strip().upper()

    
#     registry = load_registry()
#     if code not in registry:
#         print(f"\n   Code '{code}' not found. Please check and try again.\n")
#         return
#     else:
#      print (f"Time started ! you  have {load_file(timset)} to do your questions")
#      Timer()
#      test_info = registry[code]

#     with open(test_info['questions_file'], 'r') as f:
#         questions = json.load(f)

#     print(f"""
#   ══════════════════════════════════════
#    Test  : {test_info['title']}
#    Name  : {name}
#    Total : {len(questions)} question(s)
#   ══════════════════════════════════════
#   """)

#     input("  Press Enter to start...")
#     print()

    
#     score = 0
#     answers_given = []
#     for i, q in enumerate(questions, start=1):
#         print(f"  Q{i}: {q['question']}")
#         for letter in ['A', 'B', 'C', 'D']:
#             print(f"       {letter}) {q['options'][letter]}")

#         while True:
#             ans = input("  Your answer (A/B/C/D): ").strip().upper()
#             if ans in ['A', 'B', 'C', 'D']:
#                 break
#             print("    Please enter A, B, C, or D.")

#         correct = q['answer']
#         if ans == correct:
#             print("   Correct!\n")
#             score += 1
#         else:
#             print(f"   Wrong! Correct answer: {correct}\n")

#         answers_given.append(ans)

#     # Step 4: Result + Grade
#     total = len(questions)
#     percentage = round((score / total) * 100, 1)
#     grade = get_grade(percentage)
#     taken_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#     print(f"""
#   ╔══════════════════════════════════════╗
#   ║           YOUR RESULT                ║
#   ╠══════════════════════════════════════╣
#   ║  Name       : {name[:22]:<22}        ║
#   ║  Score      : {str(score)+'/'+str(total)+' ('+str(percentage)+'%)':<22} ║
#   ║  Grade      : {grade:<22}            ║
#   ║  Date/Time  : {taken_at:<22}         ║
#   ╚══════════════════════════════════════╝
#     """)

#     # Save result to shared results file (CRUD — Append)
#     results_file = test_info['results_file']
#     with open(results_file, 'a', newline='') as f:
#         writer = csv.DictWriter(f, fieldnames=[
#             'name', 'score', 'total', 'percentage', 'grade',
#             'answers_given', 'taken_at'
#         ])
#         writer.writerow({
#             'name': name,
#             'score': score,
#             'total': total,
#             'percentage': f"{percentage}%",
#             'grade': grade,
#             'taken_at': taken_at
#         })

#     print(f"   Result saved to: {results_file}\n")


import customtkinter as ctk
import os
import threading
# from questionmaker import load_registry #to read the test registry JSON file and find test info by code from questionmaker
# from questionmaker import get_grade #convert a percentage score to grade (A/B/C/D/F)
# from questionmaker import timerset #countdown timer based on time limit set
import csv # write tester result in csv file
import  json #read and write questions in json file
from datetime import datetime
class GUI:
    #This is the  1  page where  we  allow  tester  to  start  their  test
    def __init__(self):
      self.app = ctk.CTk()
      self.app.title("SMART TEST")  
      self.app.geometry("600x500")
      self.app.resizable(False, False)  
      ctk.set_appearance_mode("dark")
      ctk.set_default_color_theme("blue")
      self.question=[]
      self.current=0
      self.score=0

      self.show_home()
      self.app.mainloop()

      self.title=ctk.CTkLabel(self.app,text="Welcome to Smart Test",font=ctk.CTkFont(size=28,weight="bold"))
      self.title.pack(pady=40)


      self.subtitle=ctk.CTkLabel(self.app,text="Test your  memory",font=ctk.CTkFont(size=16),text_color="gray")
      self.subtitle.pack()

      self.start_btn=ctk.CTkButton(self.app,text="Start Here",font=ctk.CTkFont(size=18,weight="bold"),width=200,height=50,command=self.start )
      self.start_btn.pack(pady=60)
      self.app.mainloop()
    def start(self):
        print("Let start!!")

    def clear_screen(self):
        for widget in self.app.winfo_children():
            widget.destroy()


    def show_home(self):
        self.clear_screen()

        ctk.CTkLabel(
            self.app,
            text="🧠 SMART TEST",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=30)

        self.code_entry = ctk.CTkEntry(
            self.app,
            placeholder_text="Enter your name",
            width=200, height=45,
            font=ctk.CTkFont(size=16)
        )
        self.code_entry.pack(pady=14)

        self.code_entry = ctk.CTkEntry(
            self.app,
            placeholder_text="Enter your code",
            width=200, height=45,
            font=ctk.CTkFont(size=16)
        )
        self.code_entry.pack(pady=14)

        # 👇 Start button
        ctk.CTkButton(
            self.app,
            text="▶ Start Quiz",
            width=200, height=50,
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.start
        ).pack(pady=10)

        #funtion  to enter  the test 


    def load_questions(self, code):
        if not os.path.exists(self.REGISTRY_FILE):
            return False

        with open(self.REGISTRY_FILE, 'r') as f:
            registry = json.load(f)

        if code not in registry:
            return False

        questions_file = registry[code]['questions_file']
        with open(questions_file, 'r') as f:
            self.questions = json.load(f)

        return True


def start_quiz(self):
    code = self.code_entry.get().strip().upper()

    if self.load_questions(code):
        self.current = 0
        self.score = 0
        self.show_question()
    else:
        # show error message
        ctk.CTkLabel(
            self.app,
            text="Invalid code! Try again.",
            text_color="red"
        ).pack()
if __name__ == "__main__":  
    gui=GUI()
    gui.show_home()
    gui.start_quiz() #call the function to start the quiz when the start button is clicked
class Tester:
    def __init__(self):
        self.REGISTRY_FILE = 'test_registry.json'
        self.name = "" #test taker name
        self.score = 0 
        self.answers_given = [] #to store the answers given by the test taker
        self.test_info = None 
        self.questions = []
        self.timer = None

#_________________helper__________________
    def load_registry(self): #use to check  if  file  exit
        if not os.path.exists(self.REGISTRY_FILE): #if file .json fail crate it will return nothing 
            print("Fail to load registry file")
            return {}
        with open(self.REGISTRY_FILE, 'r') as f: #it open  json  file  that  we  already convert  and  convert  it to the test questions
            return json.load(f)
    def get_grade(self, percentage):
        if percentage >= 90:
            print("Excellent work!")
            return 'A'
        elif percentage >= 80:
            print("Great job!")
            return 'B'
        elif percentage >= 70:
            print("Good effort!")
            return 'C'
        elif percentage >= 60:
            print("Keep trying!")
            return 'D'
        else:
            print("Don't give up :)")
            return 'F'  
#_______________time___________________    
    def timerset(self, minutes):
        seconds = minutes * 60
        def time_up():
            print("""   ╔══════════════════════════════════════╗
                        ║            TIME IS UP!               ║
                        ║   Your answers have been submitted!  ║
                        ╚══════════════════════════════════════╝  """)
            os._exit(0)  
        self.timer =threading.Timer(seconds, time_up)
        self.timer.start()
        print(f" You have {minutes} minute(s) to complete the test!\n")
            
    
    def result_grade(self): #Result + Grade
        total = len(self.questions)
        percentage = round((self.score / total) * 100, 1)
        grade = self.get_grade(percentage)
        taken_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #datetime.now() gets the current date and time.strftime() formats it into a readable format.
        # datetime.now() is python standard library 
        print(f"""
                    ╔══════════════════════════════════════╗
                    ║           YOUR RESULT                ║
                    ╠══════════════════════════════════════╣
                    ║  Name       : {self.name[:22]:<22}        ║
                    ║  Score      : {str(self.score)+'/'+str(total)+' ('+str(percentage)+'%)':<22} ║
                    ║  Grade      : {grade:<22}            ║
                    ║  Date/Time  : {taken_at:<22}         ║
                    ╚══════════════════════════════════════╝
                                                                """)

        # Save result to shared results file (CRUD — Append)
        results_file = self.test_info['results_file']
        with open(results_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'name', 'score', 'total', 'percentage', 'grade',
                'answers_given', 'taken_at'
            ])
            writer.writerow({
                'name': self.name,
                'score': self.score,
                'total': total,
                'percentage': f"{percentage}%",
                'grade': grade,
                'answers_given': self.answers_given,
                'taken_at': taken_at
            })


        print(f"   Result saved to: {results_file}\n")
        self.timer.cancel()  # Stop the timer if test completed before time is up
#_________________tester_menu__________________        
    def tester_menu(self):
        print("\n  ┌─────────────────────────────┐")
        print("  │           TESTER            │")
        print("  └─────────────────────────────┘")

        self.name = input("  Enter your name: ").strip() #remove space start and end (empty space))
        if not self.name:
            self.name = "Unknown"

        code = input("  Enter test code: ").strip().upper()

    
        registry = self.load_registry()
        if code not in registry:
            print(f"\n   Code '{code}' not found. Please check and try again.\n")
            return
        self.test_info = registry[code]

        self.minutes = self.test_info.get('minutes', 10)

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
        self.timerset(self.minutes) #start the timer
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

            correct = q['answer']
            if ans == correct:
                print("   Correct!\n")
                self.score += 1
            else:
                print(f"   Wrong! Correct answer: {correct}\n")

            self.answers_given.append(ans)
        self.result_grade()    

#________________run_directly______________________    

if __name__ == '__main__':
    tester = Tester()
    while True:
        print("""
╔══════════════════════════════════════════╗
║               Tester_Menu                ║
╠══════════════════════════════════════════╣
║  1. Take a Test                          ║
║  2. Exit                                 ║
╚══════════════════════════════════════════╝""")
        choice = input("  Choose an option (1/2): ").strip()
        if choice == '1':
            tester.tester_menu()
        elif choice == '2':
            print("\n  Goodbye!\n")
            break
        else:
            print("    Invalid choice. Please try again.")        

