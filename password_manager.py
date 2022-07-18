import pandas as pd
from random import randint, choice

database        = pd.DataFrame(pd.read_csv("passwords.csv"))
unique_key_list = database['unique_key'].to_list() 
password_list   = database['password'].to_list()

database_dict   = {
    "unique_key" : unique_key_list,
    "password"   : password_list
}

def refresh():
    pd.DataFrame(database_dict).to_csv("passwords.csv")


def generate_password() -> str:
    special_chars = [
        '~', '!', '@', '#', '$', '%', '^', '&'
    ] 
    
    numbers_list = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
    ]
    
    letters_list = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ]
    
    all_chars_list = special_chars + numbers_list + letters_list
    
    output_string = ""
    password_length = randint(8, 28)
    
    min_numbers_list       = []
    min_uc_letters_list    = []
    min_lc_letters_list    = []
    min_special_chars_list = []
    
    for _ in range(int((password_length - password_length % 4)/4)):
        min_numbers_list.append(choice(numbers_list))
        min_uc_letters_list.append(choice(letters_list).upper())
        min_lc_letters_list.append(choice(letters_list).lower())
        min_special_chars_list.append(choice(special_chars))
        
    min_chars_list = min_special_chars_list + min_lc_letters_list + min_numbers_list + min_uc_letters_list
    
    output_string += choice(letters_list)
        
    for _ in range(password_length - 1):
        try:
            char_of_choice = choice(min_chars_list)
        
            output_string += char_of_choice
            min_chars_list.remove(char_of_choice)
            
        except Exception:
            random_char = choice(all_chars_list)
            is_upper = randint(0, 1)
    
            if random_char in letters_list and is_upper == 0:
                output_string += random_char.upper()
            elif random_char in letters_list and is_upper == 1:
                output_string += random_char.lower()
            else:
                output_string += random_char
    
    return output_string

# © Tanay Jaiman - Jul 2 2022 