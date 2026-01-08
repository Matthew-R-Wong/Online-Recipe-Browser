##-----------------------------------------------------------------------
## File : recipe.py
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

## class Recipe
##
## Description:
##
##   This class represents a single recipe record and provides simple
##   storage for the recipe's fields used by the UI and persistence
##   layers.
##
## Data members:
##
##   name (str): Recipe name used for display and identification.
##   photo_name (str): File name or path for an associated image.
##   tags (list[str]): Tags used for filtering and searching.
##   ingredients (list[tuple[str,str]]): (ingredient, amount) pairs.
##   description (str): Free-form directions or notes for the recipe.
##
## Methods:
##
##   __init__ - initialize a recipe instance with the provided fields.
##   set_values - update all fields of the recipe in-place.

class Recipe:

    ## __init__(self, name, photo_name, tags, ingredients, description)
    ##
    ## Summary of the constructor function:
    ##
    ## Initializes a new Recipe instance with the provided values.
    ##
    ## Parameters :
    ##    name - recipe name
    ##    photo_name - image file name or path
    ##    tags - list of tags
    ##    ingredients - (ingredient, amount) pairs
    ##    description - directions or notes
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Stores the provided values on the new object for use by the UI
    ## and persistence layers.

    def __init__(self, name, photo_name, tags, ingredients, description):
        self.name = name
        self.photo_name = photo_name
        self.tags = tags
        self.ingredients = ingredients
        self.description = description

    ## set_values(self, name, photo_name, tags, ingredients, description)
    ##
    ## Summary of the set values function:
    ##
    ## Updates all fields of the Recipe in-place.
    ##
    ## Parameters :
    ##    name - new name
    ##    photo_name - new image file name or path
    ##    tags - new tag list
    ##    ingredients - new (ingredient, amount) pairs
    ##    description - new directions or notes
    ##
    ## Return Value : none
    ##
    ## Description:
    ##
    ## Mutates the object so any external references to this Recipe
    ## observe the updated values immediately.
    
    def set_values(self, name, photo_name, tags, ingredients, description):
        self.name = name
        self.photo_name = photo_name
        self.tags = tags
        self.ingredients = ingredients
        self.description = description