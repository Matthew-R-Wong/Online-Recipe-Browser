##-----------------------------------------------------------------------
## File : recipe_manager.py
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

from recipe import Recipe

## class recipe_manager
##
## Description:
##
##   This class centralizes recipe storage and persistence. It keeps an
##   in-memory list of Recipe objects, maintains a master tag index,
##   and provides helpers for adding, removing, updating, and loading
##   recipes from disk.
##
## Data members:
##
##   recipe_list : In-memory list of recipes.
##   all_tags : Master list of tags currently in use.
##
## Methods:
##
##   __init__ - prepare empty containers for recipes and tags.
##   add_recipe - append a Recipe and register its tags.
##   delete_recipe - remove a Recipe by name and remove tags.
##   update_recipe - update a Recipe instance and refresh tags.
##   add_subtract_tags - add or remove tags from the master list.
##   update_tags - make tag changes after a recipe edit.
##   load_recipes - read recipes from the plain-text file format.
##   save_recipes - write recipes back to disk in the same format.

class recipe_manager:

    ## __init__(self)
    ##
    ## Summary of the constructor function:
    ##
    ## Initializes the manager and sets up empty containers for recipes
    ## and tags.
    ##
    ## Parameters : none
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Prepares recipe_list and all_tags for use by other methods.

    def __init__(self):
        self.recipe_list = []
        self.all_tags = []

    ## add_recipe(self, recipe_object)
    ##
    ## Summary of the add recipe function:
    ##
    ## Adds a Recipe object to the internal list and updates the
    ## master tag index to include any new tags from the recipe.
    ##
    ## Parameters : recipe_object - the recipe to add
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Appends to recipe_list and calls add_subtract_tags to register
    ## any tags that are not already tracked.

    def add_recipe(self, recipe_object):
        self.recipe_list.append(recipe_object)
        self.add_subtract_tags(" ".join(recipe_object.tags), 1)

    ## delete_recipe(self, recipe_name)
    ##
    ## Summary of the delete recipe function:
    ##
    ## Finds a recipe by name, removes it from the list, and removes any
    ## tags that are no longer used by any recipe.
    ##
    ## Parameters : recipe_name - name of the recipe to delete
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Iterates recipe_list to find the first match, deletes it, then
    ## calls add_subtract_tags with check=0 to remove unused tags.

    def delete_recipe(self, recipe_name):
        for index, entry in enumerate(self.recipe_list):
            if entry.name == recipe_name:
                del self.recipe_list[index]
                self.add_subtract_tags(" ".join(entry.tags), 0)
                break

    ## update_recipe(self, recipe_object, name, photo_name, tags, ingredients, description)
    ##
    ## Summary of the update function:
    ##
    ## Applies new values to an existing Recipe instance and updates the
    ## global tag index to reflect any changes.
    ##
    ## Parameters :
    ##    recipe_object - the recipe instance to update
    ##    name - new name
    ##    photo_name - new photo file name
    ##    tags - new tag list
    ##    ingredients - new ingredients
    ##    description - new description/directions
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Saves the old tags, updates the Recipe via set_values, then calls
    ## update_tags to add new tags and remove unused ones.

    def update_recipe(self, recipe_object, name, photo_name, tags, ingredients, description):
        old_tags = recipe_object.tags.copy()
        recipe_object.set_values(name, photo_name, tags, ingredients, description)
        self.update_tags(old_tags, tags)

    ## add_subtract_tags(self, tags_string, check)
    ##
    ## Summary of the tag maintenance function:
    ##
    ## Adds tags to the master list or removes them if they are no
    ## longer used by any recipe.
    ##
    ## Parameters :
    ##    tags_string - space-separated tag names
    ##    check - 1 to add, 0 to remove unused tags
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Splits the incoming string and either appends new tags to
    ## all_tags or removes tags that are not present in any recipe.

    def add_subtract_tags(self, tags_string, check):
        tag_list = tags_string.split()
        if check == 1:
            for tag in tag_list:
                clean_tag = tag.strip()
                if clean_tag not in self.all_tags:
                    self.all_tags.append(clean_tag)
        elif check == 0:
            for tag in tag_list:
                clean_tag = tag.strip()
                still_used = any(clean_tag in entry.tags for entry in self.recipe_list)
                if not still_used and clean_tag in self.all_tags:
                    self.all_tags.remove(clean_tag)

    ## update_tags(self, old_tags, new_tags)
    ##
    ## Summary of the update tags function:
    ##
    ## Adds any newly introduced tags and removes tags that are no
    ## longer present in any recipe.
    ##
    ## Parameters :
    ##    old_tags - previous tag list for the recipe
    ##    new_tags - updated tag list for the recipe
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Ensures all_tags contains the union of tags currently used by
    ## recipes and removes tags that have become unused.

    def update_tags(self, old_tags, new_tags):
        for tag in new_tags:
            if tag not in self.all_tags:
                self.all_tags.append(tag)
        for tag in old_tags:
            still_used = any(tag in entry.tags for entry in self.recipe_list)
            if not still_used and tag in self.all_tags:
                self.all_tags.remove(tag)

    ## load_recipes(self, filename="recipes.txt")
    ##
    ## Summary of the load function:
    ##
    ## Reads recipes from a text file using the project's plain-text
    ## format and populates the internal recipe list and tag index.
    ##
    ## Parameters : filename - path to the recipes file "recipes.txt"
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## The expected file format is five blocks per recipe separated by
    ## blank lines: name, photo_name, tags (space separated), ingredients
    ## block (one per line) and description. Missing file is handled
    ## silently.

    def load_recipes(self, filename="recipes.txt"):
        try:
            with open(filename, "r") as file:
                content = file.read()
        except FileNotFoundError:
            return

        blocks = content.strip().split("\n\n")
        recipe_blocks = []

        for index in range(0, len(blocks), 5):
            object = blocks[index : index + 5]
            if len(object) == 5:
                recipe_blocks.append(object)
        
        for block in recipe_blocks:
            name, photo_name, tags_line, ingredients_block, description = block

            name = name.strip()
            photo_name = photo_name.strip()
            description = description.strip()

            if tags_line.strip():
                tags = tags_line.split()
            else:
                tags = []
            
            ingredients = []
            for line in ingredients_block.splitlines():
                line = line.strip()
                if not line:
                    continue
                if "," in line:
                    ingredient, amount = line.split(",", 1)
                    ingredients.append((ingredient.strip(), amount.strip()))
                else:
                    ingredients.append((line, ""))
            
            self.add_recipe(Recipe(name, photo_name, tags, ingredients, description))


    ## save_recipes(self, filename="recipes.txt")
    ##
    ## Summary of the save function:
    ##
    ## Persists all recipes to a plain-text file in the project's
    ## readable format, overwriting existing contents.
    ##
    ## Parameters : filename - path to write to "recipes.txt"
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Iterates recipe_list writing name, photo, tags, ingredients and
    ## description blocks separated by blank lines so the file can be
    ## reloaded by load_recipes.

    def save_recipes(self, filename="recipes.txt"):
        with open(filename, "w") as file:
            for entry in self.recipe_list:
                file.write(f"{entry.name}\n\n")
                file.write(f"{entry.photo_name}\n\n")
                file.write(f"{' '.join(entry.tags)}\n\n")
                for ingredient, amount in entry.ingredients:
                    if amount:
                        file.write(f"{ingredient}, {amount}\n")
                    else:
                        file.write(f"{ingredient}\n")
                file.write("\n")
                if entry.description.strip():
                    file.write(f"{entry.description}\n\n")
                else:
                    file.write("\n")