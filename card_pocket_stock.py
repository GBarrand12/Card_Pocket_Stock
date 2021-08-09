# Card Pocket Stock Checker Program

# Copyright Georgia Barrand 2020
# The purpose of this program is to allow the user to update the stock
# amounts of their card pockets in order to keep track of the stock available
# It is designed with the stakeholder in mind being a
# Year 13 Business Studies group
# Completed outcome - Version 4

# Importing the tkinter and ttk modules
from tkinter import *
from tkinter import ttk
import os.path


# Pocket class
class Pocket:
    """The Pocket class stores the details for each pocket
     (colour and current stock available) and has methods to sell and
     restock the pockets and a method to retrieve exported data to create
      instances of the class"""

    def __init__(self, colour, current_stock_available):
        """
        This is the constructor method for the pocket class which
        initialises the instance variables.
        :param colour: The colour of each pocket
        :param current_stock_available: The amount of stock available
        for each pocket
        """

        # Initialise instance variables
        self.colour = colour
        self.current_stock_available = int(current_stock_available)
        # Adding each instance to the pockets list
        pockets.append(self)

    def restock(self, amount):
        """
        Method to increase the amount of a specific pocket's stock
        :param amount: The amount that the user entered that they
        want to restock the pocket by
        :return: Returns the updated current_stock_available for
        the selected pocket
        """
        self.current_stock_available += amount
        return self.current_stock_available

    def sell(self, amount):
        """
        Method to decrease the amount of a specific pocket's stock
        :param amount: The amount that the user entered that they
        want to sell of the pocket's stock
        :return: Returns the updated current_stock_available for
        the selected pocket
        """
        self.current_stock_available = self.current_stock_available - amount
        return self.current_stock_available

    def get_data():
        """
        Method to retrieve the data from the stock.txt file to create instances
        of the pocket class
        """
        # Opening the stock.txt file in read mode
        stock_file = open("stock.txt", "r")
        # Creating a list of each line in the stock.txt file
        line_list = stock_file.readlines()

        # Looping through each line
        for line in line_list:
            # Separating the colour and the current_stock_available fo each
            # pocket instance
            stock_data = line.strip().split(",")
            # Unpacking each value to create the Pocket object
            Pocket(*stock_data)

        # Closing the stock file
        stock_file.close()


