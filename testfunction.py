import pandas as pd

def initialize_csv():
    try:
        datafile = pd.read_csv("User_data.csv", dtype={
            "IC Number": "string",
            "Password": "string",
            "Income": "Int64",
            "Tax Relief": "Int64",
            "Tax Payable": "Int64"
        })
    
        return datafile
    except FileNotFoundError:
        datafile = pd.DataFrame(columns=["IC Number", "Password", "Income", "Tax Relief", "Tax Payable"])

        datafile = datafile.astype({
            "IC Number": "string",
            "Password": "string",
            "Income": "Int64",
            "Tax Relief": "Int64",
            "Tax Payable": "Int64"
        })

        datafile.to_csv("User_data.csv", index=False)
        return datafile

def register_user(datafile):
    while True:
        print("Registration Menu")
        print()
        ic_number = input("Please Enter Your IC Number To Register:").replace("-","").strip()
        password = input("Please Enter Your Password To Register[LAST FOUR DIGITS OF YOUR IC NUMBER]:")

        if verify_user(ic_number, password):
            print("USER'S DATA VERIFIED.")

            user_search = datafile[(datafile["IC Number"] == ic_number) & (datafile["Password"] == password)]
            if user_search.empty:
                new_user = pd.DataFrame({
                    "IC Number": [ic_number],
                    "Password": [password],
                    "Income": [""],
                    "Tax Relief": [""],
                    "Tax Payable": [""]
                })

                datafile = pd.concat([datafile, new_user], ignore_index=True)
                datafile.to_csv("User_data.csv", index=False)
                print("Registration successful. Proceed to login to access your account.")

                return datafile
            else:
                print("User already exists. Please login.")
                return True
        else:
            print("User verification failed. Please try again.")
            return False
        
def login_user(datafile):
    print("Login Menu")
    print()
    ic_number = input("IC Number:").replace("-","").strip()
    password = input("Password:")
    
    user_search = datafile[(datafile["IC Number"] == ic_number) & (datafile["Password"] == password)]
    if  user_search.empty:
        print("User not found. Please register.")
        return False
    else:
        return ic_number
    
def calculate_relief():
    print("\n=== Malaysian Tax Relief Calculator ===")
    
    # Initialize relief categories with maximum amounts
    relief_limits = {
        'Individual': 9000,
        'Spouse': 4000,
        'Child': 8000,
        'Medical': 8000,
        'Lifestyle': 2500,
        'Education': 7000,
        'Parental': 5000
    }
    
    reliefs = {}
    
    # 1. Individual Relief (auto-applied)
    reliefs['Individual'] = relief_limits['Individual']
    print(f"\n1. Individual Relief: RM{reliefs['Individual']} (auto-applied)")
    
    # 2. Spouse Relief
    if input("Do you have a spouse? (y/n): ").lower() == 'y':
        spouse_income = float(input("Enter spouse's annual income (RM): "))
        if spouse_income <= 4000:
            reliefs['Spouse'] = relief_limits['Spouse']
            print(f"2. Spouse Relief: RM{reliefs['Spouse']}")
    
    # 3. Child Relief
    child_count = int(input("Number of eligible children: "))
    if child_count > 0:
        reliefs['Child'] = min(child_count, 12) * relief_limits['Child']
        print(f"3. Child Relief: RM{reliefs['Child']} ({min(child_count, 12)} children)")
    
    # 4. Medical Expenses
    medical = float(input("Enter medical expenses (RM): "))
    if medical > 0:
        reliefs['Medical'] = min(medical, relief_limits['Medical'])
        print(f"4. Medical Relief: RM{reliefs['Medical']}")
    
    # 5. Lifestyle
    lifestyle = float(input("Enter lifestyle expenses (RM): "))
    if lifestyle > 0:
        reliefs['Lifestyle'] = min(lifestyle, relief_limits['Lifestyle'])
        print(f"5. Lifestyle Relief: RM{reliefs['Lifestyle']}")
    
    # 6. Education
    education = float(input("Enter education fees (RM): "))
    if education > 0:
        reliefs['Education'] = min(education, relief_limits['Education'])
        print(f"6. Education Relief: RM{reliefs['Education']}")
    
    # 7. Parental Care
    if input("Do you support your parents? (y/n): ").lower() == 'y':
        reliefs['Parental'] = relief_limits['Parental']
        print(f"7. Parental Care Relief: RM{reliefs['Parental']}")
    
    # Calculate total
    total_relief = sum(reliefs.values())
    print(f"\n=== TOTAL TAX RELIEF: RM{total_relief} ===")
    
    # Save to file
    
    
    return total_relief






def calculate_tax(income):
    tax = 0
    brackets = [
        (5000, 0),
        (20000, 0.01),
        (35000, 0.03),
        (50000, 0.06),
        (70000, 0.11),
        (100000, 0.19),
        (400000, 0.25),
        (600000, 0.26),
        (2000000, 0.28),
        (float('inf'), 0.30)
    ]

    remaining_income = income
    for bracker in brackets:
        limit, rate = bracker
        if remaining_income <= 0:
            break
        taxable = min(remaining_income, limit)
        tax += taxable * rate
        remaining_income -= taxable
    return int(round(tax))    

          
def verify_user(ic_number,password):
    return len(ic_number) == 12 and ic_number[-4:] == password
     
def save_to_csv(ic_number, tax_relief, tax_payable, income, datafile):
    datafile.loc[datafile["IC Number"] == ic_number, "Tax Payable"] = tax_payable
    datafile.loc[datafile["IC Number"] == ic_number, "Tax Relief"] = tax_relief
    datafile.loc[datafile["IC Number"] == ic_number, "Income"] = income
    datafile.to_csv("User_data.csv", index=False)

def read_csv(ic_number, datafile):
    matched_user = datafile[(datafile["IC Number"] == ic_number)]
    if matched_user.empty:
        print("No match user found.")
    else:
        print("User found. Here are the details:")
        print(matched_user[["IC Number", "Income", "Tax Relief", "Tax Payable"]])  