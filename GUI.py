from tkinter import *
import password_manager as pm

# MAIN GUI WINDOW ->
window = Tk() # Creates a new GUI window with 50 px padding on either sides and black background
window.config(bg= "black", padx= 50, pady= 50)

# Sets the window size to 600x600 px squared
window.config(height= 600, width= 600)         

window.eval("tk::PlaceWindow . center") # Ensures that the window pops up at the center of the screen when started
window.title("PASSWORDS MANAGER")       # Sets the title to "PASSWORDS MANAGER"
window.resizable(False, False)          # Makes the window non-resizable

# ------ Labels and Entry Fields ------

# WEBSITE NAME LABEL AND INPUT FIELD --> Used to differentiate the passwords from different websites/applications

website_label = Label(text= "Website/Application name: ", font= ("Times New Roman", 24, "normal"), bg= "black")
website_label.config(justify= "right")
website_label.grid(row= 0, column= 0, pady= 10, padx= 20)

website_input = Entry(bg= "black", fg= "white", font= ("Times New Roman", 24, "normal"), width= 30)
website_input.grid(row= 0, column= 1, pady= 10, columnspan= 2)

# USERNAME LABEL AND INPUT FIELD --> Used to differentiate passwords from the same websites but different accounts

username_label = Label(text= "Enter Username: ", font= ("Times New Roman", 24, "normal"), bg= "black")
username_label.grid(row= 1, column= 0, pady= 10, padx= 20)

username_input = Entry(bg= "black", fg= "white", font= ("Times New Roman", 24, "normal"), width= 30)
username_input.grid(row= 1, column= 1, pady= 10, columnspan= 2)

# PASSWORD LABEL AND INPUT FIELD --> Used to generate and/or input the password from the user

password_label = Label(text= "Enter Password: ", font= ("Times New Roman", 24, "normal"), bg= "black")
password_label.grid(row= 2, column= 0, pady= 10, padx= 20)

password_input = Entry(bg= "black", fg= "white", font= ("Times New Roman", 24, "normal"), width= 30)
password_input.grid(row= 2, column= 1, pady= 10, columnspan= 2)

# ----- Buttons -----

# SEARCH BUTTON --> If website and username are given, can be used to search up and save the password to clipboard

search_button = Button(bg= "white", fg= "black", font= ("Times New Roman", 18, "normal"), text= "SEARCH")
search_button.grid(row= 3, column= 0, pady= 10, padx= 10)

# GENERATE BUTTON --> If website and username are given, generates and copies a password to clipboard

generate_button = Button(bg= "white", fg= "black", font= ("Times New Roman", 18, "normal"), text= "GENERATE")
generate_button.grid(row= 3, column= 1, pady= 10, padx= 10)

# SAVE BUTTON --> If all three fields are provided/generated, saves the password to the database and encrypts it 

save_button = Button(bg= "white", fg= "black", font= ("Times New Roman", 18, "normal"), text= "SAVE")
save_button.grid(row= 3, column=2, pady= 10, padx= 10)

# ----- BUTTON FUNCTIONS -----

