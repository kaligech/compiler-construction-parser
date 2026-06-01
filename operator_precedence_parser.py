import tkinter as tk
from tkinter import ttk

# ---------------------------------
# Operator Precedence Table
# < = shift
# > = reduce
# e = error
# ---------------------------------

precedence_table = {

    '+': {'+': '>', '*': '<', 'id': '<', '$': '>'},

    '*': {'+': '>', '*': '>', 'id': '<', '$': '>'},

    'id': {'+': '>', '*': '>', 'id': 'e', '$': '>'},

    '$': {'+': '<', '*': '<', 'id': '<', '$': 'accept'}
}


# ---------------------------------
# Parser Function
# ---------------------------------

def parse_expression(expression):

    # Split expression into tokens
    tokens = expression.split()

    # Add end symbol
    tokens.append('$')

    stack = ['$']

    history = []

    i = 0

    while len(stack) > 0:

        top = stack[-1]

        current_token = tokens[i]

        # Update current stack label
        stack_status.config(
            text="Current Stack: " + " ".join(stack)
        )

        relation = precedence_table.get(top, {}).get(current_token, 'e')

        stack_content = " ".join(stack)

        remaining_input = " ".join(tokens[i:])

        # Shift operation
        if relation == '<' or relation == '=':

            action = f"Shift {current_token}"

            history.append(
                (stack_content,
                 remaining_input,
                 action)
            )

            stack.append(current_token)

            i += 1

        # Reduce operation
        elif relation == '>':

            action = "Reduce"

            history.append(
                (stack_content,
                 remaining_input,
                 action)
            )

            stack.pop()

        # Accept expression
        elif relation == 'accept':

            history.append(
                (stack_content,
                 remaining_input,
                 "ACCEPT")
            )

            return True, history

        # Reject expression
        else:

            history.append(
                (stack_content,
                 remaining_input,
                 "REJECT")
            )

            return False, history


# ---------------------------------
# Clear Table
# ---------------------------------

def clear_table():

    for row in table.get_children():

        table.delete(row)


# ---------------------------------
# Clear All
# ---------------------------------

def clear_all():

    clear_table()

    entry_field.delete(0, tk.END)

    token_label.config(text="Tokens: ")

    stack_status.config(text="Current Stack: ")

    status_label.config(
        text="STATUS: Waiting for Input",
        fg="gray"
    )


# ---------------------------------
# Run Parser
# ---------------------------------

def run_parser():

    clear_table()

    user_input = entry_field.get()

    # Check empty input
    if len(user_input.strip()) == 0:

        status_label.config(
            text="Please enter expression",
            fg="orange"
        )

        return

    # Show tokens
    token_label.config(
        text="Tokens: " + str(user_input.split())
    )

    success, parsing_history = parse_expression(user_input)

    # Add parser steps to table
    for step in parsing_history:

        table.insert("", "end", values=step)

    # Final result
    if success:

        status_label.config(
            text="STATUS: Expression Accepted",
            fg="green"
        )

    else:

        status_label.config(
            text="STATUS: Expression Rejected",
            fg="red"
        )


# ---------------------------------
# Main Window
# ---------------------------------

window = tk.Tk()

window.title("Operator Precedence Parser")

window.geometry("850x650")


# ---------------------------------
# Grammar Section
# ---------------------------------

grammar_frame = tk.LabelFrame(
    window,
    text="Grammar",
    padx=10,
    pady=10
)

grammar_frame.pack(fill="x", padx=10, pady=5)

grammar_label = tk.Label(
    grammar_frame,
    text="""
E → E + E
E → E * E
E → id
""",
    justify="left",
    font=("Arial", 11)
)

grammar_label.pack(anchor="w")


# ---------------------------------
# Precedence Table Section
# ---------------------------------

matrix_frame = tk.LabelFrame(
    window,
    text="Precedence Matrix",
    padx=10,
    pady=10
)

matrix_frame.pack(fill="x", padx=10, pady=5)

matrix_text = """
      +     *     id     $
+     >     <      <      >
*     >     >      <      >
id    >     >      e      >
$     <     <      <    accept
"""

matrix_label = tk.Label(
    matrix_frame,
    text=matrix_text,
    justify="left",
    font=("Courier New", 10)
)

matrix_label.pack(anchor="w")


# ---------------------------------
# Input Section
# ---------------------------------

top_frame = tk.Frame(window)

top_frame.pack(pady=10)

input_label = tk.Label(
    top_frame,
    text="Enter Expression:"
)

input_label.pack(side=tk.LEFT, padx=5)

entry_field = tk.Entry(
    top_frame,
    width=35
)

entry_field.pack(side=tk.LEFT, padx=5)

parse_button = tk.Button(
    top_frame,
    text="Parse",
    command=run_parser,
    bg="#4CAF50",
    fg="white"
)

parse_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(
    top_frame,
    text="Clear",
    command=clear_all,
    bg="#f44336",
    fg="white"
)

clear_button.pack(side=tk.LEFT, padx=5)


# ---------------------------------
# Token Display
# ---------------------------------

token_label = tk.Label(
    window,
    text="Tokens: ",
    font=("Arial", 10, "bold")
)

token_label.pack(pady=5)


# ---------------------------------
# Stack Status
# ---------------------------------

stack_status = tk.Label(
    window,
    text="Current Stack: ",
    font=("Arial", 10, "bold")
)

stack_status.pack(pady=5)


# ---------------------------------
# Table Section
# ---------------------------------

table_frame = tk.Frame(window)

table_frame.pack(
    pady=10,
    fill=tk.BOTH,
    expand=True
)

table = ttk.Treeview(
    table_frame,
    columns=("Stack", "Input", "Action"),
    show="headings"
)

table.heading("Stack", text="Stack")

table.heading("Input", text="Remaining Input")

table.heading("Action", text="Action")

table.pack(
    fill=tk.BOTH,
    expand=True,
    padx=20
)


# ---------------------------------
# Status Label
# ---------------------------------

status_label = tk.Label(
    window,
    text="STATUS: Waiting for Input",
    font=("Arial", 12, "bold"),
    fg="gray"
)

status_label.pack(pady=10)


# ---------------------------------
# Start GUI
# ---------------------------------

window.mainloop()