# Stock class
class Stock:
    """The Stock class holds the GUI and has methods to populate
    the pocket_names list, output the overview, validate what is entered
    and selected, restock and sell the pockets, reset the input fields
    once a pocket has been successfully restocked or sold, and export
    the current data of each pocket"""

    def __init__(self, parent):
        """
        The constructor for the Stock class.

        Holds the GUI and all the widgets
        :param parent: root
        """

        # Create frame which contains the GUI
        wrapper_frame = LabelFrame(text="Stock Checker:")
        wrapper_frame.grid(row=0, column=0, padx=10, pady=10, sticky="NE")

        # Create overview frame which contains an overview of the stock
        # of each item that is available
        overview_frame = LabelFrame(wrapper_frame, text="Overview:")
        overview_frame.grid(row=1, column=0, padx=10, pady=10, sticky="EW")

        # Label to output the stock of each card pocket colour and the
        # total stock
        self.stock_overview = StringVar()

        # Create label to display the stock overview
        label_stock_overview = Label(overview_frame,
                                     textvariable=self.stock_overview)
        label_stock_overview.grid(row=0, column=0,
                                  columnspan=2, padx=10, pady=3, sticky="EW")

        # Create a PhotoImage to store the location of the image used
        pocket_picture = PhotoImage(file="card_pockets.png")

        # Create a new Label using the PhotoImage and add it to the GUI
        image_label = Label(overview_frame, image=pocket_picture)
        # Keep a reference to the image object (otherwise it stops showing up)
        image_label.image = pocket_picture
        image_label.grid(row=0, column=3, columnspan=2,
                         padx=10, pady=10, sticky="NE")

        # Create update stock frame which contains all the widgets
        # related to restocking or selling the stock
        update_stock_frame = LabelFrame(wrapper_frame, text="Update Stock:")
        update_stock_frame.grid(row=2, column=0, padx=10, pady=10, sticky="EW")

        # Create the colour frame to house the ComboBox to
        # select the colour of card pocket
        colour_frame = LabelFrame(update_stock_frame,
                                  text="Select Colour:", width=40)
        colour_frame.grid(row=0, column=0, padx=10, pady=10, sticky="EW")

        # Set up ComboBox to select the colour of the card pocket
        # Set up variable and option list for the colour ComboBox
        self.pocket_name = StringVar()
        # Set the variable to "Choose..." to force a user to
        # select something
        self.pocket_name.set("Choose...")

        # Create a ComboBox to select the colour
        self.colour_box = ttk.Combobox(colour_frame,
                                       textvariable=self.pocket_name,
                                       state="readonly")
        self.colour_box['values'] = pocket_names
        self.colour_box.grid(row=0, column=0, padx=10, pady=3, sticky="EW")

        # Set up variable for feedback on the colour selection
        self.colour_info = StringVar()
        self.colour_info.set("")

        # Create colour info label to display feedback
        colour_info_label = Label(colour_frame, textvariable=self.colour_info,
                                  width=40, fg="red")
        colour_info_label.grid(row=5, column=0, padx=10, pady=10)

        # Label to store the selected colour once set
        self.selected_colour = StringVar()

        # Create the frame to house the entry box
        pocket_entry_frame = LabelFrame(update_stock_frame,
                                        text="Enter Amount:", width=40)
        pocket_entry_frame.grid(row=0, column=1, padx=10, pady=10, sticky="EW")

        # Create entry to input the amount of stock to be restocked or sold
        # Variable to hold the amount of pockets
        self.number_of_pockets = StringVar()
        self.pocket_entry = ttk.Entry(pocket_entry_frame,
                                      textvariable=self.number_of_pockets)
        self.pocket_entry.grid(row=0, column=0, padx=10, pady=3, sticky="EW")

        # Set up variable for feedback on the amount selection
        self.amount_info = StringVar()
        self.amount_info.set("")

        # Create amount info label to display feedback
        amount_info_label = Label(pocket_entry_frame,
                                  textvariable=self.amount_info, width=40,
                                  fg="red")
        amount_info_label.grid(row=5, column=0, padx=10, pady=10)

        # Label to store the selected amount once set
        self.selected_amount = IntVar()

        # Create button to restock the selected colour by the entered amount
        self.button_restock = Button(update_stock_frame, text="Restock",
                                     width=20, bg="mediumseagreen", fg="white")
        self.button_restock['command'] = self.restock_pockets
        self.button_restock.grid(row=3, column=0, padx=10, pady=3)

        # Create button to sell the entered amount of the selected colour
        self.button_sell = Button(update_stock_frame, text="Sell",
                                  width=20, bg="firebrick1", fg="white")
        self.button_sell['command'] = self.sell_pockets
        self.button_sell.grid(row=3, column=1, padx=10, pady=3)

        # Set up variable for feedback on the success or failure of
        # the restock/sale
        self.feedback = StringVar()
        self.feedback.set("")

        # Create feedback label to display feedback
        self.feedback_label = Label(update_stock_frame,
                                    textvariable=self.feedback, fg="black")
        self.feedback_label.grid(row=4, column=0, padx=10, pady=10,
                                 columnspan=2)

        # Create button to export the current details in the overview
        self.button_export = Button(wrapper_frame, text="Export Data",
                                    width=20, bg="royalblue", fg="white")
        self.button_export['command'] = self.export_details
        self.button_export.grid(row=6, column=0, padx=10, pady=3)

        # Set up variable for feedback on whether
        # or not the data has been exported
        self.export_info = StringVar()
        self.export_info.set("")

        # Create export_info_label to display the export feedback
        export_info_label = Label(wrapper_frame, textvariable=self.export_info)
        export_info_label.grid(row=7, column=0, padx=10, pady=10)

        # Calling the output_overview method
        self.output_overview()

    def create_pocket_names():
        """
        Method to populate the pocket_names list
        """
        for pocket in pockets:
            pocket_names.append(pocket.colour)

    def output_overview(self):
        """
        Method which outputs the information for the overview
        in a formatted way
        """
        # Start the overview variable to store the overview as a string
        overview = ""
        total_stock_available = 0
        for pocket in pockets:
            # Adds each colour and its amount to the details string
            overview += str(pocket.colour) + ": " \
                        + str(pocket.current_stock_available) + "\n"
            # Updates the total stock available by adding the stock
            # of each colour
            total_stock_available += int(pocket.current_stock_available)

        # Adding the total stock available to the overview string
        overview += "\nTotal Stock Available: "
        overview += str(total_stock_available)

        # Set the stock overview to our details
        self.stock_overview.set(overview)

    def colour_checker(self):
        """
        Method to check that the user has selected a colour from
        the colour combobox
        """

        # Checking if the user has not selected anything
        # (so the value is still "Choose...")
        if self.pocket_name.get() == "Choose...":
            # Adding appropriate feedback to a string and setting
            # the colour_info variable to it
            colour_info_str = \
                "You must select a card pocket colour to restock or sell"
            self.colour_info.set(colour_info_str)
        # Runs if the user has selected something
        else:
            # Adding appropriate feedback to a string and setting
            # the colour_info variable to it
            colour_info_str = ""
            self.colour_info.set(colour_info_str)
            # Looping through each object in the pocket_names list
            for pocket in pockets:
                if self.pocket_name.get() == pocket.colour:
                    # Checking to see if it is the name selected in
                    # the combobox for the card pocket colours
                    # This is accessing information from the Pocket class
                    # (coupling)
                    self.selected_colour = pocket.colour

    def integer_checker(self, number_of_pockets):
        """
        Method to check that the user has entered a number greater
        than 0 in the pocket_entry
        :param number_of_pockets: The amount the user entered in
        the pocket_entry
        """

        # Runs if the entered amount is a number
        try:
            # Converting the number_of_pockets to an integer
            number_of_pockets = int(number_of_pockets)
            # Checking that the amount is greater than 0
            if number_of_pockets > 0:
                # Returning the valid number_of_pockets
                # variable for further use
                return number_of_pockets

            # Checking if the entered amount is 0 or less than 0
            else:
                # Adding appropriate feedback
                self.amount_info_str = \
                    "You must enter an amount greater than 0"
                return False

        # Runs if what was entered is not a number
        except ValueError:
            # Adding appropriate feedback
            self.amount_info_str = "Please enter a whole number"
            return False

    def restock_pockets(self):
        """
        Method to call the pocket.restock method once
        a valid number and colour have been received

        """
        # Calling the colour_checker method
        self.colour_checker()
        # Setting selected_colour to the selected colour from the combobox
        selected_colour = self.selected_colour
        # Setting number_of_pockets to the amount entered in the entry
        number_of_pockets = self.number_of_pockets.get()
        # Setting the selected_amount to what the integer checker method
        # returns with number_of_pockets passed in
        selected_amount = self.integer_checker(number_of_pockets)

        # Runs if an invalid input has been entered in the entry
        if not selected_amount:
            # Setting the amount_info variable to the amount_info_str
            # which will allow the feedback to be displayed in the
            # amount_info_label
            self.amount_info.set(self.amount_info_str)
        # Runs if a valid input has been entered into the entry
        else:
            # Adding appropriate feedback for the amount_info
            self.amount_info_str = ""
            self.amount_info.set(self.amount_info_str)
            # Looping through the pockets
            for pocket in pockets:
                # Finding the selected instance
                if pocket.colour == selected_colour:
                    # Setting the current_stock_available to what
                    # is returned from the pocket.restock method
                    # with selected amount passed in
                    current_stock_available = pocket.restock(selected_amount)
                    # Runs if the current_stock_available was returned as False
                    if not current_stock_available:
                        self.feedback.set("Your restock was unsuccessful")
                        self.feedback_label.config(fg="red")
                    # Runs if the restock was successful
                    else:
                        # Adding appropriate feedback
                        self.feedback.set(
                            "You have restocked {} of the {} card pockets.\n"
                            "There are now {} {} card pockets in stock".format
                            (selected_amount, selected_colour,
                             current_stock_available, selected_colour))
                        # Running methods to reset all the inputs and update
                        # the overview
                        self.reset_inputs()
                        self.output_overview()

    def sell_pockets(self):
        """
        Method to call the pocket.sell method once
        a valid number and colour have been received.

        It also checks that the amount entered is less than the
        current_stock_available of the selected pocket colour
        """
        # Calling the colour_checker method
        self.colour_checker()
        # Setting selected_colour to the selected colour from the combobox
        selected_colour = self.selected_colour
        # Setting number_of_pockets to the amount entered in the entry
        number_of_pockets = self.number_of_pockets.get()
        # Setting the selected_amount to what the integer checker method
        # returns with number_of_pockets passed in
        selected_amount = self.integer_checker(number_of_pockets)

        # Runs if an invalid input has been entered in the entry
        if not selected_amount:
            # Setting the amount_info variable to the amount_info_str
            # which will allow the feedback to be displayed in the
            # amount_info_label
            self.amount_info.set(self.amount_info_str)
        # Runs if a valid input has been entered into the entry
        else:
            # Adding appropriate feedback for the amount_info
            self.amount_info_str = ""
            self.amount_info.set(self.amount_info_str)
            # Looping through the pockets
            for pocket in pockets:
                # Finding the selected instance
                if pocket.colour == selected_colour:
                    # Checking if the selected_amount is greater than the
                    # pocket.current_stock_available
                    if pocket.current_stock_available < selected_amount:
                        # Setting appropriate feedback
                        self.feedback.set(
                            "There are not enough {} card pockets in stock to "
                            "complete the sale.\n"
                            " Please enter a smaller number"
                            .format(selected_colour))
                        self.feedback_label.config(fg="red")
                    else:
                        # Setting the current_stock_available to what is
                        # returned from the pocket.sell method
                        # with selected_amount passed through
                        current_stock_available = pocket.sell(selected_amount)
                        # Setting appropriate feedback
                        self.feedback.set(
                            "You have sold {} of the {} card pockets."
                            "\n There are now {} {} card pockets in stock"
                            .format(selected_amount, selected_colour,
                                    current_stock_available, selected_colour))
                        # Running methods to reset all the inputs and
                        # update the overview
                        self.reset_inputs()
                        self.output_overview()

    def reset_inputs(self):
        """
        Method to reset all the inputs/variables once a pocket
        has been successfully sold or restocked
        """

        # Reset the colour combobox and pocket_entry to the default values
        # once the user has restocked or sold something
        self.number_of_pockets.set("")
        self.pocket_name.set("Choose...")
        # Resetting the combobox and entry feedback variables
        self.amount_info.set("")
        self.colour_info.set("")
        self.selected_colour = "Choose..."

    def export_details(self):
        """
        Method to export the current stock of each item to a text file
        """

        # Setting up the export_string variable
        export_string = ""
        # Opening the stock_file to write
        stock_file = open("stock.txt", "w")
        # Append each pocket_name and current_stock_available for every pocket
        for pocket in pockets:
            current_stock_available = str(pocket.current_stock_available)
            export_string += pocket.colour + ","\
                + current_stock_available + "\n"

        # Writing the export_string to te stock_file
        stock_file.write(export_string)
        # Closing the stock_file
        stock_file.close()
        # Adding appropriate feedback
        self.export_info.set("Your stock data has been successfully exported")


# Main routine
if __name__ == "__main__":
    # Add a list for objects that is populated by instance variables
    pockets = []
    # This list stores just the colours of each card pocket
    pocket_names = []

    # Checking if the stock.txt file has already been created and
    # if so getting the data from it to create the pocket instances
    if os.path.exists("stock.txt"):
        # Create a set of instances for the various card pockets
        # and colours from the exported data
        Pocket.get_data()
    # Runs if the stock.txt file does not exist
    else:
        # Create a set of instances for the various card pockets and colours
        Pocket("Lime Green", 15)
        Pocket("Matte Black", 30)
        Pocket("Silver", 20)

    # Populate the pocket_names list
    Stock.create_pocket_names()

    # Running the GUI
    root = Tk()
    Stock(root)
    root.title("Stock Updating Program")
    root.mainloop()
