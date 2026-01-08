##-----------------------------------------------------------------------
## File : recipe_ui.py
##
## Description: This program converts assignment #6 to work using python code
##				and acts as a state machine that parses through individual bytes
##              to make sure the GPS information is correct, and then output
##              the information that is correct. Additionally, the LED implementation
##              required for the C++ version is not included.
##-----------------------------------------------------------------------

import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

from recipe import Recipe
from recipe_manager import recipe_manager

TOTAL_WINDOW_WIDTH = 1200
TOTAL_WINDOW_HEIGHT = 800


## class menu_manager
##
## Description:
##
##   Coordinates the main application window, creates and lays out frames
##   and widgets, handles user events, and delegates data persistence to
##   the recipe_manager instance.
##
## Data members:
##
##   root : Main Tkinter window.
##   recipe_menu : Add recipe Toplevel instance.
##   edit_menu : Edit menu Toplevel instance.
##   hold_true_tags : Formatted string of recipes matching tag filters.
##   tag_state : Mapping tag -> BooleanVar for filters.
##   recipe_manager : Data manager for recipes.
##   recipe_list : list of recipes from the manager.
##   all_tags : tag list from the manager.
##   chosen_recipe : Currently selected recipe name.
##   Frame widgets: UI layout containers used across methods.
##
## Methods:
##
##   __init__ - build UI layout, load recipes, and initialize state.
##   update_window - refresh recipe displays when selection changes.
##   new_recipe - open or reuse the add-recipe dialog and handle submission.
##   edit_recipe - open the edit dialog pre-filled with the selected recipe.
##   clear_display - destroy existing detail widgets before redraw.
##   delete_recipe - remove the selected recipe and refresh UI/storage.
##   toggle_tags - rebuild tag selector UI and attach trace callbacks.
##   update_tag_list - compute recipes matching active tags and display.
##   show_tag_list - render the filtered recipe list in a read-only widget.
##   show_tags - display tags for the selected recipe.
##   show_recipe - display ingredient list for the selected recipe.
##   show_description - display the selected recipe's description.
##   show_photo - load, resize, and display the recipe's photo.

