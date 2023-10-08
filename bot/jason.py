import address_book
import file_sort
import note_book


def main():

    while True:
        
        choice = input('1) Address book of your victims; 2) Notebook for special murders; 3) Sort files in some folder; 4) Exit. \nChoose program: ')
        
        try:
            choice = int(choice)
        except ValueError as error:
            print('Use only specified numbers!')

        if  choice == 1:
            address_book.main()
        elif choice == 2:
            note_book.main()
        elif choice == 3:
            file_sort.main()
        elif choice == 4:
            exit()
        else:
            print('Use only specified numbers!')

if __name__ == '__main__':
    main()