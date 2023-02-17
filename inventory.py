from tabulate import tabulate


class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
        '''
        In this function, you must initialise the following attributes:
            ● country,
            ● code,
            ● product,
            ● cost, and
            ● quantity.
        '''

    def get_cost(self):
        return int(self.cost)

    def get_quantity(self):
        return int(self.quantity)

    def __str__(self):
        return f"County: {self.country}\n" \
               f"Code: {self.code}\n" \
               f"Product: {self.product}\n" \
               f"Cost: {self.cost}\n" \
               f"Quantity: {self.quantity}\n"


# =============Shoe list===========
shoe_list = []
# Temp_list is used to store each  line of the inventory file as a separate item in the list.
# This is then used by multiple functions.
temp_list = []


# ==========Functions outside the class==============
#  This function is used to prompt user for a file selection.
#  It checks if the file exists and display's error message if not.
def user_file_sel():
    while True:
        user_sel = input("Please input the filename: ") + ".txt"
        try:
            inv_file = open(user_sel, "r")
            return user_sel
        except FileNotFoundError:
            print(f"There is no file with name '{user_sel}'")


#  This function takes the temp_list (list_obj) declared as well as the selected shoe_file.
#  It skips the first line of text file where the headers are.
#  It then reads each line of text and formats before adding as a nested list inside temp_list.
#  It then returns appended temp_list.
def read_shoes_data(list_obj, shoe_file):  # Will add lines to a temporary list(list_obj).
    ref_file = open(shoe_file, 'r+')
    while True:
        try:
            next(ref_file)
            for line in ref_file:
                list_obj.append(line.split(","))
            for count1, item in enumerate(list_obj):
                for count2, attr in enumerate(item):
                    list_obj[count1][count2] = (list_obj[count1][count2].strip("\n"))
            ref_file.close()
            return list_obj
        except FileNotFoundError:
            print(f"There is no file with name '{shoe_file}'")


#  This function reads the first line of the text file and returns each string value separated by ','.
#  These are added to the headers_list.
def get_headers(shoe_file):
    temp_file = open(shoe_file, "r")
    headers = temp_file.readline()
    headers = headers[:-1]
    headers_list = headers.split(",")
    return headers_list


#  new_shoe_list = capture_shoes(header_list, user_input_list, temp_list)
#  This function allows user to capture info on new shoe using input prompts.
#  The entries will  be added to the new_shoe_temp_list.
#  This list will be returned for adding to use within the add_shoe_obj function.
#  The next function will do the 2nd part of the requirement and create a shoe object and append to shoe_list.
def capture_shoes(headers_list_func, list_obj, temp_list_func):
    new_shoe_temp_list = []
    for item in headers_list_func:
        if item == "Country":
            temp_var = input(f"Please input the {item}: ")
            new_shoe_temp_list.append(temp_var)
        elif item == "Code":
            temp_var = (input(f"Please input the {item}: ")).upper()
            for info in temp_list_func:
                if temp_var in info:
                    print(f"{item} in use: {temp_var}")
                    temp_var = (input(f"Please input the {item}: ")).upper()
            new_shoe_temp_list.append(temp_var)
        elif item == "Product":
            temp_var = input(f"Please input the {item}: ")
            for info in temp_list_func:
                if temp_var in info:
                    print(f"{item} in use: {temp_var}")
                    temp_var = (input(f"Please input the {item}: ")).upper()
            new_shoe_temp_list.append(temp_var)
        elif item == "Cost":
            while True:
                try:
                    temp_var = int(input(f"Please input the {item}: "))
                    new_shoe_temp_list.append(temp_var)
                    break
                except ValueError:
                    print("Not a number")
        elif item == "Quantity":
            while True:
                try:
                    temp_var = int(input(f"Please input the {item}: "))
                    new_shoe_temp_list.append(temp_var)
                    break
                except ValueError:
                    print("Not a number")
        list_obj.append(temp_var)
    return new_shoe_temp_list


