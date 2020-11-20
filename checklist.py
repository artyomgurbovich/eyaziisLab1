import tkinter as tk

class ChecklistBox(tk.Frame):
    def __init__(self, parent, choices, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.vars = []
        bg = self.cget("background")
        for choice in choices:
            var = tk.BooleanVar()
            self.vars.append(var)
            cb = tk.Checkbutton(self, var=var, text=choice,
                                onvalue=1, offvalue=0,
                                anchor="w", width=55, background=bg,
                                relief="flat", highlightthickness=0
            )
            cb.pack(side="top", fill="x", anchor="w")

    def update(self, choices):
        self.vars = []
        for widget in self.winfo_children():
            widget.destroy()
        for choice in choices:
            var = tk.BooleanVar()
            self.vars.append(var)
            cb = tk.Checkbutton(self, var=var, text=choice,
                                onvalue=1, offvalue=0,
                                anchor="w", width=55,
                                relief="flat", highlightthickness=0
            )
            cb.pack(side="top", fill="x", anchor="w")

    def getCheckedItems(self):
        values = []
        for i, v in enumerate(self.vars):
            value = v.get()
            if value:
                values.append(i)
        return set(values)