class menu_manager:

    ## __init__(self, root)
    ##
    ## Summary of the constructor function:
    ##
    ## Initializes the UI manager, builds frames and widgets, and loads
    ## recipes from disk.
    ##
    ## Parameters : root (top level Tkinter window)
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Configures window geometry, creates frames for layout, instantiates
    ## the recipe_manager, and sets up initial widget states and bindings.

    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Manager")


        self.recipe_menu = None
        self.hold_true_tags = ""
        self.tag_state = {}

        self.recipe_manager = recipe_manager()
        self.recipe_manager.load_recipes()
        self.recipe_list = self.recipe_manager.recipe_list
        self.all_tags = self.recipe_manager.all_tags

        self.chosen_recipe = tk.StringVar()

        self.top_frame = Frame(root, bg="lightgrey")
        self.top_frame.pack(side="top", fill="both", expand=True)
        self.bottom_frame = Frame(root, bg="lightgrey")
        self.bottom_frame.pack(side="bottom", fill="both", expand=True)

        self.top_left_frame = Frame(self.top_frame, bg="lightgrey")
        self.top_left_frame.pack(side="left", fill="both", expand=True)
        self.top_right_frame = Frame(self.top_frame, bg="lightgrey")
        self.top_right_frame.pack(side="right", fill="both", expand=True)
        
        self.bottom_left_frame = Frame(self.bottom_frame, bg="lightgrey")
        self.bottom_left_frame.pack(side="left", fill="both", expand=True)
        self.bottom_right_frame = Frame(self.bottom_frame, bg="lightgrey")
        self.bottom_right_frame.pack(side="right", fill="both", expand=True)

        self.left_frame = Frame(self.top_left_frame, bg="lightgrey")
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.right_frame = Frame(self.top_left_frame, bg="lightgrey")
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.description_label_frame = Frame(self.bottom_right_frame, bg="lightgrey")
        self.description_label_frame.pack(side="top", fill="x", expand=False)
        self.description_frame = Frame(self.bottom_right_frame, bg="lightgrey")
        self.description_frame.pack(side="top", fill="both", expand=True)
        
        self.add_item_frame = Frame(self.right_frame, bg="lightgrey")
        self.add_item_frame.pack(side="left", fill="both", expand=True)
        self.edit_item_frame = Frame(self.right_frame, bg="lightgrey")
        self.edit_item_frame.pack(side="right", fill="both", expand=True)

        self.below_browser_frame = Frame(self.left_frame, bg="lightgrey")
        self.below_browser_frame.pack(side="bottom", fill="both", expand=True)
        self.below_add_button_frame = Frame(self.add_item_frame, bg="lightgrey")
        self.below_add_button_frame.pack(side="bottom", fill="both", expand=True)
        self.below_edit_button_frame = Frame(self.edit_item_frame, bg="lightgrey")
        self.below_edit_button_frame.pack(side="bottom", fill="both", expand=True)

        self.delete_recipe_button_frame = Frame(self.below_edit_button_frame, bg="lightgrey")
        self.delete_recipe_button_frame.pack(side="top", fill="x", expand=False)
        self.tags_frame = Frame(self.below_edit_button_frame, bg="lightgrey")
        self.tags_frame.pack(side="bottom", fill="both", expand=True)

        self.upper_frame = Frame(self.bottom_left_frame, bg="lightgrey")
        self.upper_frame.pack(side="top", fill = "both", expand=False)
        self.lower_frame = Frame(self.bottom_left_frame, bg="lightgrey")
        self.lower_frame.pack(side="bottom", fill="both", expand=True)

        self.top_left_frame.pack_propagate(False)
        self.top_right_frame.pack_propagate(False)
        self.bottom_left_frame.pack_propagate(False)
        self.bottom_right_frame.pack_propagate(False)

        self.toggle_tags()
        self.box = ttk.Combobox(self.left_frame, textvariable=self.chosen_recipe, values=[item.name for item in self.recipe_list], state="readonly")
        self.box.bind("<<ComboboxSelected>>", self.update_window)

        recipe_label = tk.Label(self.left_frame, text="Recipe Browser", bg="lightgrey")
        add_item = ttk.Button(self.add_item_frame, text="Add Recipe", command=self.new_recipe)
        edit_item = ttk.Button(self.edit_item_frame, text="Edit Recipe", command=self.edit_recipe)
        delete_item = ttk.Button(self.below_edit_button_frame, text="Delete Recipe", command=self.delete_recipe)

        add_item.pack(anchor="nw", padx=25, pady=35)
        edit_item.pack(anchor="nw", padx=25, pady=35)
        delete_item.pack(anchor="nw", padx=18, pady=25)
        recipe_label.pack(anchor="nw", padx=30, pady=(20,0))
        self.box.pack(anchor="nw", padx=30, pady=(0, 36))

        self.root.update_idletasks()
        self.root.geometry(f"{TOTAL_WINDOW_WIDTH}x{TOTAL_WINDOW_HEIGHT}")
        self.root.resizable(width=False, height=False)


    ## update_window(self, event=None)
    ##
    ## Summary of the update window function:
    ##
    ## Refreshes all recipe display areas when a new recipe is selected.
    ##
    ## Parameters : event - optional Tkinter event (Can be ignored because it is never used)
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Calls the helper methods show_recipe, show_photo, show_description,
    ## show_tags, and update_tag_list to update the UI.

    def update_window(self, event=None):
        self.show_recipe()
        self.show_photo()
        self.show_description()
        self.show_tags()
        self.update_tag_list()

    ## new_recipe(self)
    ##
    ## Summary of the new recipe function:
    ##
    ## Opens (or reuses) a Toplevel window for entering a new recipe and
    ## its values.
    ##
    ## Parameters : none
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Builds widgets for name, photo, tags, ingredients and description.
    ## On submission a Recipe is created and added via recipe_manager.

    def new_recipe(self):
        if self.recipe_menu is None or not self.recipe_menu.winfo_exists():
            self.recipe_menu = Toplevel(self.root)
            self.recipe_menu.title("Input Recipe Below")

            menu_instructions = Frame(self.recipe_menu, bg="lightgrey")
            menu_instructions.grid(row=0, column=0, sticky="nsew")
            
            name_var = StringVar()
            photo_name_var = StringVar()
            tags_var = StringVar()

            tk.Label(menu_instructions, text="", bg="lightgrey").grid(row=0, column=0, padx=(50))
            tk.Label(menu_instructions, text="", bg="lightgrey").grid(row=0, column=1, padx=(300))

            tk.Label(menu_instructions, text="Name", bg="lightgrey").grid(row=1, column=0)
            tk.Entry(menu_instructions, textvariable=name_var).grid(row=1, column=1, sticky="ew")

            tk.Label(menu_instructions, text="Photo Name", bg="lightgrey").grid(row=2, column=0)
            tk.Entry(menu_instructions, textvariable=photo_name_var).grid(row=2, column=1, sticky="ew")

            tk.Label(menu_instructions, text="Tags", bg="lightgrey").grid(row=3, column=0)
            tk.Entry(menu_instructions, textvariable=tags_var).grid(row=3, column=1, sticky="ew")

            tk.Label(menu_instructions, text="Ingredients", bg="lightgrey").grid(row=4, column=0)
            ingredients_var = tk.Text(menu_instructions, height=10, width=20)
            ingredients_var.grid(row=4, column=1, sticky="nsew")
            scrollbar = tk.Scrollbar(menu_instructions, command=ingredients_var.yview)
            ingredients_var.config(yscrollcommand=scrollbar.set)
            scrollbar.grid(row=4, column=2, sticky="ns")

            tk.Label(menu_instructions, text="Description", bg="lightgrey").grid(row=5, column=0)
            description_var = tk.Text(menu_instructions, height=10, width=20)
            description_var.grid(row=5, column=1, sticky="nsew")

            ## pair_ingredients()
            ##
            ## Summary of the ingredient parser:
            ##
            ## Parses the contents of the ingredients_var Text widget into
            ## a list of (ingredient, amount) tuples.
            ##
            ## Parameters : none (reads from ingredients_var)
            ##
            ## Return Value : list of tuples (str, str)
            ##
            ## Description:
            ##
            ## Splits text by lines. Each line may be name, amount, or just
            ## name. Trims whitespace and ignores blank lines.

            def pair_ingredients():
                text = ingredients_var.get("1.0", "end-1c")
                split_text = text.split("\n")
                ingredient_pair_array = []
                for item in split_text:
                    item = item.strip()
                    if not item:
                        continue
                    pair = item.split(",", 1)
                    ingredient = pair[0]
                    amount = pair[1] if len(pair) > 1 else ""
                    ingredient_pair_array.append((ingredient.strip(), amount.strip()))
                return ingredient_pair_array

            ## clear_text_boxes()
            ##
            ## Summary of the clear inputs helper:
            ##
            ## Clears the dialog input widgets and hides the Toplevel.
            ##
            ## Parameters : none
            ##
            ## Return Value : none
            ##
            ## Description:
            ##
            ## Resets StringVars' and clears Text widgets, then calls
            ## withdraw() to hide the window for bringing up later.

            def clear_text_boxes():
                name_var.set("")
                photo_name_var.set("")
                tags_var.set("")
                ingredients_var.delete("1.0", "end")
                description_var.delete("1.0", "end")
                self.recipe_menu.withdraw()

            ## submit_recipe()
            ##
            ## Summary of the submit helper:
            ##
            ## Validates and, if valid, creates a new Recipe, adds it via
            ## recipe_manager, and refreshes the UI.
            ##
            ## Parameters : none
            ##
            ## Return Value : none
            ##
            ## Description:
            ##
            ## Ensures the name is not empty, reads form fields, constructs a
            ## Recipe and calls recipe_manager.add_recipe and
            ## save_recipes before updating widgets.

            def submit_recipe():
                if name_var.get() == "":
                    return
                name = name_var.get()
                photo_name = photo_name_var.get()
                tags = tags_var.get().split()
                ingredients = pair_ingredients()
                description = description_var.get("1.0", "end-1c")
                self.recipe_manager.add_recipe(Recipe(name, photo_name, tags, ingredients, description))
                self.recipe_manager.save_recipes()
                self.box["values"] = [item.name for item in self.recipe_manager.recipe_list]
                clear_text_boxes()
                self.toggle_tags()
                self.update_window()

            bottom_frame = Frame(self.recipe_menu, bg="lightgrey")
            bottom_frame.grid(row=1, column=0, padx=10, pady=5)
            ttk.Button(bottom_frame, text="Submit Recipe", command=submit_recipe).grid(row=0, column=0)

            self.recipe_menu.protocol("WM_DELETE_WINDOW", clear_text_boxes)
        else:
            self.recipe_menu.deiconify()

    ## edit_recipe(self, event=None)
    ##
    ## Summary of the edit dialog function:
    ##
    ## Opens a Toplevel dialog pre-filled with the selected recipe's data
    ## for editing.
    ##
    ## Parameters : event - optional Tkinter event (Can be ignored because it is never used)
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Locates the selected Recipe, populates widget variables, and
    ## applies changes via recipe_manager.update_recipe on submit.

    def edit_recipe(self, event=None):
        user_choice = self.chosen_recipe.get()
        if not user_choice:
            return
        
        tags_holder = ""
        ingredients_text = ""
        recipe_object = None

        for item in self.recipe_list:
            if item.name == user_choice:
                recipe_object = item
                name_var = StringVar(value=item.name)
                photo_name_var = StringVar(value=item.photo_name)
                            
                for tag in item.tags:
                    tags_holder += f" {tag}"
                tags_holder = tags_holder.strip()
                tags_var = StringVar(value=tags_holder)

                for object in item.ingredients:
                    ingredient, amount = object
                    ingredient = ingredient.replace(":", "")
                    ingredients_text += f"{ingredient}, {amount}\n"
                
                description_text = item.description
                break
        if recipe_object is None:
            return
        
        self.edit_menu = Toplevel(self.root)
        self.edit_menu.title("Recipe Editor")

        menu_instructions = Frame(self.edit_menu, bg="lightgrey")
        menu_instructions.pack(padx=20, pady=20)

        tk.Label(menu_instructions, text="", bg="lightgrey").grid(row=0, column=0, padx=(50))
        tk.Label(menu_instructions, text="", bg="lightgrey").grid(row=0, column=1, padx=(300))

        tk.Label(menu_instructions, text="Name", bg="lightgrey").grid(row=1, column=0)
        tk.Entry(menu_instructions, textvariable=name_var).grid(row=1, column=1, sticky="ew")

        tk.Label(menu_instructions, text="Photo Name", bg="lightgrey").grid(row=2, column=0)
        tk.Entry(menu_instructions, textvariable=photo_name_var).grid(row=2, column=1, sticky="ew")

        tk.Label(menu_instructions, text="Tags", bg="lightgrey").grid(row=3, column=0)
        tk.Entry(menu_instructions, textvariable=tags_var).grid(row=3, column=1, sticky="ew")

        tk.Label(menu_instructions, text="Ingredients", bg="lightgrey").grid(row=4, column=0)
        ingredients_var = tk.Text(menu_instructions, height=10, width=20)
        ingredients_var.grid(row=4, column=1, sticky="nsew")
        ingredients_var.insert("1.0", ingredients_text)
        scrollbar = tk.Scrollbar(menu_instructions, command=ingredients_var.yview)
        ingredients_var.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=4, column=2, sticky="ns")

        tk.Label(menu_instructions, text="Description", bg="lightgrey").grid(row=5, column=0)
        description_var = tk.Text(menu_instructions, height=10, width=20)
        description_var.grid(row=5, column=1, sticky="nsew")
        description_var.insert("1.0", description_text)

        ## pair_ingredients()
        ##
        ## Summary of the ingredient parser:
        ##
        ## Parses the edit dialog ingredients_var contents into
        ## (ingredient, amount) tuples.
        ##
        ## Parameters : none
        ##
        ## Return Value : list of tuple (str, str)
        ##
        ## Description:
        ##
        ## Similar to the add dialog parser. Reads lines, splits on the
        ## first comma and trims whitespace, ignoring blank lines.

        def pair_ingredients():
            text = ingredients_var.get("1.0", "end-1c")
            split_text = text.split("\n")
            ingredient_pair_array = []
            for item in split_text:
                item = item.strip()
                if not item:
                    continue
                pair = item.split(",", 1)
                ingredient = pair[0]
                amount = pair[1] if len(pair) > 1 else ""
                ingredient_pair_array.append((ingredient.strip(), amount.strip()))
            return ingredient_pair_array
        
        ## clear_text_boxes()
        ##
        ## Summary of the clear helper:
        ##
        ## Clears input widgets and closes the edit dialog window.
        ##
        ## Parameters : none
        ##
        ## Return Value : none
        ##
        ## Description:
        ##
        ## Resets StringVars' and Text widgets then calls destroy() on
        ## the edit dialog to remove it.

        def clear_text_boxes():
            name_var.set("")
            photo_name_var.set("")
            tags_var.set("")
            ingredients_var.delete("1.0", "end")
            description_var.delete("1.0", "end")
            self.edit_menu.destroy()

        ## submit_recipe()
        ##
        ## Summary of the submit helper (edit dialog):
        ##
        ## Reads the edited fields, updates the Recipe object via
        ## recipe_manager.update_recipe, saves changes and refreshes
        ## the main UI.
        ##
        ## Parameters : none
        ##
        ## Return Value : none
        ##
        ## Description:
        ##
        ## Gathers values from widgets, calls update_recipe, saves the
        ## file and updates displayed widgets and tag lists.

        def submit_recipe():
            name = name_var.get()
            photo_name = photo_name_var.get()
            tags = tags_var.get().split()
            ingredients = pair_ingredients()
            description = description_var.get("1.0", "end-1c")
            self.recipe_manager.update_recipe(recipe_object, name, photo_name, tags, ingredients, description)
            self.recipe_manager.save_recipes()
            self.box["values"] = [item.name for item in self.recipe_manager.recipe_list]
            self.clear_display()
            clear_text_boxes()
            self.toggle_tags()
            self.update_tag_list()
            self.update_window()

        bottom_frame = Frame(self.edit_menu, bg="lightgrey")
        bottom_frame.pack(padx=10, pady=5)
        ttk.Button(bottom_frame, text="Finish Editing", command=submit_recipe).grid(row=0, column=0)
        self.edit_menu.protocol("WM_DELETE_WINDOW", self.edit_menu.destroy)

    ## clear_display(self)
    ##
    ## Summary of the clear display function:
    ##
    ## Removes child widgets from display frames so content can be
    ## redrawn cleanly.
    ##
    ## Parameters : none
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Iterates a small set of frames used for recipe details and destroys
    ## any existing widgets to avoid duplication when updating views.

    def clear_display(self):
        for frame in [self.lower_frame, self.upper_frame, self.description_label_frame, self.description_frame, self.top_right_frame, self.tags_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

    ## delete_recipe(self)
    ##
    ## Summary of the delete function:
    ##
    ## Removes the currently selected recipe (if any), updates storage
    ## and refreshes the UI.
    ##
    ## Parameters : none
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Reads self.chosen_recipe, calls recipe_manager.delete_recipe,
    ## saves changes and refreshes lists and displays.

    def delete_recipe(self):
        user_choice = self.chosen_recipe.get()
        if not user_choice:
            return
        self.recipe_manager.delete_recipe(user_choice)
        self.recipe_manager.save_recipes()
        self.box["values"] = [item.name for item in self.recipe_manager.recipe_list]
        self.chosen_recipe.set("")
        self.box.set("")
        self.clear_display()
        self.toggle_tags()
        self.update_window()

    ## toggle_tags(self, event=None)
    ##
    ## Summary of the tag toggle builder:
    ##
    ## Rebuilds the tag selection UI allowing users to toggle tag filters.
    ##
    ## Parameters : event - optional Tkinter event (Can be ignored because it is never used)
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Clears the tag container, builds a scrollable listbox of tags and
    ## attaches BooleanVars for tracking tag state changes which trigger
    ## update_tag_list.

    def toggle_tags(self, event=None):
        self.tag_state = {}

        for widget in self.below_add_button_frame.winfo_children():
            widget.destroy()

        container = Frame(self.below_add_button_frame, bg="lightgrey")
        container.pack(fill="both", expand=True)
        container.pack_propagate(False)

        toggler_label = tk.Label(container, text="Sort by Tags", bg="lightgrey")
        toggler_label.pack(side="top", fill="x", expand=False)

        def toggle():
            try:
                tag_options_list.curselection()[0]
                selection = tag_options_list.curselection()[0]
                tag = tag_options_list.get(selection)
                state = not self.tag_state[tag].get()
                self.tag_state[tag].set(state)
                color = "lightgreen" if state else "white"
                tag_options_list.itemconfigure(selection, bg=color)
            except:
                return


        toggle_tags_button = tk.Button(container, text="toggle tag", bg="lightgrey", command=toggle)
        toggle_tags_button.pack(side="bottom", fill="x", expand=False)
    
        scroller = tk.Scrollbar(container)
        scroller.pack(side="right", fill="y", expand=False)
        tag_options_list = tk.Listbox(container, yscrollcommand=scroller.set)
        tag_options_list.pack(fill="y", expand=True)
        scroller.config(command=tag_options_list.yview)

        for index, tag in enumerate(self.recipe_manager.all_tags):
            tag_options_list.insert(index, tag)
            var = tk.BooleanVar(value=False)
            var.trace_add("write", self.update_tag_list)
            self.tag_state[tag] = var

    ## update_tag_list(self, *args)
    ##
    ## Summary of the tag filtering function:
    ##
    ## Computes which recipes match the currently enabled tags and updates
    ## the sorted list display.
    ##
    ## Parameters : *args - optional arguments from trace callbacks
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Builds a newline-separated string of matching recipe names and calls
    ## show_tag_list to display it.

    def update_tag_list(self, *args):
        temp_tag_string = [tag for tag in self.tag_state if self.tag_state[tag].get()]
        self.hold_true_tags = "\n".join([f"  {r.name}" for r in self.recipe_manager.recipe_list if all(tag in r.tags for tag in temp_tag_string)])
        self.show_tag_list()

    ## show_tag_list(self)
    ##
    ## Summary of the tag-list display function:
    ##
    ## Renders the previously computed list of matching recipe names in a
    ## read-only Text widget with a scrollbar.
    ##
    ## Parameters : none
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Clears the browser area, builds a container with a scrollable Text
    ## widget and inserts self.hold_true_tags then disables editing.

    def show_tag_list(self):
        for widget in self.below_browser_frame.winfo_children():
            widget.destroy()
        
        container = tk.Frame(self.below_browser_frame, bg="lightgrey")
        container.pack(side="top", fill="both", expand=True)
        container.pack_propagate(False)

        sorting_label = tk.Label(container, text="Sorted Recipes", bg="lightgrey")
        sorting_label.pack(side="top", fill="x")
        scrolltool = tk.Scrollbar(container)
        scrolltool.pack(side="right", fill="y")

        show_selection = tk.Text(container, wrap="word", yscrollcommand=scrolltool.set)
        show_selection.pack(side="left", fill="both", expand=True)
        scrolltool.config(command=show_selection.yview)

        show_selection.insert("1.0", self.hold_true_tags)
        show_selection.config(state="disabled", bg="lightgrey", highlightthickness=0, bd=0, cursor="arrow")

    ## show_tags(self, event=None)
    ##
    ## Summary of the tags display function:
    ##
    ## Shows the tag list for the selected recipe in the tags panel.
    ##
    ## Parameters : event - optional Tkinter event (Can be ignored because it is never used)
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## If a recipe is selected, builds a scrollable Text widget listing the
    ## recipe's tags and disables editing for presentation.

    def show_tags(self, event=None):
        user_choice = self.chosen_recipe.get()
        if not user_choice:
            return
        for widget in self.tags_frame.winfo_children():
            widget.destroy()

        for item in self.recipe_manager.recipe_list:
            if item.name == user_choice:
                container = Frame(self.tags_frame, bg="lightgrey")
                container.pack(fill="both", expand=True)
                container.pack_propagate(False)

                tk.Label(container, text="Recipes Tags", bg="lightgrey").pack(side="top", fill="x", pady=10)
                scroller = tk.Scrollbar(container)
                scroller.pack(side="right", fill="y", expand=False)
                tags_text = tk.Text(container, wrap="word", yscrollcommand=scroller.set, height=13, width=18)
                tags_text.pack(side="left", expand=True)
                scroller.config(command=tags_text.yview)

                tags_text.insert("1.0", "\n".join(f"  {tag}" for tag in item.tags))
                tags_text.config(state="disabled", bg="lightgrey", highlightthickness=0, bd=0, cursor="arrow")

    ## show_recipe(self, event=None)
    ##
    ## Summary of the ingredient display function:
    ##
    ## Displays the ingredients and amounts for the selected recipe in a
    ## scrollable, read-only Text widget.
    ##
    ## Parameters : event - optional Tkinter event (Can be ignored because it is never used)
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Clears the upper and lower frames and inserts the formatted
    ## ingredient list for the currently selected recipe.

    def show_recipe(self, event=None):
        user_choice = self.chosen_recipe.get()

        for widget in self.lower_frame.winfo_children():
            widget.destroy()
        for widget in self.upper_frame.winfo_children():
            widget.destroy()

        ingredients_label = tk.Label(self.upper_frame, text="Ingredients list:", bg="lightgrey")
        ingredients_label.pack(side="bottom", fill="x", expand=False, pady=10)

        for item in self.recipe_list:
            if item.name == user_choice:
                ingredients_list = item.ingredients
                ingredients_text = ""
                for item in ingredients_list:
                    ingredient, amount = item
                    ingredients_text += f"  {ingredient}:\t\t\t\t{amount}\n"

                container = tk.Frame(self.lower_frame, bg="lightgrey")
                container.pack(fill="both", expand=True)

                scroll = tk.Scrollbar(container)
                scroll.pack(side="right", fill="y")
                ing_text = tk.Text(container, wrap="word", yscrollcommand=scroll.set)
                ing_text.pack(side="left", fill="both", expand=True)
                scroll.config(command=ing_text.yview)

                ing_text.insert("1.0", ingredients_text)
                ing_text.config(state="disabled", bg="lightgrey", highlightthickness=0, bd=0, cursor="arrow")

    ## show_description(self)
    ##
    ## Summary of the description display function:
    ##
    ## Shows the recipe description text for the selected recipe.
    ##
    ## Parameters : none
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Clears description frames and creates a wrapped Label with the
    ## recipe's description for display.

    def show_description(self):
        user_choice = self.chosen_recipe.get()

        for frame in [self.description_label_frame, self.description_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

        rec_desc_label = tk.Label(self.description_label_frame, text="Recipe Description:", bg="lightgrey")
        rec_desc_label.pack(side="top", fill="x", pady=10)

        for item in self.recipe_manager.recipe_list:
            if item.name == user_choice:
                rec_desc_text = tk.Label(self.description_frame, text=item.description, bg="lightgrey", wraplength=470, justify="left")
                rec_desc_text.pack(anchor="nw", fill="y", padx=20)

    ## show_photo(self)
    ##
    ## Summary of the photo display function:
    ##
    ## Loads and shows the image for the selected recipe using PIL.
    ##
    ## Parameters : none
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Attempts to open photo_name (adds .png if missing), resizes the
    ## image while preserving aspect ratio to fit the UI and attaches the
    ## PhotoImage object to the label to prevent garbage collection.

    def show_photo(self):
        user_choice = self.chosen_recipe.get()

        for widget in self.top_right_frame.winfo_children():
            widget.destroy()

        for item in self.recipe_manager.recipe_list:
            if item.name == user_choice:
                if ".png" not in item.photo_name:
                    item.photo_name += ".png"
                try:
                    image = Image.open(item.photo_name)
                except (FileNotFoundError, OSError):
                    no_photo = tk.Label(self.top_right_frame, text="A photo with that name could not be found", bg="lightgrey")
                    no_photo.pack(anchor="n", fill="both", expand=True)
                    return
                self.top_right_frame.update_idletasks()
                width, height = image.size
                scale = min((TOTAL_WINDOW_WIDTH//2)/width, (TOTAL_WINDOW_HEIGHT//2)/height)
                resized_image = image.resize((int(width*scale), int(height*scale)))
                photo = ImageTk.PhotoImage(resized_image)
                lbl = tk.Label(self.top_right_frame, image=photo, bg="lightgrey")
                lbl.photo = photo
                lbl.pack(anchor="n", fill="both", expand=True)