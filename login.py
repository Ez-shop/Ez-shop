import tkinter as tk
from tkinter import messagebox
import subprocess
from database import add_user, check_user, get_user_id

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Ez-Shop Login")
        self.root.geometry("1200x700+0+0")
        self.root.config(bg="#fafafa")

        # Variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.new_username_var = tk.StringVar()
        self.new_password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()

        # GUI Elements
        self.create_widgets()

    def create_widgets(self):
        login_frame = tk.Frame(self.root, bg="white")
        login_frame.place(x=350, y=100, width=500, height=500)

        title = tk.Label(login_frame, text="Ez-Shop", font=("Impact", 35, "bold"), bg="white", fg="#1877f2")
        title.place(x=180, y=30)

        # Login/Signup Tabs
        self.login_label = tk.Label(login_frame, text="Login", font=("times new roman", 18, "bold"), bg="white", fg="#1877f2")
        self.login_label.place(x=120, y=100)
        self.login_label.bind("<Button-1>", lambda e: self.show_panel("login"))

        self.signup_label = tk.Label(login_frame, text="Signup", font=("times new roman", 18, "bold"), bg="white", fg="gray")
        self.signup_label.place(x=320, y=100)
        self.signup_label.bind("<Button-1>", lambda e: self.show_panel("signup"))

        # Panels
        self.login_panel = self.create_login_panel(login_frame)
        self.signup_panel = self.create_signup_panel(login_frame)
        self.show_panel("login")

    def create_login_panel(self, parent):
        panel = tk.Frame(parent, bg="white")
        
        tk.Label(panel, text="Username", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=20)
        tk.Entry(panel, textvariable=self.username_var, font=("times new roman", 15)).place(x=50, y=50, width=350)
        
        tk.Label(panel, text="Password", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=90)
        tk.Entry(panel, textvariable=self.password_var, show="*", font=("times new roman", 15)).place(x=50, y=120, width=350)
        
        tk.Button(panel, text="Login", command=self.login, bg="#1877f2", fg="white", font=("times new roman", 15, "bold")).place(x=50, y=200, width=350)
        return panel

    def create_signup_panel(self, parent):
        panel = tk.Frame(parent, bg="white")
        
        tk.Label(panel, text="Username", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=20)
        tk.Entry(panel, textvariable=self.new_username_var, font=("times new roman", 15)).place(x=50, y=50, width=350)
        
        tk.Label(panel, text="Password", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=90)
        tk.Entry(panel, textvariable=self.new_password_var, show="*", font=("times new roman", 15)).place(x=50, y=120, width=350)
        
        tk.Label(panel, text="Confirm Password", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=160)
        tk.Entry(panel, textvariable=self.confirm_password_var, show="*", font=("times new roman", 15)).place(x=50, y=190, width=350)
        
        tk.Button(panel, text="Signup", command=self.signup, bg="#1877f2", fg="white", font=("times new roman", 15, "bold")).place(x=50, y=240, width=350)
        return panel

    def show_panel(self, panel_type):
        self.login_panel.place_forget()
        self.signup_panel.place_forget()
        self.clear_fields()

        if panel_type == "login":
            self.login_panel.place(x=0, y=150, width=500, height=300)
            self.login_label.config(fg="#1877f2")
            self.signup_label.config(fg="gray")
        else:
            self.signup_panel.place(x=0, y=150, width=500, height=300)
            self.signup_label.config(fg="#1877f2")
            self.login_label.config(fg="gray")

    def clear_fields(self):
        self.username_var.set("")
        self.password_var.set("")
        self.new_username_var.set("")
        self.new_password_var.set("")
        self.confirm_password_var.set("")

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        if check_user(username, password):
            messagebox.showinfo("Success", "Welcome to Ez-Shop!")
            self.root.destroy()  # Close login window

            # Debugging: Print the command being executed
            print(f"Launching TheEmporium.py with username: {username}")
            try:
                subprocess.Popen(['python', 'TheEmporium.py', username])
            except Exception as e:
                print(f"Error launching TheEmporium.py: {e}")
        else:
            messagebox.showerror("Error", "Invalid credentials!")


    def signup(self):
        username = self.new_username_var.get()
        password = self.new_password_var.get()
        confirm_password = self.confirm_password_var.get()

        if not all([username, password, confirm_password]):
            messagebox.showerror("Error", "All fields are required!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords don't match!")
            return

        if add_user(username, password):
            messagebox.showinfo("Success", "Account created successfully!")
            self.show_panel("login")
        else:
            messagebox.showerror("Error", "Username already exists!")

if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.mainloop()