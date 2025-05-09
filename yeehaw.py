# setting admin login information
admin_username = "admin"        # this is hardcoded for admin only
admin_password = "admin123"

# file names that are used to store customer, user, transaction informations
customers_file = "customer.txt"
users_file = "user.txt"
transactions_file = "transaction.txt"

# dictionary that holds customer information
customers_dict = {}     # during the program run this will store the customer info

# creating the customers file if it doesnt exist
def create_customers_file():
    try:
        with open(customers_file, 'r') as file: # this reads the file to know if that file already exists
            pass
    except FileNotFoundError:
        with open(customers_file, 'w') as file: # this creates that file 
            pass

# creatning the users file if it doesnt exist
def create_users_file():
    try:
        with open(users_file, 'r') as file:
            pass
    except FileNotFoundError:
        with open(users_file, 'w') as file:
            pass

# creating the transactions file if it doesnt exist
def create_transactions_file():
    try:
        with open(transactions_file, 'r') as file:
            pass
    except FileNotFoundError:
        with open(transactions_file, 'w') as file:
            pass

#loading all customers into dictionary 
def load_customers():           # when the program starts this will load customers into the dictionary
    global customers_dict
    with open(customers_file, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) != 4:
                continue
            acc_num, name, address, balance = parts
            customers_dict[acc_num] = {
                'name': name,
                'address': address,
                'balance': float(balance)
            }

# saving customrs info from disctionary to file
def save_customers():
    with open(customers_file, 'w') as file:
        for acc_num, data in customers_dict.items():
            file.write(f"{acc_num},{data['name']},{data['address']},{data['balance']}\n")

# creating a new unique customer id aka account number
def get_customers_id():
    with open(customers_file,'r') as file:
        lines = file.readlines()

        if lines:
            last_line = lines[-1]
            last_id = last_line.split(',')[0]
            last_id_num = last_id[1:]
            next_id_num = int(last_id_num) + 1
            next_id = "C" + f"{next_id_num:03d}"
            return next_id
        
        else:
            return "C001"  # this line makes the count start from C001 if it doesnt already exist

# printing admin menu options
def admin_menu():
    print("\nAdmin Menu:")
    print("1. Create Customer")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Check Balance")
    print("5. Transaction History")
    print("6. Exit")

# printing customer menu options
def customer_menu():
    print("\nCustomer Menu:")
    print("1. Deposit Money")
    print("2. Withdraw Money")
    print("3. Check Balance")
    print("4. Transaction History")
    print("5. Exit")

# login function for both admin and customers
def login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

# checking admin login
    if username == admin_username and password == admin_password:
        return "admin", None

#checking customer login from file
    with open(users_file, 'r') as file:
        lines = file.readlines()
        for things in lines:
            parts = things.strip().split(',')
            if len(parts) != 3:
                continue
            cus_username = parts[1].strip()
            cus_password = parts[2].strip()
            if password == cus_password and username == cus_username:
                return "customer", parts[0]

    print("Invalid Credentials!")
    return None, None

# creating a new custtomer using function
def create_customer():
    print("Create New Customer")
    name = input("Enter customer name: ")
    username = input("Enter Customer Username: ")

    with open(users_file, 'r') as file:     # this will check if the username already exists
        lines = file.readlines()
        for line in lines:
            if line.strip().split(',')[1] == username:
                print("Username Already Exists")
                return

    password = input("Enter Customer Password: ")
    address = input("Enter Customer Address: ")
    initial_balance = (input("Enter Initial Balance: "))

    if not initial_balance.isdigit() or float(initial_balance) < 0:
        print("Invalid Balance")
        return
    
    initial_balance = float(initial_balance)
    account_number = get_customers_id()

# adding customer to dictionary
    customers_dict[account_number] = {
        'name': name,
        'address': address,
        'balance': initial_balance
    }
    save_customers()

#  adding user login details to file
    with open(users_file, 'a') as file:
        file.write(f"{account_number},{username},{password}\n")

    print(f"Customer Created Successfully! Account Number: {account_number}")

