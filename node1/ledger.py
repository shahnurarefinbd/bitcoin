# Creating different wallet for users

def query_balance(target_user):
    f = open("Ledger.txt", "r")
    content = f.readlines()
    f.close()

    balance = 0

    for l in content:
        line_value = l.split(":")
        if line_value[0] == target_user:
            balance = balance - int(line_value[2])
        if line_value[1] == target_user:
            balance = balance + int(line_value[2])
    return balance


def transfer_value(from_user, to_user, amount):
    # new line for each transaction
    new_line = str(from_user) + ":" + str(to_user) + ":" + str(amount)
    f = open("Ledger.txt", "a")
    f.write(new_line + "\n")
    f.close()


def initiate_users(user_name):
    transfer_value("ledger", user_name, 100)
    # leger : bob : 100
