
import tkinter as tk


#================================================================#
# Calculator | Jarrod Burns | ta747839@gmail.com | 10/19/2021    #
# Revision 1.0.1 - Update before commit                          #
#================================================================#


class Calc:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.grid()
        self.master.title("Calculator")

        self.x_value = ""
        self.y_value = ""
        self.sign = ""

        self.sign_hotkeys = {
            "/": "KP_Divide",
            "*": "KP_Multiply",
            "+": "KP_Add",
            "-": "KP_Subtract"
        }

        self.int_buttons = dict()
        self.integers = ['9', '8', '7', '6', '5', '4', '3', '2', '1']
        for index, element in enumerate(self.integers):

            self.int_buttons[index] = tk.Button(
                self.frame,
                text=index + 1,
                padx=29,
                pady=12,
                command=lambda x=str(index + 1): self.button_click(x),
                font=("Segoe", 12, "bold")
            )
            self.int_buttons[index].grid(
                row=((int(element) + 2) // 3) + 1,
                column=index % 3
            )

        self.zero_btn = tk.Button(
            self.frame,
            text="0",
            padx=69,
            pady=12,
            command=lambda x="0": self.button_click(x),
            font=("Segoe", 12, "bold")
        )
        self.zero_btn.grid(row=5, column=0, columnspan=2, sticky="s")

        self.text_box = tk.Text(
            self.frame,
            state="disabled",
            height=1,
            width=13,
            font=("Segoe", 32)
        )
        self.text_box.grid(row=0, column=0, columnspan=4)

        self.backspace_btn = tk.Button(
            self.frame,
            text="←",
            padx=5,
            pady=12,
            command=self.backspace,
            font=("Segoe", 12, "bold")
        )
        self.backspace_btn.grid(row=1, column=0, sticky="w")

        self.clear_btn = tk.Button(
            self.frame,
            text="C",
            padx=7,
            pady=12,
            command=self.clear,
            font=("Segoe", 12, "bold")
        )
        self.clear_btn.grid(row=1, column=0, sticky="e")

        self.equals_btn = tk.Button(
            self.frame,
            text="=",
            padx=28,
            pady=40,
            command=self.equals,
            font=("Segoe", 12, "bold")
        )
        self.equals_btn.grid(row=4, column=3, rowspan=2, sticky="s")

        self.additon_btn = tk.Button(
            self.frame,
            text="+",                                   # Enterd as: Alt 43
            padx=28,
            pady=39,
            command=lambda x="+": self.sign_operation(x),
            font=("Segoe", 12, "bold")
        )
        self.additon_btn.grid(row=2, column=3, rowspan=2, sticky="s")

        self.subtract_btn = tk.Button(
            self.frame,
            text="-",                                   # Enterd as: Alt 45
            padx=30,
            pady=12,
            command=lambda x="-": self.sign_operation(x),
            font=("Segoe", 12, "bold")
        )
        self.subtract_btn.grid(row=1, column=3)

        self.multiplication_btn = tk.Button(
            self.frame,
            text="×",                                   # Enterd as: Alt 0215
            padx=29,
            pady=12,
            command=lambda x="*": self.sign_operation(x),
            font=("Segoe", 12, "bold")
        )
        self.multiplication_btn.grid(row=1, column=2)

        self.division_btn = tk.Button(
            self.frame,
            text="÷",                                   # Enterd as: Alt 0247
            padx=29,
            pady=12,
            command=lambda x="/": self.sign_operation(x),
            font=("Segoe", 12, "bold")
        )
        self.division_btn.grid(row=1, column=1)

        self.decimal_btn = tk.Button(
            self.frame,
            text=".",
            padx=31,
            pady=12,
            command=self.decimal,
            font=("Segoe", 12, "bold")
        )
        self.decimal_btn.grid(row=5, column=2, sticky="se")

        # rjust hack; pass "tag-right" to insert statements.
        self.text_box.tag_configure('tag-right', justify='right')

        # Hot key binding assignments.
        for num in range(0, 10):
            num = str(num)
            self.frame.bind_all(num or "KP_" + num,
                                lambda event, x=num: self.button_click(x))

        for k, v in self.sign_hotkeys.items():
            self.frame.bind_all(k or v,
                                lambda event, x=k: self.sign_operation(x))

        self.frame.bind_all("<Return>" or "KP_Enter", lambda event: self.equals())
        self.frame.bind_all("<BackSpace>", lambda event: self.backspace())
        self.frame.bind_all("." or "KP_Decimal", lambda event: self.decimal())
        self.frame.bind_all("c", lambda event: self.clear())

        # Sets the ledger display to zero on application startup.
        self.text_box.configure(state="normal")
        self.insert_ledger("0")
        self.text_box.configure(state="disabled")

    def state_config(func, *args, **kwargs):
        """
        This decorator unlocks the textbox for data insertion during a
        method call and then locks the textbox after method resolution.
        """

        def wrapper(self, *args, **kwargs):
            self.text_box.configure(state="normal")
            func(self, *args, **kwargs)
            self.text_box.configure(state="disabled")

        return wrapper

    def insert_commas(self, value):
        """
        Adds commas for display.
        """

        # :, will chop off trailing zeros after the decimal place,
        # the split call lets us represent a number like 5,000.00001
        if "." in value:
            t = value.split(".")
            return f"{int(t[0]):,}." + t[1]
        else:
            return f"{int(value):,}"

    def reset_values(self):
        self.x_value = ""
        self.y_value = ""
        self.sign = ""

    def clear_ledger(self):
        self.text_box.delete(1.0, "end")

    def insert_ledger(self, value):
        self.text_box.insert(1.0, value, "tag-right")

    @ state_config
    def button_click(self, btn_value):

        if len(self.x_value) < 11:
            self.clear_ledger()
            self.x_value += btn_value
            self.insert_ledger(self.insert_commas(self.x_value))

        # Block multi-zero inputs before decimal place
        if len(self.x_value) == 1 and not int(btn_value) and "." not in self.x_value:
            self.x_value = ""

    @ state_config
    def backspace(self):
        if len(self.x_value) > 1:
            self.x_value = self.x_value[:-1]
        else:
            # Resets display if last number is backspaced
            self.x_value = "0"

        self.clear_ledger()
        self.insert_ledger(self.insert_commas(self.x_value))

    @ state_config
    def clear(self):
        self.reset_values()
        self.clear_ledger()
        self.insert_ledger("0")

    @ state_config
    def sign_operation(self, sign):
        """
        Handles multiplication, division, subtraction,
        and addition operations.
        """
        if len(self.x_value) > 0:
            self.sign = sign
            self.y_value = self.x_value
            self.x_value = ""
            self.clear_ledger()

    @ state_config
    def decimal(self):
        if len(self.x_value) < 1:
            self.x_value = "0."
            self.insert_ledger(self.x_value)

        if "." not in self.x_value:
            self.clear_ledger()
            self.x_value += "."
            self.insert_ledger(self.insert_commas(self.x_value))

    @ state_config
    def equals(self):
        if self.x_value:
            solution = str(eval(self.y_value + self.sign + self.x_value))
            self.clear_ledger()
            self.insert_ledger(self.insert_commas(solution))
            self.reset_values()

            # Replace display if solution is above max display size.
            if len(solution) > 11 and "." not in solution:
                self.clear_ledger()
                self.insert_ledger("sum > 10^11")

            # Display approximation of decimals if above max display size
            if len(solution) > 10 and "." in solution:
                self.clear_ledger()
                self.insert_ledger("≈" + self.insert_commas(solution))  # Alt 247


if __name__ == "__main__":
    window = tk.Tk()
    app = Calc(window)
    window.mainloop()
