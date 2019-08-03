f = open('users.txt')
ha = input('Uname: ')
he = input('Pwd: ')
for lines in f:
    if lines.split(' ')[0] == ha:
        if lines.split(' ')[1] == he:
            print('Login Successful')
        else:
            print('Password Incorrect')



