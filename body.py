
from connection_pool import get_connection
from orm import CPA, Client, Assistant, TaxReturn
from datetime import datetime

def prompt_add_client(cursor):
    name = input('Enter client name: ')
    address = input('Enter client address: ')
    income = input('Enter client income: ')
    cpa_id = input('Enter the CPA ID: ')
    add_client(cursor, name, address, income, cpa_id)

def prompt_add_assistant(cursor):
    name = input("Enter assistant's name: ")
    cpa_id = input("Enter CPA ID: ")
    add_assistant(cursor, name, cpa_id)

def prompt_add_cpa(cursor):
    name = input('Enter CPA name: ')
    add_cpa(cursor, name)

def prompt_add_return(cursor):
    client_id = input("Enter client ID: ")
    assistant_id = input("Enter assistant ID: ")
    cpa_id = input("Enter CPA ID: ")
    status = input("Enter status: ")
    add_return(cursor, client_id, assistant_id, cpa_id, status)

def prompt_mark_materials(cursor):
    client_id = input('Enter client_id: ')
    mark_materials(cursor, client_id)

def prompt_check_materials(cursor):
    client_id = input('Enter client_id: ')
    check_materials(cursor, client_id)

def prompt_mark_filed(cursor):
    return_id = input('Enter return_id: ')
    mark_filed(cursor, return_id)

def prompt_check_filed(cursor):
    return_id = input('Enter return_id: ')
    check_filed(cursor, return_id)

def prompt_mark_checked(cursor):
    return_id = input('Enter return_id: ')
    mark_cpa_check(cursor, return_id)

def prompt_check_checked(cursor):
    return_id = input('Enter return_id: ')
    check_cpa_check(cursor, return_id)

def search(cursor):
    search_menu = """ Type Letter to Search by Name: \n 
    A. Assistant \n 
    B. CPA \n 
    C. Client \n 
    D. Tax Return \n 
    """
    option = input(search_menu).upper()

    if option == "A":
        name = input("Enter the assistant's name: ")
        for assistant in Assistant.search_from_db_by_name(cursor, name):
            print(assistant, "\n")

    elif option == "B":
        name = input("Enter the CPA's full name: ")
        for cpa in CPA.search_from_db_by_name(cursor, name):
            print(cpa, "\n")

    elif option == "C":
        name = input("Enter the client's full name: ")
        for client in Client.search_from_db_by_name(cursor, name):
            print(client, "\n")

    else:
        name = input("Enter the client's full name: ")
        for tr in TaxReturn.search_from_db_by_name(cursor, name):
            print(tr, "\n")



def add_cpa(cursor, name):
    # add a cpa
    new_cpa = CPA(name=name)
    new_cpa.save(cursor)
    print("CPA has been added \n")

def add_assistant(cursor, name, cpa_id):
    # add an assistant
    new_assistant = Assistant(name=name, cpa_id=cpa_id)
    new_assistant.save(cursor)
    print("Assistant has been added \n")

def add_client(cursor, name, address, income, cpa_id):
    # onboard a client
    new_client = Client(name=name, address=address, income=income, cpa_id=cpa_id)
    new_client.save(cursor)
    print("Client has been added \n")

def add_return(cursor, client_id, assistant_id, cpa_id, status):
    # add a tax return
    new_return = TaxReturn(client_id=client_id, assistant_id=assistant_id, cpa_id=cpa_id, status=status)
    new_return.save(cursor)
    print("Tax return has been added \n")

def mark_materials(cursor, client_id):
    # mark if a client has provided required materials

    mark = Client.load_from_db(cursor, client_id)
    mark.materials_provided_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mark.save(cursor)
    print("Materials Marked \n")

def check_materials(cursor, client_id):
    # check if a client has provided required materials
    row = Client.load_from_db(cursor, client_id)
    if row.materials_provided_at is None:
        print("The client has not been provided their materials yet.\n")
    else:
        print(f"The client provided their materials at {row.materials_provided_at} \n")


def mark_filed(cursor, return_id):
    # mark a tax return as filed
    mark = TaxReturn.load_from_db(cursor, return_id)
    mark.filed_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mark.status = "Filed"
    mark.save(cursor)
    print("Tax return marked as filed \n")

def check_filed(cursor, return_id):
    # check if a tax return is filed
    row = TaxReturn.load_from_db(cursor, return_id)
    if row.filed_at is None or row.status == "Not Filed" :
        print("The tax return has not been filed")
    else:
        print(f"The return was filed at {row.filed_at} \n")

def mark_cpa_check(cursor, return_id):
    # mark if a cpa checked a return
    mark = TaxReturn.load_from_db(cursor, return_id)
    mark.reviewed_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mark.save(cursor)
    print("Tax return marked as reviewed \n")


def check_cpa_check(cursor, return_id):
    # check if the cpa checked a return
    check = TaxReturn.load_from_db(cursor, return_id)
    if check.reviewed_at is None:
        print("The tax return has not been reviewed yet \n")
    else:
        print(f"The tax return was reviewed at {check.reviewed_at} \n")