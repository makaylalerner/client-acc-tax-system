import datetime
import random
from typing import List, Dict, Union, Callable


import body
from connection_pool import get_connection

def run(connection, cursor):
    menu = """ Choose one of the following: \n 
1. Add a new client \n 
2. Add a client's tax return. \n
3. Add a new tax filing assistant \n 
4. Add a new CPA \n 
5. Mark a client's materials provided \n 
6. Check if a client's materials have been provided \n 
7. Mark a tax return as filed \n 
8. Check if a return was filed \n 
9. Mark a tax return as checked by CPA \n 
10. Check if a CPA checked a return \n 
11. Search for an ID \n
Enter x to exit 
"""

    option = '0'
    while option != 'x':

        option = input(menu)

        if option == '1':
            body.prompt_add_client(cursor)

        elif option == '2':
            body.prompt_add_return(cursor)

        elif option == '3':
            body.prompt_add_assistant(cursor)

        elif option == '4':
            body.prompt_add_cpa(cursor)

        elif option == '5':
            body.prompt_mark_materials(cursor)

        elif option == '6':
            body.prompt_check_materials(cursor)

        elif option == '7':
            body.prompt_mark_filed(cursor)

        elif option == '8':
            body.prompt_check_filed(cursor)

        elif option == '9':
            body.prompt_mark_checked(cursor)

        elif option == '10':
            body.prompt_check_checked(cursor)

        elif option == '11':
            body.search(cursor)

        else:
            print("Input invalid")
            option = input(menu)

        connection.commit()


if __name__ == "__main__":
    with get_connection() as connection:
        with connection.cursor() as cursor:
            run(connection, cursor)
        connection.commit()