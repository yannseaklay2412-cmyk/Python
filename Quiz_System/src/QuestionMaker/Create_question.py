import os
import csv
import json
import random
import string
from tkinter import filedialog, messagebox
import customtkinter as ctk
import tkinter as tk
from datetime import datetime

class Question_maker:
 def __init__(self):
     self.upload_question=[]
     self.REGISTRY_FILE = 'test_registry.json' 
     self.typein_question=[]
    
  #=============================================================================================   
 def generate_code(self,length=6): #use to generate code
    chars = string.ascii_uppercase + string.digits 
    return ''.join(random.choices(chars, k=length))
#=============================================================================================
 def load_registry(self):
    if not os.path.exists(self.REGISTRY_FILE):
        print(" No registry file found. Creating a new one...")
        return {}
    print(" Registry loaded successfully!")
    with open(self.REGISTRY_FILE, 'r') as f:
        return json.load(f)
#=============================================================================================
 def save_registry(self,registry):
    with open(self.REGISTRY_FILE, 'w') as f:
        json.dump(registry, f, indent=2) 
#=============================================================================================
 
#=============================================================================================
 
#=============================================================================================
    

   


#=============================================================================================


class Design(Question_maker):
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.title("Question Maker")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
       
       
        btn_style = {
    "corner_radius": 20,         
    "border_width": 2,            
     "border_color": "#0a0a0a",   
    "fg_color": "#FAF0F0",      
    "hover_color": "#1a6fa8",    
    "text_color": "#050505",     
    
}   
        self.first_page()
        
        self.start_btn=ctk.CTkButton(self.root,text="Upload Questions from File",font=ctk.CTkFont(size=14,weight="bold"),width=150,height=50,command=self.upload_questions_from_file,**btn_style) 
        self.start_btn.pack(pady=(10)) 

        self.start_btn=ctk.CTkButton(self.root,text="Type Questions Manually",font=ctk.CTkFont(size=14,weight="bold"),width=150 ,height=50,command=self.second,**btn_style) 
        self.start_btn.pack(pady=10)
    
        self.exit_btn = ctk.CTkButton(self.root, text="Exit",
                               font=ctk.CTkFont(size=14, weight="bold"),
                               width=100, height=50,
                               **btn_style,
                               command=self.root.destroy) 
        self.exit_btn.pack(pady=10)

        self.root.mainloop()
    def register_test(self, questions, title="Untitled Test",time_limit=10):
        registry = self.load_registry()

        # Generate unique code
        code = self.generate_code()
        while code in registry:
            code = self.generate_code()

        # Save questions to a JSON file
        questions_file = f'questions_{code}.json'
        with open(questions_file, 'w') as f:
            json.dump(questions, f, indent=2)

        if not title:
            title = "Untitled Test"

        # Create results CSV file
        titlee = title.strip().replace(' ', '_')
        results_file = f'results_{titlee}.csv'
        with open(results_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'name', 'score', 'total', 'percentage', 'grade',
                'answers_given', 'taken_at'
            ])
            writer.writeheader()

        # Register in registry
        registry[code] = {
            'title': title,
            'time limit': time_limit,
            'questions_file': questions_file,
            'results_file': results_file,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_questions': len(questions)
        }
        self.save_registry(registry)
    
        return code




    #function to  access upload file from file explorer
    def upload_questions_from_file(self):
     file_path = filedialog.askopenfilename(
        title="Select a Text File",
        filetypes=[("Text Files", "*.txt")]
    )
     if  not file_path: 
        print("Can't Open File.")
     self.load_questions_from_file(file_path) 
     if self.upload_question:
            messagebox.showinfo("Success!", f"{len(self.upload_question)} question(s) loaded successfully!")
     else:
            messagebox.showwarning("No Questions Found", "No valid questions were found in the file.")
    
    def second(self):
        self.clear_screen()
        self.label = ctk.CTkLabel(self.root, text="How  many question you want to make?", font=ctk.CTkFont(size=20),text_color="#0b0a0b")
        self.label.pack(pady=(80,30))
        self.amount_entry = ctk.CTkEntry(self.root,
                                placeholder_text="Amount",
                                width=150, height=50,
                                justify="center",
                                font=ctk.CTkFont(size=16))
        self.amount_entry.pack(pady=(40, 10))
        self.save_btn = ctk.CTkButton(self.root, text="Confirm",width=100, height=50,
                                    font=ctk.CTkFont(size=14, weight="bold"),
                                    command=self.questions)
        self.save_btn.pack(pady=20)
     
    
    def questions(self):
        amount = self.amount_entry.get().strip()
        
        if not amount.isdigit() or int(amount) <= 0: 
            messagebox.showwarning("Warning", "Please enter a valid number!")
            return
        
        self.upload_question = []
        self.current_question = 1
        self.total_questions = int(amount)
        self.type_in_q()
        # Question
    def type_in_q(self):
        self.clear_screen()
        self.label = ctk.CTkLabel(self.root, text=f"Question {self.current_question} of {self.total_questions}", font=ctk.CTkFont(size=15), text_color="#2b21f1")
        self.label.pack(pady=10)
        self.question_entry = ctk.CTkEntry(self.root,
                                placeholder_text="Enter your question",
                                width=400, height=100,
                                justify="center",
                                font=ctk.CTkFont(size=16))
        self.question_entry.pack(pady=(10, 10))

       

        self.option_entries = {}
        for option in range(1,5): 
                entry = ctk.CTkEntry(self.root,
                                    placeholder_text=f"Option {option}",
                                    width=200, height=40,
                                    font=ctk.CTkFont(size=14))
                entry.pack(padx=(10,200))
                entry.pack(pady=5)
                self.option_entries[option] = entry  

        
        self.answer_entry = ctk.CTkEntry(self.root,
                                placeholder_text="Correct Answer (A/B/C/D)",
                                width=200, height=40,
                                font=ctk.CTkFont(size=14))
        self.answer_entry.pack(pady=10)

        # Save button
        self.save_btn = ctk.CTkButton(self.root, text="Save Question",width=100, height=50,
                                      
                                    font=ctk.CTkFont(size=14, weight="bold"),
                                    command=self.append_question)  
        self.save_btn.pack(pady=20)
    def append_question(self):
        question_text = self.question_entry.get().strip()
        options = {letter: entry.get().strip() for letter, entry in self.option_entries.items()}
        answer = self.answer_entry.get().strip().upper()

        if not question_text or any(not opt for opt in options.values()) or answer not in ['A', 'B', 'C', 'D']:
            messagebox.showwarning("Warning", "Please fill in all fields correctly!")
            return

        self.upload_question.append({
            'question': question_text,
            'options': options,
            'answer': answer
        })
        if self.current_question < self.total_questions:
         self.current_question += 1
         self.type_in_q()
        else:
         self.info() 


    def info(self):   
         self.clear_screen()
         self.title_entry = ctk.CTkEntry(self.root,placeholder_text="Enter Quiz title",width=300,height=40,font=ctk.CTkFont(size=16))
         self.title_entry.pack(pady=10)
         self.time_entry = ctk.CTkEntry(self.root,placeholder_text="Time limit",width=300,height=40,font=ctk.CTkFont(size=16))
         self.time_entry.pack(pady=10)
         self.code = self.generate_code()
         self.save_btn = ctk.CTkButton(self.root, text="Save Question",
                                    font=ctk.CTkFont(size=14, weight="bold"),
                                    command=lambda: [self.save_test_info(), self.root.destroy()])
         self.save_btn.pack(pady=20)

       
    def save_test_info(self):
         title = self.title_entry.get() .strip() 
         time_limit = self.time_entry.get().strip()
      
         if not title:
            messagebox.showwarning("Warning", "Please enter a title!")
            return
         if not time_limit.isdigit() or int(time_limit) <= 0:
             messagebox.showwarning("Warning", "Please enter a valid time!")
             return
         
    
         code = self.register_test(self.upload_question,
                               title=title,
                               time_limit=int(time_limit))

         messagebox.showinfo("Success",
                f"Test Created!\n"
                f"Title: {title}\n"
                f"Code: {code}\n"
                f"Questions: {len(self.upload_question)}\n"
                f"Time limit: {time_limit} min")

         self.first_page()


    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    def first_page(self):
        self.clear_screen()
        self.label = ctk.CTkLabel(self.root, text="Welcome to Question Maker Section!", font=ctk.CTkFont(size=20),text_color="#0b0a0b")
        self.label.pack(pady=(100,30))
if __name__ == "__main__":  
    gui=Design()
