# %%
from pywebio.input import *
import time
import pandas as pd  # to perform data manipulation and analysis
import numpy as np  # to cleanse data
from datetime import datetime  # to manipulate dates
import plotly.express as px  # to create interactive charts
import plotly.graph_objects as go  # to create interactive charts
# to build Dash apps from Jupyter environments
from jupyter_dash import JupyterDash
# to get components for interactive user interfaces
import dash_core_components as dcc
# to compose the dash layout using Python structures
import dash_html_components as html
from pathlib import Path
from pywebio import *  # for pywebio
from pywebio.input import *  # for pywebio
from pywebio.output import *  # for pywebio
import smtplib
from email.mime.text import MIMEText


# %%
# check if database exists, if not, create one


def check_if_database_exists():
    file = Path("my_budget.csv")
    if file.exists():
        user_df = pd.read_csv(file)
    else:
        user_df = pd.DataFrame(
            columns=['Username', 'Designated Budget', 'Remaining Budget'])
        # write into csv
        user_df.to_csv('my_budget.csv', index=False)
    return user_df

# %%
# check if user exists, if not, create one


def check_if_user_exists(username):
    if username in user_df['Username'].values:
        return str("Old User")
    else:
        return str("New User")


# %%
def user_type_actions(user_type):
    if user_type == "Old User":
        put_text(f"Welcome back, {username}!")
        user_budget = float(user_df["Remaining Budget"]
                            [user_df["Username"] == username])
        # put_text(f"Hi {username}, your budget is {user_budget}!")
    elif user_type == "New User":
        put_text(
            f"Hi {username}, since you are a first time user, let's set a budget for the month!")
        user_budget = float(
            input("Please input your budget for the month: ", type=FLOAT, required=True))
        new_user_data = [username, user_budget, user_budget]
        user_df.loc[len(user_df), :] = new_user_data
        # put_text(f"Hi {username}, your budget is {user_budget}!")
    return username, user_budget

# %%


def access_create_transaction_file(username):
    if user_type == "Old User":
        file = Path(f"{username}_transactions.csv")
        user_transaction_df = pd.read_csv(file)
    elif user_type == "New User":
        user_transaction_df = pd.DataFrame(
            columns=['Date', 'Amount', 'Category'])
        # write into csv
        user_transaction_df.to_csv(f"{username}_transactions.csv", index=False)
        file = Path(f"{username}_transactions.csv")
        user_transaction_df = pd.read_csv(file)

    return user_transaction_df

# %%


def main_page_decisions():
    selected_decision = radio("What would you like to do?", options=[
                              'Record a Transaction', 'Check Previous Transactions', 'Check Remaining Budget', 'Set New Budget', 'Quit'])
    return selected_decision

# %%


def record_transaction(user_transaction_df, user_df):
    from datetime import datetime
    today_date = datetime.today().strftime('%Y-%m-%d')

    # input details of transaction
    exp_date = today_date
    indiv_expense = input("Please input the amount", type=FLOAT, required=True)
    exp_category = radio("What's the category?", options=[
        'Food', 'Entertainment', 'Transport', 'Bills'])

    # record into df, general and transaction
    # general df
    initial_budget = float(user_df['Designated Budget'])
    remaining_budget = float(user_df['Remaining Budget'])
    remaining_budget = float(remaining_budget - indiv_expense)
    user_df['Remaining Budget'] = remaining_budget

    # transaction df
    new_transaction = [exp_date, indiv_expense, exp_category]
    user_transaction_df.loc[len(user_transaction_df), :] = new_transaction

    # transaction recording
    put_text("Your transaction is currently being recorded")
    put_text("Recording Transaction...")
    put_markdown("Transaction recorded!")

    return user_transaction_df, user_df

# %%


def check_previous_transactions(user_transaction_df):
    put_html(user_transaction_df.to_html(border=0))

# %%


def check_remaining_budget(user_df):
    remaining_budget = float(user_df['Remaining Budget'])
    designated_budget = float(user_df['Designated Budget'])
    remaining_budget_percent = "{:.0%}".format(
        remaining_budget/designated_budget)
    put_text(f"You are left with {remaining_budget_percent} of your budget!")
    return remaining_budget, remaining_budget_percent

# %%


def set_new_budget(user_df):
    new_user_budget = float(
        input("Please input your new budget: ", type=FLOAT, required=True))
    user_df['Designated Budget'] = new_user_budget
    user_df['Remaining Budget'] = new_user_budget
    put_text(f"Your New Budget is {new_user_budget}!")
    return new_user_budget, user_df


# %%

def quit_app():
    put_text("Thank you for using Dennis's tracker, Goodbye!")
    put_text("Please proceed to close this tab!")

# %%


# %%
# main page
# Import following modules
put_markdown("## Welcome to Budget Tracker by Dennis")

username = input("What's your name?", type=TEXT, required=True)

# check if database exist
user_df = check_if_database_exists()

# check if user is new or old
user_type = check_if_user_exists(username)

username, user_budget = user_type_actions(user_type)

put_text(f"Hi {username}, your budget is {user_budget}!")

user_transaction_df = access_create_transaction_file(username)

while True:
    selected_decision = main_page_decisions()
    # record transaction
    if selected_decision == "Record a Transaction":
        user_transaction_df, user_df = record_transaction(
            user_transaction_df, user_df)
        continue
    # check previous transactions
    elif selected_decision == "Check Previous Transactions":
        check_previous_transactions(user_transaction_df)
        continue
    # check remaining budget
    elif selected_decision == "Check Remaining Budget":
        remaining_budget, remaining_budget_percent = check_remaining_budget(
            user_df)
        continue

    elif selected_decision == "Set New Budget":
        new_user_budget, user_df = set_new_budget(user_df)
        continue

    # quit app
    elif selected_decision == "Quit":
        # record new details to both df
        user_transaction_df.to_csv(f"{username}_transactions.csv", index=False)
        user_df.to_csv("my_budget.csv", index=False)
        quit_app()
        break