def save_password():
    """ Command for the save button. Saves the given fields to the database. """
    
    # Saving the Entry field inputs for data manipulation
    website  = website_input.get()
    username = username_input.get()
    password = password_input.get()
    
    if not website == '' and not username == '' and not password == '' and (website + username).lower() in pm.database_dict["unique_key"]:
        # Triggered if all inputs are entered and the website and username already exists in the database.
        # prompts the user if they want to change the password 
        
        # Change password prompt window ->
        change_password_prompt_window = Tk()                                    # Window created
        change_password_prompt_window.title("Confirmation Prompt")              # Window title
        change_password_prompt_window.config(padx= 50, pady= 50, bg= "black")   # padding (50 px each) and background
        change_password_prompt_window.resizable(False, False)                   # Sets resizability to False
        change_password_prompt_window.eval("tk::PlaceWindow . center")          # Window pops up at the center
        
        # Change password prompt label ->
        change_password_prompt_label = Label(
            master= change_password_prompt_window, 
            text= f"This website and username already exists.\nWould you like to change the password to {password}?",
            font= ("Times New Roman", 24, "normal"),
            bg= "black"
        )
        change_password_prompt_label.config(pady= 20)                           # Sets padding at y equal to 20 px
        change_password_prompt_label.grid(row= 0, column= 0, columnspan= 2)
        
        # Destroy password prompt window function ->
        def destroy_password_prompt_window():
            """Destroys the Change Password Prompt Window when called"""
            change_password_prompt_window.destroy()
        
        # "Yes" button pushed function ->
        def yes_button_pushed():
            """Activates when YES button is pushed. Changes the password in the database."""
            unique_key_index = pm.database_dict["unique_key"].index((website + username).lower())
            pm.database_dict["password"][unique_key_index] = password_input.get()
            pm.refresh()
            
            # Destroys the "no longer needed" windows
            change_password_prompt_window.after(250, destroy_password_prompt_window)
            
        # "No" button pushed ->
        def no_button_pushed():
            """Activates when NO button is pushed."""
            
            # Destroys the "no longer needed" windows
            change_password_prompt_window.after(250, destroy_password_prompt_window)
        
        # YES (Confirm password change) button ->
        yes_button = Button(
            master= change_password_prompt_window,
            text= "YES",
            font= ("Times New Roman", 24, "normal"),
            bg= "white", 
            fg= "black",
            command= yes_button_pushed
        )
        yes_button.grid(row= 1, column= 1)
        
        # NO (Deny password change) button ->
        no_button = Button(
            master= change_password_prompt_window,
            text= "NO",
            font= ("Times New Roman", 24, "normal"),
            bg= "white",
            fg= "black",
            command= no_button_pushed
        )
        no_button.grid(row= 1, column= 0)
        
        pm.refresh()
         
    elif not website == '' and not username == '' and not password == '':
        # Triggered when none of the fields are empty and the entry is completely new in the database.
        
        confirm_prompt_window = Tk()
        confirm_prompt_window.title("Confirmation Prompt")
        confirm_prompt_window.config(padx= 50, pady= 50, bg= "black")
        confirm_prompt_window.resizable(False, False)
        confirm_prompt_window.eval("tk::PlaceWindow . center")
        
        prompt_text = "Do you want to proceed with saving the following data?\n\n"
        prompt_website = f"Website/Application: {website}\n"
        prompt_username = f"Username: {username}\n"
        prompt_password = f"Password: {password}"
        
        confirm_prompt_label = Label(master= confirm_prompt_window, 
            text= prompt_text + prompt_website + prompt_username + prompt_password,
            font= ("Times New Roman", 24, "normal"),
            bg= "black"
        )
        confirm_prompt_label.config(pady= 20)
        confirm_prompt_label.grid(row= 0, column= 0, columnspan= 2)
        
        def confirmed():
            nonlocal confirm_prompt_window
            
            website  = website_input.get().lower()
            username = username_input.get().lower()
            password = password_input.get()
            unique_key = website + username
            
            pm.database_dict["unique_key"].append(unique_key)
            pm.database_dict["password"].append(password)
            
            website_input.delete(0, END)
            username_input.delete(0, END)
            password_input.delete(0, END)
            
            def destroy_deny_windows():
                confirm_prompt_window.destroy()
            
            confirm_prompt_window.after(100, destroy_deny_windows)
            
            pm.refresh()
                
        def deny():
            nonlocal confirm_prompt_window
                
            website_input.delete(0, END)
            username_input.delete(0, END)
            password_input.delete(0, END)
            
            def destroy_deny_windows():
                # deny_window.destroy()
                confirm_prompt_window.destroy()
            
            confirm_prompt_window.after(100, destroy_deny_windows)
            
        confirm_button = Button(master= confirm_prompt_window, bg= "white", fg= "black", text= "CONFIRM")
        confirm_button.config(command= confirmed, font= ("Times New Roman", 24))
        confirm_button.grid(row= 1, column= 1)
        
        deny_button = Button(master= confirm_prompt_window, bg= "white", fg= "black", text= "DENY")
        deny_button.config(command= deny, font= ("Times New Roman", 24))
        deny_button.grid(row= 1, column= 0)
        
    else: 
        error_window = Tk()
        error_window.eval("tk::PlaceWindow . center")
        error_window.resizable(False, False)
        error_window.title("Oh no! An error occured.")
        error_window.config(height= 200, width= 200, bg= "black", padx= 50, pady= 50)
        
        error_label = Label(
            master= error_window, 
            text= "An error occured.\nPlease check all the fields again.",
            font= ("Times New Roman", 24, "normal"),
            bg= "black"
            )
        
        error_label.pack()
    
    pm.refresh()
    
def search_password():
    """ Command for the search button. Searches the password from the database for given fields. """
    
    website  = website_input.get().lower()
    username = username_input.get().lower()
    
    unique_key = website + username
    
    try:
        key_index = pm.database_dict["unique_key"].index(unique_key)
        password  = pm.database_dict["password"][key_index]
        
        password_input.delete(0, END)
        password_input.insert(END, password)
        
    except ValueError:
        error_window = Tk()
        error_window.eval("tk::PlaceWindow . center")
        error_window.resizable(False, False)
        error_window.title("Oh no! An error occured.")
        error_window.config(height= 200, width= 200, bg= "black", padx= 50, pady= 50)
        
        error_label = Label(
            master= error_window, 
            text= "An error occured.\nPlease check the website and username again.",
            font= ("Times New Roman", 24, "normal"),
            bg= "black"
            )
        
        def terminate_error_window():
            nonlocal error_window
            
            error_window.destroy()
        
        error_window.after(1500, terminate_error_window)
        
        error_label.pack()
        
def generate_password():
    generated_password = pm.generate_password()
    
    password_input.delete(0, END)
    password_input.insert(END, generated_password)  
    
# ----- COMMAND CONFIGS -----
        
search_button.config(command= search_password)
save_button.config(command= save_password)
generate_button.config(command= generate_password)

window.mainloop()

# © Tanay Jaiman - Jul 2 2022 