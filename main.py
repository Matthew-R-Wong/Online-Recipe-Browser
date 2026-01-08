##-----------------------------------------------------------------------
## File : main.py
##
## Programmer: Matthew Wong
##
## Program #: Final Project
##
## Due Date: 12/09/2025
##
## Course: EGRE 347, Spring 2020
##
## Pledge: I have neither given nor received unauthorized aid on this program.
##
## Description: This program acts as an interactive recipe manager GUI. It uses
##              the tkinter library to create a physical window where users can
##              add, edit, view, and delete recipes. The program requires a monitor
##              to display the GUI and allows users to manage their recipes easily.
##              Additionally, it uses a text file to store and load the recipies
##              so that the same recipes are available across multiple runs.
##
##-----------------------------------------------------------------------

import tkinter as tk
from recipe_ui import menu_manager

if __name__ == "__main__":
    root = tk.Tk()
    menu = menu_manager(root)
    root.mainloop()