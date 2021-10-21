import json
import random
from datetime import datetime


"""
Distributeur de billet :

S'inscire :
    Mot de passe aléatoire (4 chiffres)
    Dire le nombre d'argent que l'on a

Retirer de l'argent :
    Rentrer son mot de passe
    Retirer l'argent

Avoir un json:
    stocke les mots de passe
    stocke le solde

Avoir un ficher texte pour chaque personne qui stocke l'historique des virements
"""


def main():

    print("Que veux-tu faire :")
    choice = input("1- S'inscire\n2- Retirer de l'argent\n3- Ajouter de l'argent\n")

    while choice not in ('1', '2', '3'):
        print("Je n'ai pas compris")
        choice = input("1- S'inscire\n2- Retirer de l'argent\n3- Ajouter de l'argent\n")

    if choice == '1':
        register()
    elif choice == '2':
        withdraw()
    else:
        moneyInput()


def register():

    userData = manageFile()

    password = str(random.randint(0, 9999))
    password = '0'*(4-len(password)) + password

    while password in list(userData.keys()):
        password = str(random.randint(0, 9999))
        password = '0'*(4-len(password)) + password

    print(f"Ton mot de passe est : {password}")

    while True:
        try:
            money = int(input("Combien d'argent as-tu ?\n"))
            break
        except ValueError:
            print("Je ne comprend pas !")

    manageLog(password, money)
    userData[password] = money

    manageFile(userData)


def withdraw():
    password = input("Quel est ton mot de passe ?")

    userData = manageFile()

    while password not in userData.keys():
        print("Ce n'est pas le bon mot de passe")
        password = input("Quel est ton mot de passe ?")

    while True:
        try:
            amountMoneyWithdraw = int(input("Combien d'argent veux-tu retirer ?\n"))
            if amountMoneyWithdraw > userData[password]:
                print("Tu ne pas retirer tout ça, pauvre fou")
                continue
            elif amountMoneyWithdraw == userData[password]:
                print("Attention, tu n'as plus d'argent !")
            break
        except ValueError:
            print("Je n'ai pas compris")

    currentAmountMoney = userData[password]

    manageLog(password, f"-{amountMoneyWithdraw}")

    currentAmountMoney -= amountMoneyWithdraw

    userData[password] = currentAmountMoney
    print(f"Il te reste {userData[password]}")

    manageFile(userData)


def moneyInput():
    password = input("Quel est ton mot de passe ?")

    userData = manageFile()

    while password not in userData.keys():
        print("Ce n'est pas le bon mot de passe")
        password = input("Quel est ton mot de passe ?")

    while True:
        try:
            amountMoneyInput = int(input("Combien d'argent veux-tu ajouter ?\n"))
            break
        except ValueError:
            print("Je n'ai pas compris")

    manageLog(password, f"+{amountMoneyInput}")

    currentAmountMoney = userData[password]

    currentAmountMoney += amountMoneyInput

    userData[password] = currentAmountMoney

    print(f"Il te reste {userData[password]}")

    manageFile(userData)


def manageFile(toWrite=None):

    if toWrite is not None:
        with open('userData.json', 'w', encoding='utf-8') as f:
            json.dump(toWrite, f, indent=4)
    else:
        with open('userData.json', encoding='utf-8') as f:
            userData = json.load(f)
        return userData


def manageLog(password, amount):
    with open(f"log/log-{password}.txt", 'a', encoding='utf-8') as f:
        now = datetime.now()
        dateString = now.strftime("%d/%m/%Y %H:%M:%S")
        f.write(f"{dateString} ; {amount}\n")


if __name__ == "__main__":
    main()
