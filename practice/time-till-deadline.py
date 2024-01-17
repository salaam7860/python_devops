from datetime import datetime


# Ask the user about his goal and the deadline & split the user input and make list 
def user():
    user_input = input("Enter your goal with a deadline separated by colon\n")
    input_list = user_input.split(':')
    sp_var(input_list)


# make that list into separate variables 
def sp_var(input_list):
    goal = input_list[0]
    deadline = input_list[1]
    cal(deadline)


# Calculate how many days from now till deadline 
def cal(deadline):
    deadline_date = datetime.strptime(deadline, "%d.%m.%Y")
    today_date = datetime.today()
    print(deadline_date - today_date)

user()







