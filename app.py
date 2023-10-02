from faker import Faker
import random
import csv
from datetime import datetime, timedelta


def generate_fake_accounts(num_accounts):
    fake = Faker()
    accounts = []
    for _ in range(num_accounts):
        account = {}
        account['id'] = random.randint(0, num_accounts + 1)
        account['plan'] = random.choice(['free', 'basic', 'full'])
        account['username'] = fake.user_name()
        account['last_login_date'] = fake.date_between(start_date='-1y', end_date='today')
        account['expire_date'] = fake.date_between(start_date='-1y', end_date='+1y')
        accounts.append(account)
    return accounts

def save_accounts_to_csv(accounts, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['id', 'plan', 'username', 'last_login_date', 'expire_date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(accounts)

def load_accounts_from_csv(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        accounts = [account for account in reader]
    return accounts

def print_total_accounts(accounts):
    plans = {}
    for account in accounts:
        plan = account['plan']
        plans[plan] = plans.get(plan, 0) + 1
    print("\nTotal accounts according to plans:")
    for plan, count in plans.items():
        print(f'{plan}: {count}')
    print()

def find_inactive_free_accounts(accounts):
    today = datetime.today().date()
    inactive_accounts = [
        account 
        for account in accounts 
        if account['plan'] == 'free' and 
        (today - datetime.strptime(account['last_login_date'], '%Y-%m-%d').date()).days > 90
    ]
    return inactive_accounts

def find_expired_accounts(accounts):
    today = datetime.today().date()
    expired_accounts = [
        account 
        for account in accounts 
        if account['plan'] in ['basic', 'full'] and 
        datetime.strptime(account['expire_date'], '%Y-%m-%d').date() < today
    ]
    return expired_accounts


if __name__ == '__main__':
    accounts = generate_fake_accounts(1003)
    save_accounts_to_csv(accounts,'accounts.csv')
    loaded_accounts = load_accounts_from_csv('accounts.csv')

    while True:
        print("Menu:")
        print("1. Display the total number of accounts according to plans")
        print("2. Find Free accounts with more than 3 months without logging in")
        print("3. Find expired accounts with basic or full plans")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            print_total_accounts(loaded_accounts)
        elif choice == '2':
            inactive_accounts = find_inactive_free_accounts(loaded_accounts)
            if len(inactive_accounts) == 0:
                print("No free accounts with more than 3 months without logging in")
            else:
                print("Free accounts with more than 3 months without logging in:")
                for account in inactive_accounts:
                    print(
                        f'''
                        id: {account['id']}
                        plan: {account['plan']}
                        username: {account['username']}
                        last login date: {account['last_login_date']}
                        expire date: {account['expire_date']}
                        '''
                    )
        elif choice == '3':
            expired_accounts = find_expired_accounts(loaded_accounts)
            if len(expired_accounts) == 0:
                print("No expired accounts with basic or full plans")
            else:
                print("Expired accounts with basic or full plans:")
                for account in expired_accounts:
                    print(
                        f'''
                        id: {account['id']}
                        plan: {account['plan']}
                        username: {account['username']}
                        last login date: {account['last_login_date']}
                        expire date: {account['expire_date']}
                        '''
                    )
        elif choice == '4':
            break
        else:
            print("Wrong. Try again.")