from testfunction import *

def main_menu():
    datafile = initialize_csv()
    
    while True:
        print("Welcome to the Malaysian Tax Calculation System")
        print("1. Register User")
        print("2. Login")
        print("3. View All Tax Records")
        print("4. Exit")
        choice = int(input("Please select an choice: "))

        try:
            if choice == 1:
                if not register_user(datafile):
                    print("Registration failed.")

            elif choice == 2:
                datafile = initialize_csv()
                ic_number = login_user(datafile)
                if ic_number:
                    income = int(input("Total Annual Income: "))
                    tax_relief = calculate_relief()
                    taxable_income = income - tax_relief
                    tax_payable = calculate_tax(taxable_income)
                    save_to_csv(ic_number, tax_relief, tax_payable, income, datafile)

            elif choice == 3:
                ic_number = login_user(datafile)
                if ic_number:
                    read_csv(ic_number, datafile)
            elif choice == 4:
                print("Thank you for using the Tax Calculation System. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
                print()


main_menu()