#  This function takes in  the user input list, and shoe_list as arguments.
#  It is used to create a shoe object out of the shoe_nested list.
#  If a new shoe has been created it uses an if/else statement to check for a 2d list.
#  This allows the function to create either a single object from 1 new shoe entry.
#  Or create multiple objects from the whole shoe list.
#  The user_input_list_func input argument takes either the single new entry or multiple entry nested list as arg.

def add_shoe_obj(user_input_list_func, shoe_list_func):
    if type(user_input_list_func[0]) == list:  # This creates multiple shoe objects from the user_input_list_func
        for temp in user_input_list_func:
            if len(temp) == 5:
                shoe_list_func.append(Shoe(temp[0], temp[1], temp[2], temp[3], temp[4]))
    else:
        if len(user_input_list_func) == 5:  # This creates an object from a single shoe in the user_input_list_func
            shoe_list_func.append(Shoe(user_input_list_func[0], user_input_list_func[1],
                                       user_input_list[2], user_input_list_func[3],
                                       user_input_list_func[4]))


#  view_all(temp_list, shoe_list, header_list)
#  This function is used to display all shoes.
#  It takes both the list_obj(temp_list) containing all shoes as a list.
#  And the shoe_list, which contains all shoes each as an object.
#  It first tries to tabulate a list from the list_obj(temp list).
#  If the user does not have tabulate installed, except will display error.
#  It will then print the string method for each shoe object from the shoe_list using for loop.
def view_all(list_obj, shoe_list_obj, header_list_func):
    try:
        for num, item in enumerate(list_obj):
            if type(item) != list:
                list_obj[num] = list_obj[num].split(",")
        print(tabulate(list_obj, headers=header_list_func))
    except ImportError:
        print("You do not have the tabulate library installed")
        print("Printing out all shoe information using class method '__str__'")
        for item in shoe_list_obj:
            print(item)


#   This function will re-write the whole "inventory.txt" (or other user specified txt file).
def re_stock(shoe_list_obj, shoe_file, temp_list_func, header_list_func):
    #  lambda method used to sort shoe_list objects by "get_quantity" method.
    shoe_list_obj_sorted = sorted(shoe_list_obj, key=lambda i: int(i.get_quantity()), reverse=False)
    lowest_qty = shoe_list_obj_sorted[0]  # Index [0] assigns lowest_qty show object to "lowest_qty" variable.
    print(f"Lowest quantity shoe:\n\n{lowest_qty}")
    user_choice = input("Would you like to add to this quantity of shoe? ('y' or 'n')")
    while True:
        write_list = [",".join(header_list_func)]
        if user_choice == 'y':
            try:
                quantity_choice = int(
                    input(f"what is the quantity you would like to add to {lowest_qty.get_quantity()}:"))
            except ValueError:
                print("Not an integer, please try again")
            new_qty = int(quantity_choice) + int(lowest_qty.get_quantity())
            print(f"New quantity: {new_qty}")
            lowest_qty.quantity = new_qty  # Updates the lowest_qty value with user selected added quantity.
            for count, item1 in enumerate(shoe_list_obj):  # Updates shoe_list object with new quantity using for loop.
                if item1 == lowest_qty:  # Finds the shoe_list object by checking if "lowest_qty" == object.quantity
                    shoe_list_obj[count].quantity = new_qty  # Updates the shoe_list object.quantity value
                    temp_list_func[count][4] = str(new_qty)  # Updates the shoe_list value in parallel.
            for item2 in temp_list_func:  # For loop to format "temp_list_func"
                line_joint = ",".join(item2)  # Join method used to convert into string
                write_list.append("\n" + line_joint)  # String then appended to the "write_list"
            temp_file = open(shoe_file, "r+")
            for item3 in write_list:
                temp_file.write(item3)  # Iterating through each str in write list and writing to new line of txt file.
            temp_file.close()
            break
        elif user_choice == 'n':
            break
        else:
            user_choice = input("Invalid selection.\nWould you like to add to this quantity of shoe? ('y' or 'n')")
    return


