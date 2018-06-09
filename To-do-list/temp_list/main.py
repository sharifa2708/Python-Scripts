from to_do_list import tasks
import datetime

#menu for user
def menu(to_do_list):
    print('''
    ------- TO DO LIST -------
    1 - Add a task
    2 - search for a task
    3 - Show all tasks
    4 - empty list
    5 - save list to file
    6 - load list from file
    7 - update wallpaper
    8 - exit
    ''')
    val = int(input('\n>>> '))
    while val != 8:
        if val not in range(1,7+1):
            val = input('Incorrect Choice! Enter again: ')

        if val == 1:

            #input message
            message = input('Message: ')
            correct_date = False

            #input date
            while not correct_date:
                try:
                    date = input('Due date(DD-MM-YYYY): ')
                    day, month, year = date.split('-')
                    date = datetime.date(int(year), int(month), int(day))
                    correct_date = True
                except Exception as e:
                    print(f'{e}! PLease try again!')

            #input priority
            urg = int(input('How urgent is this task(1-10): '))
            while urg not in range(1,10+1):
                print('Out of bounds! Try Again')
                urg = int(input('How urgent is this task(1-10): '))

            imp = int(input('How important is this task(1-10): '))
            while imp not in range(1,10+1):
                print('Out of bounds! Try Again')
                imp = int(input('How important is this task(1-10): '))
            urg_imp = round(urg/imp,2)
            print(' ')
            #add task to to do list
            to_do_list.add(message,date,urg_imp)

        if val == 2:
            print('''
            search by:
            1 - Message
            2 - keyword
            3 - date
            ''')
            sval = int(input('\n> '))
            while sval not in [1,2,3]:
                sval = input('Incorrect Choice! Enter again: ')

            if sval == 1:
                message = input('Message to be searched: ')
                plist = to_do_list.search(key='message',value=message)

            if sval == 2:
                keyword = input('Enter keyword to be searched: ')
                plist = to_do_list.keyword_search(keyword)

            if sval == 3:
                #input date
                correct_date = False
                while not correct_date:
                    #try:
                    print('Due date(DD-MM-YYYY): ',end=' ')
                    date = input()
                    day, month, year = date.split('-')
                    date = datetime.date(int(year), int(month), int(day))
                    correct_date = True
                    #except Exception as e:
                print('')

                plist = to_do_list.search(key='date',value=date)

            print('\n\t[\n\n  Search Results:\n')
            to_do_list.show(full_list=False,partial_list=plist)
            print('\n\t]\n')

        if val == 3:
            print('\n\t[\n\n Your to-do list:\n')
            to_do_list.show()
            print('\t]\n')

        if val == 4:
            to_do_list.empty()

        if val == 5:
            to_do_list.save()

        if val == 6:
            to_do_list.load()

        if val == 7:
            print('You may need to restart gnome for the changes to be reflected!')
            to_do_list.update_wallpaper()

        if val == 8:
            break
        print('')
        print('''
        ------- TO DO LIST -------
        1 - Add a task
        2 - search for a task
        3 - Show all tasks
        4 - empty list
        5 - save list to file
        6 - load list from file
        7 - update wallpaper
        8 - exit
        ''')
        val = int(input('\n>>> '))


### --- MAIN --- ###
to_do_list = tasks()
menu(to_do_list)
