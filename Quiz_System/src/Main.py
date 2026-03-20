from  QuestionMaker import Create_question
from  QuestionMaker.Create_question import Design
import customtkinter as ctk
from Tester import tester
from Tester.tester import GUI
import tkinter as tk
if __name__ == "__main__":
    root = tk.Tk()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root.title("Question Maker")
    root.geometry("600x500")
    root.resizable(False, False)
    btn_style = {
    "corner_radius": 20,         
    "border_width": 2,            
     "border_color": "#0a0a0a",   
    "fg_color": "#FAF0F0",      
    "hover_color": "#1a6fa8",    
    "text_color": "#0B0B0B",      
}   

    label = ctk.CTkLabel(root, text="Welcome Smart Test Application", font=ctk.CTkFont(size=20),text_color="#0b0a0b")
    label.pack(pady=(100,30))


    def open_question_maker():
     root.destroy()     
     Design()            

    def open_tester():
     root.destroy()     
     GUI() 

     
    Q_btn = ctk.CTkButton(root, text="Question Maker",
                               font=ctk.CTkFont(size=14, weight="bold"),
                               width=200, height=50,
                               **btn_style,
                               command=open_question_maker) 
    Q_btn.pack(pady=10)
    T_btn = ctk.CTkButton(root, text="Tester",
                               font=ctk.CTkFont(size=14, weight="bold"),
                               width=200, height=50,
                               **btn_style,
                               command=open_tester) 
    T_btn.pack(pady=10)
    
    exit_btn = ctk.CTkButton(root, text="Exit",
                               font=ctk.CTkFont(size=14, weight="bold"),
                               width=100, height=50,
                               **btn_style,
                               command=root.destroy) 
    exit_btn.pack(pady=10)
    root.mainloop()