# finding a customer using account number
def find_customer(account_number):
    return customers_dict.get(account_number)

# updating balance and saving that to file 
def update_balance(account_number, new_balance):
    if account_number in customers_dict:
        customers_dict[account_number]['balance'] = new_balance
        save_customers()

# recording a transaction to file
def record_transaction(account_number, transaction_type, amount):
    with open(transactions_file, 'a') as file:
        file.write(f'{account_number},{transaction_type},{amount}\n')

# depositing money to account
def deposit_money(account_number):
    customer = find_customer(account_number)
    if not customer:
        print("Customer Not Found")
        return

    print(f"Current Balance: {customer['balance']}")
    amount = (input("Enter deposit amount: "))
    if not amount.isdigit() or float(amount) <= 0:
        print("Invalid Amount")
        return

    amount = float(amount)
    new_balance = customer['balance'] + amount
    update_balance(account_number, new_balance)
    record_transaction(account_number, "DEPOSIT", amount)
    print(f"Deposit Successful. New Balance: {new_balance}")

# withdrawing money from account
def withdraw_money(account_number):
    customer = find_customer(account_number)
    if not customer:
        print("Customer Not Found")
        return

    print(f"Current Balance: {customer['balance']}")
    amount = (input("Enter Withdrawal amount: "))
    if not amount.isdigit() or float(amount) <= 0:
        print("Invalid Amount")
        return
    
    if float(amount) > customer['balance']:
        print("Insufficient Funds")
        return

    amount = float(amount)
    new_balance = customer['balance'] - amount
    update_balance(account_number, new_balance)
    record_transaction(account_number, "WITHDRAW", amount)
    print(f"Withdrawal successful! New Balance: {new_balance}")

# checking customer balance
def check_new_balance(account_number):
    customer = find_customer(account_number)
    if customer:
        print(f"Account Balance For {customer['name']}: {customer['balance']}")
    else:
        print('Customer not found')

# viewing tramnsaction history for a customer
def view_history(account_number):
    print(f'Transaction history for account number: {account_number}')
    found = False
    with open(transactions_file, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if parts[0] == account_number:
                print(f"{parts[1]}: {parts[2]}")
                found = True
    if not found:
        print("No transactions found.")

# main program starts here 
def main():
    create_users_file()
    create_customers_file()
    create_transactions_file()
    load_customers()

    while True:
        print("\nLOGIN MENU")
        print("1. Login")
        print("2. Exit Program")
        main_choice = input("Enter choice: ")

        if main_choice == '2':
            print("Goodbye!")
            break
        elif main_choice != '1':
            print("Invalid choice!")
            continue

        role, account_number = login()
        if not role:
            continue

# admin operations
        if role == "admin":
            while True:
                admin_menu()
                choice = input("Enter your choice (1-6): ")
                if choice == '1':
                    create_customer()
                elif choice == '2':
                    acc_num = input("Enter Account Number: ")
                    deposit_money(acc_num)
                elif choice == '3':
                    acc_num = input("Enter Account Number: ")
                    withdraw_money(acc_num)
                elif choice == '4':
                    acc_num = input("Enter Account Number: ")
                    check_new_balance(acc_num)
                elif choice == '5':
                    acc_num = input("Enter Account Number: ")
                    view_history(acc_num)
                elif choice == '6':
                    print("Exiting admin menu...")
                    break
                else:
                    print("Invalid choice!")
                    #test
#test2
# customer operations
        else:
            while True:
                customer_menu()
                choice = input("Enter your choice (1-5): ")
                if choice == '1':
                    deposit_money(account_number)
                elif choice == '2':
                    withdraw_money(account_number)
                elif choice == '3':
                    check_new_balance(account_number)
                elif choice == '4':
                    view_history(account_number)
                elif choice == '5':
                    print("Exiting customer menu...")
                    break
                else:
                    print("Invalid choice!")

main()