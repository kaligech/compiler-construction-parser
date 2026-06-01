import tkinter as tk
from tkinter import ttk, messagebox

# TABLES 
PRECEDENCE_TABLE = {
    '+':  {'+': '>', '-': '>', '*': '<', '/': '<', '(': '<', ')': '>', 'id': '<', '$': '>'},
    '-':  {'+': '>', '-': '>', '*': '<', '/': '<', '(': '<', ')': '>', 'id': '<', '$': '>'},
    '*':  {'+': '>', '-': '>', '*': '>', '/': '>', '(': '<', ')': '>', 'id': '<', '$': '>'},
    '/':  {'+': '>', '-': '>', '*': '>', '/': '>', '(': '<', ')': '>', 'id': '<', '$': '>'},
    '(':  {'+': '<', '-': '<', '*': '<', '/': '<', '(': '<', ')': '=', 'id': '<', '$': 'err'},
    ')':  {'+': '>', '-': '>', '*': '>', '/': '>', '(': 'err', ')': '>', 'id': 'err', '$': '>'},
    'id': {'+': '>', '-': '>', '*': '>', '/': '>', '(': 'err', ')': '>', 'id': 'err', '$': '>'},
    '$':  {'+': '<', '-': '<', '*': '<', '/': '<', '(': '<', ')': 'err', 'id': '<', '$': 'acc'}
}

# BACKTRACKING PARSER LOGIC 
# Grammar: S -> aAd | aBc, A -> b, B -> b
class BacktrackingParser:
    def __init__(self, input_str):
        self.tokens = input_str.replace(" ", "")
        self.pos = 0
        self.steps = []

    def parse(self):
        self.steps.append(f"Starting Parse for: {self.tokens}")
        result = self.S()
        if result and self.pos == len(self.tokens):
            return True, self.steps
        return False, self.steps

    def match(self, char):
        if self.pos < len(self.tokens) and self.tokens[self.pos] == char:
            self.pos += 1
            return True
        return False

    def S(self):
        initial_pos = self.pos
        self.steps.append(f"Trying S -> aAd at pos {self.pos}")
        # Try Rule 1: S -> aAd
        if self.match('a'):
            if self.A():
                if self.match('d'):
                    return True
        
        # Backtrack
        self.steps.append(f"FAILED Rule 1, Backtracking to pos {initial_pos}")
        self.pos = initial_pos
        
        # Try Rule 2: S -> aBc
        self.steps.append(f"Trying S -> aBc at pos {self.pos}")
        if self.match('a'):
            if self.B():
                if self.match('c'):
                    return True
        return False

    def A(self):
        self.steps.append("  Trying A -> b")
        return self.match('b')

    def B(self):
        self.steps.append("  Trying B -> b")
        return self.match('b')
    
# GUI CLASS 
class ParsingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Compiler Construction: Parsing Techniques")
        self.root.geometry("1000x800")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # Create Tabs
        self.tab_op = ttk.Frame(self.notebook)
        self.tab_bt = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_op, text="Operator Precedence")
        self.notebook.add(self.tab_bt, text="Backtracking")

        self.setup_operator_ui()
        self.setup_backtracking_ui()

    # Operator Precedence UI 
    def setup_operator_ui(self):
        # Input
        input_frame = tk.Frame(self.tab_op)
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Expression (e.g. id + id * id):").pack(side=tk.LEFT)
        self.op_entry = tk.Entry(input_frame, width=30)
        self.op_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="Parse", command=self.run_operator, bg="green", fg="white").pack(side=tk.LEFT)

        # Precedence Table Display
        table_label = tk.Label(self.tab_op, text="Operator Precedence Table", font=('Arial', 10, 'bold'))
        table_label.pack()
        
        terms = ['+', '-', '*', '/', '(', ')', 'id', '$']
        self.op_tree_table = ttk.Treeview(self.tab_op, columns=terms, height=8)
        for t in terms: self.op_tree_table.heading(t, text=t); self.op_tree_table.column(t, width=40, anchor='center')
        self.op_tree_table.pack(pady=5)
        for row_term in terms:
            vals = [PRECEDENCE_TABLE[row_term].get(c, ' ') for c in terms]
            self.op_tree_table.insert('', 'end', text=row_term, values=vals)

        # Process Table
        self.op_process = ttk.Treeview(self.tab_op, columns=("Stack", "Input", "Action"), show='headings', height=10)
        self.op_process.heading("Stack", text="Stack"); self.op_process.heading("Input", text="Input"); self.op_process.heading("Action", text="Action")
        self.op_process.pack(expand=True, fill='both', padx=10)

        self.op_canvas = tk.Canvas(self.tab_op, height=150, bg="white")
        self.op_canvas.pack(fill='x', padx=10, pady=5)

    def run_operator(self):
        raw_input = self.op_entry.get()
        tokens = []
        for t in raw_input.split():
            tokens.append('id' if t.isdigit() else t)
        tokens.append('$')
        
        self.op_process.delete(*self.op_process.get_children())
        stack = ['$']
        i = 0
        
        while True:
            top = stack[-1]
            current = tokens[i]
            
            if top not in PRECEDENCE_TABLE or current not in PRECEDENCE_TABLE[top]:
                self.op_process.insert('', 'end', values=(" ".join(stack), " ".join(tokens[i:]), "ERROR"))
                break
                
            relation = PRECEDENCE_TABLE[top][current]
            self.op_process.insert('', 'end', values=(" ".join(stack), " ".join(tokens[i:]), f"Relation: {relation}"))

            if relation == '<' or relation == '=':
                stack.append(current)
                i += 1
            elif relation == '>':
                stack.pop() # Reduction
            elif relation == 'acc':
                messagebox.showinfo("Success", "Accepted by Operator Precedence!")
                self.draw_simple_tree(tokens[:-1])
                break
            else:
                messagebox.showerror("Error", "String Rejected")
                break

    #  Backtracking UI 
    def setup_backtracking_ui(self):
        tk.Label(self.tab_bt, text="Grammar: S -> aAd | aBc, A -> b, B -> b", font=("Arial", 10, "italic")).pack(pady=5)
        
        input_frame = tk.Frame(self.tab_bt)
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Input (e.g. abc or abd):").pack(side=tk.LEFT)
        self.bt_entry = tk.Entry(input_frame, width=20)
        self.bt_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="Parse with Backtracking", command=self.run_backtracking, bg="blue", fg="white").pack(side=tk.LEFT)

        self.bt_log = tk.Listbox(self.tab_bt, height=15)
        self.bt_log.pack(expand=True, fill='both', padx=10)

    def run_backtracking(self):
        self.bt_log.delete(0, tk.END)
        parser = BacktrackingParser(self.bt_entry.get())
        success, steps = parser.parse()
        for step in steps:
            self.bt_log.insert(tk.END, step)
        
        if success:
            messagebox.showinfo("Result", "Accepted via Backtracking!")
        else:
            messagebox.showerror("Result", "Rejected")

    def draw_simple_tree(self, tokens):
        self.op_canvas.delete("all")
        # Simplified dynamic display
        x_start = 50
        y = 80
        self.op_canvas.create_text(300, 20, text="Simplified Bottom-Up Reduction View", font=("Arial", 10, "bold"))
        self.op_canvas.create_text(300, 40, text="E", font=("Arial", 14))
        
        for i, t in enumerate(tokens):
            x = x_start + (i * 60)
            self.op_canvas.create_text(x, y, text=t, font=("Arial", 12))
            self.op_canvas.create_line(300, 50, x, y-10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ParsingApp(root)
    root.mainloop()