#  This function allows the user to display information of specific shoe "code".
def search_shoe(shoe_list_obj):
    print("Shoe codes: ")
    temp_shoe_code_list = []
    for item in shoe_list_obj:
        print(item.code)
        temp_shoe_code_list.append(item.code)  # Adding each shoe code to a "temp_shoe_code_list".
    while True:
        user_sel_code = (input("Please select which inventory item to display using the shoe code:\n")).upper()
        if user_sel_code not in temp_shoe_code_list:  # Checks if the shoe code is not in "temp_shoe_code_list".
            print("Invalid selection")
        else:
            print(item)
            break


#  This function uses for loop to iterate through all shoe objects in shoe_list.
#  It then prints the value_per_item using the calculation item.get_cost() * item.get_quantity()
def value_per_item(shoe_list_obj):
    for item in shoe_list_obj:
        print(f"Total value per item type '{item.product}': £{item.get_cost() * item.get_quantity()}")


#  This function sorts the shoe_list objects by largest quantity using lambda function and "get_quantity" method.
#  It then prints the shoe object and that it's for sale.
def highest_qty(shoe_list_obj):
    shoe_list_obj_sorted = sorted(shoe_list_obj, key=lambda i: int(i.get_quantity()), reverse=True)
    hi_qty = shoe_list_obj_sorted[0]
    print("Highest qty item for sale:\n"
          f"{hi_qty}")


#   This function adds a new shoe string, creates a list and then appends the list to the user selected text file.
def inventory_shoe_add(inventory_add_list, user_sel1_func):
    write_new_shoe_list = inventory_add_list
    for inv_count, inv_item in enumerate(write_new_shoe_list):
        if type(inv_item) == int:
            write_new_shoe_list[inv_count] = str(inv_item)
    inventory_add_list = ",".join(write_new_shoe_list)
    inventory_file = open(user_sel1_func, 'a+')
    inventory_file.seek(2, 0)
    inventory_file.write(inventory_add_list + '\n')
    inventory_file.close()
    temp_list.append(inventory_add_list)


# ==========Main Menu=============

user_sel1 = user_file_sel()
temp_list = read_shoes_data(temp_list, user_sel1)
add_shoe_obj(temp_list, shoe_list)

while True:
    #  Options for user are displayed.
    choice_list = ["y", "n"]
    header_list = get_headers(user_sel1)
    user_sel2 = input("Please select from the following number options:\n"
                      "'1': view all\n"
                      "'2': re-stock\n"
                      "'3': search shoe\n"
                      "'4': total value per item\n"
                      "'5': highest quantity\n"
                      "'6': add shoe\n"
                      "'7': choose new file\n"
                      "'8': Close: ")
    if user_sel2 == '1':
        view_all(temp_list, shoe_list, header_list)
    elif user_sel2 == '2':
        re_stock(shoe_list, user_sel1, temp_list, header_list)
    elif user_sel2 == '3':
        search_shoe(shoe_list)
    elif user_sel2 == '4':
        value_per_item(shoe_list)
    elif user_sel2 == '5':
        highest_qty(shoe_list)
    elif user_sel2 == '6':
        add_shoe_cont = True
        while add_shoe_cont:  # While statement to continuously ask user to add new shoe or not.
            user_input_list = []
            new_shoe_list = capture_shoes(header_list, user_input_list, temp_list)
            inventory_shoe_add(new_shoe_list, user_sel1)  # Function to add new shoe strings from list to text file.
            add_shoe_obj(user_input_list, shoe_list)  # Add_shoe_obj is rerun to read all values from txt file inc. new.
            add_shoe_choice = input("Add another shoe? ('y' or 'n')").lower()
            if add_shoe_choice not in choice_list:
                print("Invalid selection")
                add_shoe_choice = input("Add another shoe? ('y' or 'n')").lower()
            elif add_shoe_choice == "n":
                break
            else:
                continue
    elif user_sel2 == '7':
        user_sel1 = user_file_sel()
    elif user_sel2 == '8':
        break
    else:
        print("Invalid selection, try again")
