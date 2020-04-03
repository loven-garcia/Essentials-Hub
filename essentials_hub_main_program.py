#THIS IS THE MAIN PY FILE

from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter.font import Font
import sqlite3
import smtplib
import string
import random


# ======================================================FUNCTIONS===============================================================


def exit_launcher():
    root.destroy()


def main_login_window():
    
    global main_window
    main_window = Toplevel(root)
    main_window.geometry('1300x750+100+50')
    main_frame_for_main_window = Frame(main_window)
    main_frame_for_main_window.pack()
    
    canvas_main_window = Canvas(main_frame_for_main_window, width = 1300, height = 750)
    canvas_main_window.pack()
    canvas_main_window.create_image(0,0, anchor = NW, image = image_main_login_cover)

    frame_above_canvas = Frame(main_frame_for_main_window, bg = 'Black')
    canvas_main_window.create_window(720,150, anchor =NW, window = frame_above_canvas)

    #THE 2 FRAMES BELOW ARE FOR THE FRAMES ABOVE THE FRAME ABOVE CANVAS
    frame_above_frame_of_canvas_top = Frame(frame_above_canvas)
    frame_above_frame_of_canvas_top.pack()

    frame_above_frame_of_canvas_bottom = Frame(frame_above_canvas, bg = 'black')
    frame_above_frame_of_canvas_bottom.pack()

    #THIS IS FOR THE IMAGE ABOVE USERNAME AND PW
    canvas_top_of_main_rec = Canvas(frame_above_frame_of_canvas_top, width = 520, height = 115, highlightthickness = 0)
    canvas_top_of_main_rec.pack()
    canvas_top_of_main_rec.create_image(0,0, anchor = NW, image = image_main_login_top_of_main_rec)

    #THESE ARE FOR THE USERNAME AND PASSWORD
    global firstclick_username
    firstclick_username = True
    global firstclick_password
    firstclick_password = True
    
    # THESE ARE FOR THE ENTRY WIDGETS FOR USERNAME AND PASSWORD
    global entry_for_username
    entry_for_username = Entry(frame_above_frame_of_canvas_bottom, width = 34, font = font_for_username_and_password, bg = 'black', highlightbackground = 'white', fg = 'white', highlightthickness = 0.5, highlightcolor ='white')
    entry_for_username.insert(0, ' Username')
    entry_for_username.bind('<FocusIn>', on_entry_click_username)
    entry_for_username.grid(row = 0, column = 0, pady = 13, ipady =13, columnspan = 2)

    global entry_for_password
    entry_for_password = Entry(frame_above_frame_of_canvas_bottom,width = 34, font = font_for_username_and_password, bg = 'black', highlightbackground = 'white', fg = 'white', highlightthickness = 0.5, highlightcolor ='white')
    entry_for_password.insert(0, ' Password')
    entry_for_password.bind('<FocusIn>', on_entry_click_password)
    entry_for_password.grid(row = 1, column = 0, pady = (13,15), ipady =13, columnspan = 2)
 

    #THIS IS FOR THE CHECK BUTTON
    global variable_for_sign_in_as_admin
    variable_for_sign_in_as_admin = IntVar()
    variable_for_sign_in_as_admin.set(0)
    check_button_admin_or_not = Checkbutton(frame_above_frame_of_canvas_bottom, font = font_for_login_check_button, text = '  Sign in as Admin', variable = variable_for_sign_in_as_admin, bg = 'Black',fg = 'White')
    check_button_admin_or_not.grid(row = 2, column = 0, pady = (0,10), sticky = W, columnspan = 2)


    #THESE ARE FOR THE SIGN-IN AND SIGN-UP BUTTONS
    button_for_sign_in = Button(frame_above_frame_of_canvas_bottom, text = 'Login', font =font_for_sign_in_sign_up, bg = '#e99314', fg = 'Black', command = sign_in)
    button_for_sign_in.grid(row = 3, column = 0, pady = (35,5), ipady = 11, ipadx = 90, sticky = W)

    button_for_sign_up = Button(frame_above_frame_of_canvas_bottom, text = 'Or Sign Up', font = font_for_sign_in_sign_up, bg = 'black', fg = '#e99314', borderwidth = 0, command = sign_up)
    button_for_sign_up.grid(row = 3, column = 1, pady = (35,5), sticky = W)

    #BUTTON FOR FORGOT PASSWORD
    button_for_sign_up = Button(frame_above_frame_of_canvas_bottom, text = 'Forgot Password?', font = font_for_sign_in_sign_up, bg = 'black', fg = '#e99314', borderwidth = 0, command = forgot_password)
    button_for_sign_up.grid(row = 4, column = 0, sticky = W)


# < FOR REMOVING THE INSERT TEXT ON USERNAME AND PASSWORD
def on_entry_click_username(event):
    global firstclick_username
    if firstclick_username:
        firstclick_username = False
        entry_for_username.delete(0, 'end') 


def on_entry_click_password(event):
    global firstclick_password
    if firstclick_password:
        firstclick_password = False
        entry_for_password.delete(0, 'end') 
        entry_for_password.config(show = '*')
# >

def sign_in():
        
        #THIS IS TO CHECK WHETHER ALL THE BOXES ARE FILLED
        if entry_for_username.get() == '' or entry_for_password.get() == '':
            messagebox.showerror('ERROR!', 'Please fill all the boxes!', parent = main_window)

        else:
            
            #STORE THE USERNAME FOR THE NEXT WINDOW
            global username
            username = entry_for_username.get()

            #IF ALL THE BOXES ARE FILLED, OPEN THE DATABASE
            conn = sqlite3.connect('Essentials_Hub_Database.db')
            curs = conn.cursor()

            #GET THE PASSWORD BASED FROM THE USERNAME GIVEN
            curs.execute('select password from Users_Information where username = :username',{
                        'username': entry_for_username.get()})
            password = curs.fetchall()

            #GET THE ACCOUNT TYPE BASED FROM THE USERNAME GIVEN
            curs.execute('select AccountType from Users_Information where username = :username',{
                        'username': entry_for_username.get()})
            account_type = curs.fetchall()

            
            #CHECK IF PASSWORD IS CORRECT
            try:
                if password[0][0] == entry_for_password.get():
                    try:
                        if account_type[0][0] == 'Admin' and variable_for_sign_in_as_admin.get() == 1:
                            sign_in_as_admin()
                            #THIS IS TO DESTROY THE MAIN LOGIN WINDOW
                            main_window.destroy()
                        elif account_type[0][0] =='Admin' and variable_for_sign_in_as_admin.get() == 0:
                            sign_in_as_guest()
                            #THIS IS TO DESTROY THE MAIN LOGIN WINDOW
                            main_window.destroy()
                        elif account_type[0][0] == 'Not Admin' and variable_for_sign_in_as_admin.get() ==0:
                            sign_in_as_guest()
                            #THIS IS TO DESTROY THE MAIN LOGIN WINDOW
                            main_window.destroy()
                        else:
                            messagebox.showerror('ERROR!', 'Account does not have admin priveledges!', parent = main_window)
                    except:
                        messagebox.showerror('ERROR!', 'Account does not have admin priveledges!', parent = main_window)
                else:
                    messagebox.showerror('ERROR!', 'Incorrect Username or Password, try again.', parent = main_window)
            except:
                messagebox.showerror('ERROR!', 'Incorrect Username or Password, try again.', parent = main_window)


            entry_for_username.delete(0, END)
            entry_for_password.delete(0, END)

def sign_in_as_guest():
    

    global sign_in_as_guest_window
    sign_in_as_guest_window = Toplevel(root)
    sign_in_as_guest_window.geometry('1300x750+100+50')

    main_frame_sign_in_as_guest_window = Frame(sign_in_as_guest_window)
    main_frame_sign_in_as_guest_window.pack()

    canvas_sign_in_as_guest_window = Canvas( main_frame_sign_in_as_guest_window, width = 1300, height = 750)
    canvas_sign_in_as_guest_window.pack()
    canvas_sign_in_as_guest_window.create_image(0,0, anchor = NW, image = image_sign_in_as_guest_cover)

    frame_above_canvas_top_part = Frame(main_frame_sign_in_as_guest_window, bg = '#020202')
    canvas_sign_in_as_guest_window.create_window(74, 33, anchor = NW, window = frame_above_canvas_top_part)

    frame_above_canvas_bottom_part = Frame(main_frame_sign_in_as_guest_window, bg = '#020202')
    canvas_sign_in_as_guest_window.create_window(370, 685, anchor = NW, window = frame_above_canvas_bottom_part)

    #LABEL FOR WELCOMING USER   
    label_for_welcoming_user = Label(frame_above_canvas_top_part, text = f'Welcome to Essentials Hub, {username}!', bg = 'Black', fg = '#e99314', font = font_for_welcoming_user)
    label_for_welcoming_user.grid(row = 0, column = 0)

    #BUTTON FOR LOGOUT
    button_for_logout = Button(frame_above_canvas_top_part, text = 'Logout', font =font_for_sign_in_sign_up, bg = 'black', fg = 'white', command = logout)
    button_for_logout.grid(row = 0, column = 1, ipadx = 10, ipady = 4, padx = (875,0))

    button_for_online_shop = Button(frame_above_canvas_bottom_part, text = 'Online Shop', font =font_for_sign_in_sign_up, bg = 'black', fg = 'white')
    button_for_online_shop.grid(row = 0, column = 0, ipadx = 7, ipady = 3)

    button_for_facts_statistics = Button(frame_above_canvas_bottom_part, text = 'Facts & Statistics', font =font_for_sign_in_sign_up, bg = 'black', fg = 'white')
    button_for_facts_statistics.grid(row = 0, column = 1, ipadx = 7, ipady = 3, padx=(40,0))

    button_for_blog_section = Button(frame_above_canvas_bottom_part, text = 'Blog Section', font =font_for_sign_in_sign_up, bg = 'black', fg = 'white')
    button_for_blog_section.grid(row = 0, column = 2, ipadx = 7, ipady = 3, padx=(40,0))

    button_for_about_us = Button(frame_above_canvas_bottom_part, text = 'About Us', font =font_for_sign_in_sign_up, bg = 'black', fg = 'white')
    button_for_about_us.grid(row = 0, column = 3, ipadx = 7, ipady = 3, padx=(60,0))

def logout():
    sign_in_as_guest_window.destroy()
    main_login_window()


def forgot_password():

    #THIS IS TO DESTROY THE MAIN LOGIN WINDOW
    main_window.destroy()

    global forgot_password_window
    forgot_password_window = Toplevel(root)
    forgot_password_window.geometry('1300x750+100+50')
    main_frame = Frame(forgot_password_window)
    main_frame.pack()

    canvas_forgot_password = Canvas(main_frame, width = 1300, height = 750)
    canvas_forgot_password.pack()
    canvas_forgot_password.create_image(0,0, anchor = NW, image = image_forgot_password_1)

    frame_above_canvas = Frame(forgot_password_window, bg = 'Black')
    canvas_forgot_password.create_window(150,325, anchor =NW, window = frame_above_canvas)

    global firstclick_username_forgot_pw_1
    firstclick_username_forgot_pw_1 = True

    frame_above_frame_of_canvas_top = Frame(frame_above_canvas, bg = 'black')
    frame_above_frame_of_canvas_top.grid(row = 0, column = 0)

    frame_above_frame_of_canvas_bottom = Frame(frame_above_canvas, bg = 'black')
    frame_above_frame_of_canvas_bottom.grid(row = 1, column = 0)

    global entry_for_username_forgot_password
    entry_for_username_forgot_password = Entry(frame_above_frame_of_canvas_top, width = 34, font = font_for_username_and_password, bg = 'black', highlightbackground = 'white', fg = 'white', highlightthickness = 0.5, highlightcolor ='white')
    entry_for_username_forgot_password.insert(0, ' Username')
    entry_for_username_forgot_password.bind('<FocusIn>', on_entry_click_username_forgot_pw_1)
    entry_for_username_forgot_password.grid(row = 0, column = 0, pady = 13, ipady =13)

    button_for_submit = Button(frame_above_frame_of_canvas_bottom, text = 'Submit', font =font_for_sign_in_sign_up, bg = '#e99314', fg = 'Black', command = submit_forgot_pw)
    button_for_submit.grid(row = 0, column = 0, pady = 5, ipady = 11, ipadx = 63, sticky =W)

    button_for_go_back = Button(frame_above_frame_of_canvas_bottom, text = 'Go Back', font = font_for_sign_in_sign_up, bg = 'black', fg = '#e99314', borderwidth = 1.5, command = forgot_password_first_page_go_back)
    button_for_go_back.grid(row = 0, column = 1, pady =5, ipady = 11, ipadx = 63, sticky =W)

    #I NEED THIS PART IN ORDER TO NOT RUN THE entry_for_username_forgot_password.get() when i destroy the window in going back
    global state_of_username
    state_of_username = True

def on_entry_click_username_forgot_pw_1(event):
    global firstclick_username_forgot_pw_1
    if firstclick_username_forgot_pw_1:
        firstclick_username_forgot_pw_1 = False
        entry_for_username_forgot_password.delete(0, 'end') 

def forgot_password_first_page_go_back():
    forgot_password_window.destroy()
    main_login_window()

def submit_forgot_pw():

    if entry_for_username_forgot_password.get() == '':
            messagebox.showerror('ERROR!', 'Please fill the  username box!', parent = forgot_password_window)

    else:
        conn = sqlite3.connect('Essentials_Hub_Database.db')
        curs = conn.cursor()
        curs.execute('select username from Users_Information where username = :username',{
                            'username': entry_for_username_forgot_password.get()})
        username = curs.fetchall()

        try:
            if username[0][0] == entry_for_username_forgot_password.get():
                forgot_pw_second_page()
                forgot_password_window.destroy()
        except:
            messagebox.showerror('ERROR!', 'Invalid Username, try again', parent = forgot_password_window)

def forgot_pw_second_page():

    #I NEED THIS PART IN ORDER TO NOT RUN THE entry_for_username_forgot_password.get() when i destroy the window in going back
    while state_of_username:
        global username_for_forgot_pw
        username_for_forgot_pw = entry_for_username_forgot_password.get()
        break
        
    #THIS IS TO GET THE SECURITY QUESTION AND PUT IT IN THE LABEL
    conn = sqlite3.connect('Essentials_Hub_Database.db')
    curs = conn.cursor()

    curs.execute('select SecurityQuestion from Users_Information where username = :username',{
                    'username': username_for_forgot_pw})
    security_question = curs.fetchall()


    #THIS IS FOR ANOTHER WINDOW
    global forgot_password_second_window
    forgot_password_second_window = Toplevel(root)
    forgot_password_second_window.geometry('1300x750+100+50')
    main_frame = Frame(forgot_password_second_window)
    main_frame.pack()

    canvas_forgot_password = Canvas(main_frame, width = 1300, height = 750)
    canvas_forgot_password.pack()
    canvas_forgot_password.create_image(0,0, anchor = NW, image = image_forgot_password_2)

    frame_above_canvas = Frame(forgot_password_second_window, bg = 'Black')
    canvas_forgot_password.create_window(150,325, anchor =NW, window = frame_above_canvas)

    global firstclick_username_forgot_pw_2
    firstclick_username_forgot_pw_2 = True
    
    frame_above_frame_of_canvas_top = Frame(frame_above_canvas, bg = 'black')
    frame_above_frame_of_canvas_top.grid(row = 0, column = 0)

    frame_above_frame_of_canvas_middle = Frame(frame_above_canvas, bg = 'black')
    frame_above_frame_of_canvas_middle.grid(row = 1, column = 0)
    
    frame_above_frame_of_canvas_bottom = Frame(frame_above_canvas, bg = 'black')
    frame_above_frame_of_canvas_bottom.grid(row = 2, column = 0)
    
    label_for_security_question = Label(frame_above_frame_of_canvas_top, text = security_question[0][0], font = font_for_forgot_pw_security_question, bg = 'Black', fg = 'white' )
    label_for_security_question.grid(row = 0, column = 0)

    global entry_for_security_question_answer_forgot_password
    entry_for_security_question_answer_forgot_password = Entry(frame_above_frame_of_canvas_middle, width = 34, font = font_for_username_and_password, bg = 'black', highlightbackground = 'white', fg = 'white', highlightthickness = 0.5, highlightcolor ='white')
    entry_for_security_question_answer_forgot_password.insert(0, ' Answer')
    entry_for_security_question_answer_forgot_password.bind('<FocusIn>', on_entry_click_username_forgot_pw_2)
    entry_for_security_question_answer_forgot_password.grid(row = 0, column = 0, pady = 13, ipady =13)

    button_for_submit = Button(frame_above_frame_of_canvas_bottom, text = 'Submit', font =font_for_sign_in_sign_up, bg = '#e99314', fg = 'Black', command = submit_forgot_pw_for_security_question)
    button_for_submit.grid(row = 0, column = 0, pady = 5, ipady = 11, ipadx = 63, sticky =W)

    button_for_go_back = Button(frame_above_frame_of_canvas_bottom, text = 'Go Back', font = font_for_sign_in_sign_up, bg = 'black', fg = '#e99314', borderwidth = 1.5, command = forgot_password_second_page_go_back)
    button_for_go_back.grid(row = 0, column = 1, pady =5, ipady = 11, ipadx = 63, sticky =W)

def forgot_password_second_page_go_back():
    forgot_password_second_window.destroy()
    forgot_password()


def submit_forgot_pw_for_security_question():
    if entry_for_security_question_answer_forgot_password.get() == '':
            messagebox.showerror('ERROR!', 'Please fill the answer box!', parent = forgot_password_second_window)

    else:
        conn = sqlite3.connect('Essentials_Hub_Database.db')
        curs = conn.cursor()
        curs.execute('select SecurityQuestionAnswer from Users_Information where username = :username',{
                    'username': username_for_forgot_pw})
        security_question_answer = curs.fetchall()

        try:
            if security_question_answer[0][0] == entry_for_security_question_answer_forgot_password.get():
                get_code_then_send_to_email()
                forgot_password_second_window.destroy()

        except:
            messagebox.showerror('ERROR!', 'Incorrect Answer, try again', parent = forgot_password_second_window)


def on_entry_click_username_forgot_pw_2(event):
    global firstclick_username_forgot_pw_2
    if firstclick_username_forgot_pw_2:
        firstclick_username_forgot_pw_2 = False
        entry_for_security_question_answer_forgot_password.delete(0, 'end') 


def get_code_then_send_to_email():
    
    #THIS IS FOR GENERATING THE RANDOM CODE
    letters = string.ascii_uppercase
    lst = []
    for i in range(7):
        lst.append(random.choice(letters))
    
    global random_code
    random_code = ''.join(lst)

    global username_for_forgot_pw
    

    #THIS IS FOR ME TO GET THE EMAIL WHERE I CAN SEND THE CODE
    conn = sqlite3.connect('Essentials_Hub_Database.db')
    curs = conn.cursor()
    curs.execute('select email from Users_Information where username = :username',{
                'username': username_for_forgot_pw})
    email = curs.fetchall()

    #THIS IS FOR ME TO SEND THE CODE TOTHE EMAIL OF USER
    email_sender = 'essentialshubofficial@gmail.com'
    email_password = '!1EssentialsHub'
    email_receiver = email[0][0]
    message = f'The verification code is {random_code}'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_sender, email_password)
    server.sendmail(email_sender,email_receiver,message)
    server.close()

    forgot_pw_third_page()


def forgot_pw_third_page():

    global forgot_password_third_window
    forgot_password_third_window = Toplevel(root)
    forgot_password_third_window.geometry('1300x750+100+50')
    main_frame = Frame(forgot_password_third_window)
    main_frame.pack()

    canvas_forgot_password = Canvas(main_frame, width = 1300, height = 750)
    canvas_forgot_password.pack()
    canvas_forgot_password.create_image(0,0, anchor = NW, image = image_forgot_password_3)

    frame_above_canvas = Frame(forgot_password_third_window, bg = 'Black')
    canvas_forgot_password.create_window(150,325, anchor =NW, window = frame_above_canvas)

    global firstclick_username_forgot_pw_3
    firstclick_username_forgot_pw_3 = True

    frame_above_frame_of_canvas_top = Frame(frame_above_canvas, bg = 'black')
    frame_above_frame_of_canvas_top.grid(row = 0, column = 0)

    frame_above_frame_of_canvas_bottom = Frame(frame_above_canvas, bg = 'black')
    frame_above_frame_of_canvas_bottom.grid(row = 1, column = 0)

    global entry_for_code_forgot_password
    entry_for_code_forgot_password = Entry(frame_above_frame_of_canvas_top, width = 34, font = font_for_username_and_password, bg = 'black', highlightbackground = 'white', fg = 'white', highlightthickness = 0.5, highlightcolor ='white')
    entry_for_code_forgot_password.insert(0, ' Verification Code')
    entry_for_code_forgot_password.bind('<FocusIn>', on_entry_click_username_forgot_pw_3)
    entry_for_code_forgot_password.grid(row = 0, column = 0, pady = 13, ipady =13)

    button_for_submit = Button(frame_above_frame_of_canvas_bottom, text = 'Submit', font =font_for_sign_in_sign_up, bg = '#e99314', fg = 'Black', command = check_the_random_code)
    button_for_submit.grid(row = 0, column = 0, pady = 5, ipady = 11, ipadx = 63, sticky =W)

    button_for_go_back = Button(frame_above_frame_of_canvas_bottom, text = 'Go Back', font = font_for_sign_in_sign_up, bg = 'black', fg = '#e99314', borderwidth = 1.5, command = forgot_password_third_page_go_back)
    button_for_go_back.grid(row = 0, column = 1, pady =5, ipady = 11, ipadx = 63, sticky =W)


def forgot_password_third_page_go_back():
    global state_of_username
    state_of_username = False
    forgot_password_third_window.destroy()
    forgot_pw_second_page()


def on_entry_click_username_forgot_pw_3(event):
    global firstclick_username_forgot_pw_3
    if firstclick_username_forgot_pw_3:
        firstclick_username_forgot_pw_3 = False
        entry_for_code_forgot_password.delete(0, 'end')


def check_the_random_code():
    if random_code == entry_for_code_forgot_password.get():
        forgot_pw_fourth_page()
        forgot_password_third_window.destroy()

    
    else:
        messagebox.showerror('ERROR!', 'Incorrect verification code, try again', parent = forgot_password_third_window)

def forgot_pw_fourth_page():

    global forgot_password_fourth_window
    forgot_password_fourth_window = Toplevel(root)
    forgot_password_fourth_window.geometry('1300x750+100+50')
    main_frame = Frame(forgot_password_fourth_window)
    main_frame.pack()

    canvas_forgot_password = Canvas(main_frame, width = 1300, height = 750)
    canvas_forgot_password.pack()
    canvas_forgot_password.create_image(0,0, anchor = NW, image = image_forgot_password_4)

    frame_above_canvas = Frame(forgot_password_fourth_window, bg = 'Black')
    canvas_forgot_password.create_window(150,325, anchor =NW, window = frame_above_canvas)

    global firstclick_username_forgot_pw_4
    firstclick_username_forgot_pw_4 = True
    global firstclick_username_forgot_pw_5
    firstclick_username_forgot_pw_5 = True

    frame_above_frame_of_canvas_top = Frame(frame_above_canvas, bg = 'black')
    frame_above_frame_of_canvas_top.grid(row = 0, column = 0)

    frame_above_frame_of_canvas_bottom = Frame(frame_above_canvas, bg = 'black')
    frame_above_frame_of_canvas_bottom.grid(row = 1, column = 0)

    global entry_for_new_pw_forgot_password
    entry_for_new_pw_forgot_password = Entry(frame_above_frame_of_canvas_top, width = 34, font = font_for_username_and_password, bg = 'black', highlightbackground = 'white', fg = 'white', highlightthickness = 0.5, highlightcolor ='white')
    entry_for_new_pw_forgot_password.insert(0, ' New Password')
    entry_for_new_pw_forgot_password.bind('<FocusIn>', on_entry_click_username_forgot_pw_4)
    entry_for_new_pw_forgot_password.grid(row = 0, column = 0, pady = 13, ipady =13)

    global entry_for_confirm_pw_forgot_password
    entry_for_confirm_pw_forgot_password = Entry(frame_above_frame_of_canvas_top, width = 34, font = font_for_username_and_password, bg = 'black', highlightbackground = 'white', fg = 'white', highlightthickness = 0.5, highlightcolor ='white')
    entry_for_confirm_pw_forgot_password.insert(0, ' Confirm New Password')
    entry_for_confirm_pw_forgot_password.bind('<FocusIn>', on_entry_click_username_forgot_pw_5)
    entry_for_confirm_pw_forgot_password.grid(row = 1, column = 0, pady = 13, ipady =13)

    button_for_submit = Button(frame_above_frame_of_canvas_bottom, text = 'Submit', font =font_for_sign_in_sign_up, bg = '#e99314', fg = 'Black', command = update_pw_in_forgot_pw)
    button_for_submit.grid(row = 0, column = 0, pady = 5, ipady = 11, ipadx = 63, sticky =W)

    button_for_go_back = Button(frame_above_frame_of_canvas_bottom, text = 'Go Back', font = font_for_sign_in_sign_up, bg = 'black', fg = '#e99314', borderwidth = 1.5, command = forgot_password_fourth_page_go_back)
    button_for_go_back.grid(row = 0, column = 1, pady =5, ipady = 11, ipadx = 63, sticky =W)


def forgot_password_fourth_page_go_back():
    forgot_password_fourth_window.destroy
    forgot_pw_third_page()

def on_entry_click_username_forgot_pw_4(event):
    global firstclick_username_forgot_pw_4
    if firstclick_username_forgot_pw_4:
        firstclick_username_forgot_pw_4 = False
        entry_for_new_pw_forgot_password.delete(0, 'end')
        entry_for_new_pw_forgot_password.config(show = '*')


def on_entry_click_username_forgot_pw_5(event):
    global firstclick_username_forgot_pw_5
    if firstclick_username_forgot_pw_5:
        firstclick_username_forgot_pw_5 = False
        entry_for_confirm_pw_forgot_password.delete(0, 'end')
        entry_for_confirm_pw_forgot_password.config(show = '*')


def update_pw_in_forgot_pw():
    
    if entry_for_new_pw_forgot_password.get() == entry_for_confirm_pw_forgot_password.get():
        global new_pw
        new_pw = entry_for_confirm_pw_forgot_password.get()
        # forgot_password_fourth_window.destroy()

        conn = sqlite3.connect('Essentials_Hub_Database.db')
        curs = conn.cursor()
        curs.execute('update Users_Information set password = :password where username = :username', {
        'password': new_pw,
        'username': username_for_forgot_pw})
        conn.commit()
        
        messagebox.showinfo('SUCCESS!', 'Password has been reset!', parent = forgot_password_fourth_window)

    else: 
         messagebox.showerror('ERROR!', 'Password do not match, try again', parent = forgot_password_fourth_window)


def sign_up():

    #THIS IS TO DESTROY THE MAIN LOGIN WINDOW
    main_window.destroy()

    #THIS IS TO DETERMINE IF IF USER WANTS ADMIN PROVELEDGES OR NOT, BECOMES FALSE WHEN USER CLICKED SIGN-UP AS GUEST
    global admin_or_not
    admin_or_not = True

    global sign_up_window
    sign_up_window = Toplevel(root)
    sign_up_window.geometry('1300x750+100+50')

    main_frame_sign_up_window = Frame(sign_up_window)
    main_frame_sign_up_window.pack()

    canvas_sign_up_window = Canvas(main_frame_sign_up_window, width = 1300, height = 750)
    canvas_sign_up_window.pack()
    canvas_sign_up_window.create_image(0,0, anchor = NW, image = image_sign_up_window)

    frame_above_sign_up_canvas_1 = Frame(sign_up_window, bg = 'Black')
    canvas_sign_up_window.create_window(100,475, anchor =NW, window = frame_above_sign_up_canvas_1)

    frame_above_sign_up_canvas_2 = Frame(sign_up_window, bg = 'Black')
    canvas_sign_up_window.create_window(100,560, anchor =NW, window = frame_above_sign_up_canvas_2)

    frame_above_sign_up_canvas_3 = Frame(sign_up_window, bg = 'Black')
    canvas_sign_up_window.create_window(100,645, anchor =NW, window = frame_above_sign_up_canvas_3)

    #THESE ARE THE BUTTONS FOR SIGN UP AS GUEST AND SIGN UP AS ADMIN
    button_for_sign_up_as_guest = Button(frame_above_sign_up_canvas_1, text = 'Sign Up as Guest', font =font_for_sign_up_as_guest, bg = '#e99314', fg = 'Black', command = sign_up_as_guest)
    button_for_sign_up_as_guest.grid(row = 0, column = 0, ipady = 11, ipadx = 90, sticky = W)

    button_for_sign_up_as_admin = Button(frame_above_sign_up_canvas_2, text = 'Sign Up as Admin', font =font_for_sign_up_as_guest, bg = '#363636', fg = 'White', command = sign_up_as_admin)
    button_for_sign_up_as_admin.grid(row = 0, column = 0, ipady = 11, ipadx = 90, sticky = W)

    button_for_sign_in_instead = Button(frame_above_sign_up_canvas_3, text = 'Go Back', font =font_for_sign_up_as_guest, bg = 'white', fg = 'black', command = go_back_to_sign_in)
    button_for_sign_in_instead.grid(row = 0, column = 0, ipady = 11, ipadx = 129, sticky = W)

#< GO BACK TO THE SIGN IN WINDOW
def go_back_to_sign_in():
    sign_up_window.destroy()
    main_login_window()
#>

def sign_up_as_guest():
    
    #THIS IS FOR ME TO KNOW IF THE ACCOUNT IS ADMIN TYPE OR NOT
    global admin_or_not
    admin_or_not = False

    #close the sign up main page
    sign_up_window.destroy()

    #Set up new window for the guest sign up
    global sign_up_as_guest_window
    sign_up_as_guest_window = Toplevel(root)
    sign_up_as_guest_window.geometry('1300x750+100+50')

    main_frame_sign_up_as_guest_window = Frame(sign_up_as_guest_window)
    main_frame_sign_up_as_guest_window.pack()

    canvas_sign_up_as_guest_window = Canvas(main_frame_sign_up_as_guest_window, width = 1300, height = 750)
    canvas_sign_up_as_guest_window.pack()
    canvas_sign_up_as_guest_window.create_image(0,0, anchor = NW, image = image_sign_up_as_guest_window)

    frame_above_sign_up_as_guest_canvas = Frame(main_frame_sign_up_as_guest_window, bg = 'Black')
    canvas_sign_up_as_guest_window.create_window(70,180, anchor =NW, window = frame_above_sign_up_as_guest_canvas)

    frame_above_sign_up_as_guest_canvas_bottom = Frame(main_frame_sign_up_as_guest_window, bg = 'Black')
    canvas_sign_up_as_guest_window.create_window(70,610, anchor =NW, window = frame_above_sign_up_as_guest_canvas_bottom)

    #THESE ARE FOR THE LABELS FOR THE SIGN UP AS GUEST
    label_fname = Label(frame_above_sign_up_as_guest_canvas, font = font_for_sign_up_as_guest, bg = 'Black', fg = 'White',text = 'First Name')
    label_fname.grid(row = 0, column = 0, padx = (45,40), sticky = W, pady = 10)

    label_lname = Label(frame_above_sign_up_as_guest_canvas, font = font_for_sign_up_as_guest, bg = 'Black', fg = 'White', text = 'Last Name')
    label_lname.grid(row = 1, column = 0, padx = (45,40), sticky = W, pady =10)

    label_email = Label(frame_above_sign_up_as_guest_canvas, font = font_for_sign_up_as_guest, bg = 'Black', fg = 'White', text = 'Email')
    label_email.grid(row = 2, column = 0, padx = (45,40), sticky = W, pady =10)
    
    label_username = Label(frame_above_sign_up_as_guest_canvas, font = font_for_sign_up_as_guest, bg = 'Black', fg = 'White', text = 'Username')
    label_username.grid(row = 3, column = 0, padx = (45,40), sticky = W, pady =10)

    label_password = Label(frame_above_sign_up_as_guest_canvas, font = font_for_sign_up_as_guest, bg = 'Black', fg = 'White', text = 'Password')
    label_password.grid(row = 4, column = 0,padx = (45,40), sticky = W, pady =10)

    #THESE ARE THE ENTRY WIDGETS FOR THE SIGN UP AS GUEST
    global entry_fname
    entry_fname = Entry(frame_above_sign_up_as_guest_canvas, font = font_for_sign_in_entry,width = 18, borderwidth =1, bg = 'Black', fg = 'White' )
    entry_fname.grid(row = 0, column = 1, sticky = W+E, ipady = 3, pady = 10, padx =13)

    global entry_lname
    entry_lname= Entry(frame_above_sign_up_as_guest_canvas, font = font_for_sign_in_entry, width = 18 ,borderwidth =1, bg = 'Black', fg = 'White' )
    entry_lname.grid(row =1, column = 1, sticky = W+E, ipady = 3, pady =10, padx =13)

    global entry_email
    entry_email = Entry(frame_above_sign_up_as_guest_canvas, font = font_for_sign_in_entry, width = 18 ,borderwidth =1, bg = 'Black', fg = 'White' )
    entry_email.grid(row =2, column = 1, sticky = W+E, ipady = 3, pady =10, padx =13)

    global entry_username
    entry_username = Entry(frame_above_sign_up_as_guest_canvas, font = font_for_sign_in_entry, width = 18 ,borderwidth =1, bg = 'Black', fg = 'White' )
    entry_username.grid(row =3, column = 1, sticky = W+E, ipady = 3, pady =10, padx =13)

    global entry_password
    entry_password = Entry(frame_above_sign_up_as_guest_canvas, show = '*', font = font_for_sign_in_entry, width = 18 ,borderwidth =1, bg = 'Black', fg = 'White' )
    entry_password.grid(row =4, column = 1, sticky = W+E, ipady = 3, pady =10, padx =13)

    #THIS IS THE LABEL FOR THE SECURITY QUESTION
    label_security_question = Label(frame_above_sign_up_as_guest_canvas, font = font_for_sign_up_as_guest, bg = 'Black', fg = 'White', text = 'Security Question:')
    label_security_question.grid(row = 5, column = 0, columnspan =2,padx = (45,40), sticky = W, pady =10)

    #THIS IS THE OPTION MENU
    global variable_for_option_menu
    variable_for_option_menu = StringVar()
    variable_for_option_menu.set('What is the name of your first Pet?')

    option_menu_for_security_questions = OptionMenu(frame_above_sign_up_as_guest_canvas, variable_for_option_menu, 'What is the name of your first Pet?', 'Who is you favorite artist?', 'What is the middle name of your mother?', 'What elementary school did you attend?', 'In what town or city did your mother and father meet?', 'In what town or city was your first full time job?')
    option_menu_for_security_questions.config(bg = 'Black', fg = 'White', highlightbackground = 'black', highlightcolor = 'black', font = font_for_option_menu)
    option_menu_for_security_questions.grid(row = 6, column = 0, columnspan = 2, ipadx = 10, ipady = 7, padx = 5, pady = 10)
    
    #THIS IS THE LABEL FOR THE ANSWER IN SECURITY QUESTION
    label_security_question_answer = Label(frame_above_sign_up_as_guest_canvas, font = font_for_sign_up_as_guest, bg = 'Black', fg = 'White', text = 'Answer')
    label_security_question_answer.grid(row = 7, column = 0,padx = (45,40), sticky = W, pady =10)
    
    #THIS IS FOR THE ENTRY OF THE SECURITY QUESTION ANSWER
    global entry_security_question
    entry_security_question = Entry(frame_above_sign_up_as_guest_canvas, font = font_for_sign_in_entry, width = 18 ,borderwidth =1, bg = 'Black', fg = 'White' )
    entry_security_question.grid(row =7, column = 1, sticky = W+E, ipady = 3, pady =10, padx =13)
    
    #THESE ARE FOR THE BUTTONS BELOW
    button_submit_sign_up_as_guest = Button(frame_above_sign_up_as_guest_canvas_bottom, text = 'Sign Up!', bg = '#e99314', fg = 'black', font = font_for_option_menu, command = submit_sign_up)
    button_submit_sign_up_as_guest.grid(row = 0, column = 0, ipady = 9, ipadx = 40, padx = (50,0), sticky = W+E)

    button_back_sign_up_as_guest = Button(frame_above_sign_up_as_guest_canvas_bottom, text = 'Back', bg = '#363636', fg = 'white', font = font_for_option_menu, command = back_sign_up_as_guest)
    button_back_sign_up_as_guest.grid(row = 0, column = 1, ipady = 9, ipadx = 40, padx = (10,50), sticky = W+E)


def back_sign_up_as_guest():
    sign_up_as_guest_window.destroy()
    sign_up()


def sign_up_as_admin():

    #close the sign up main page
    sign_up_window.destroy()

    #Set up new window for the guest sign up
    global sign_up_as_admin_window
    sign_up_as_admin_window = Toplevel(root)
    sign_up_as_admin_window.geometry('1300x750+100+50')

    main_frame_sign_up_as_admin_window = Frame(sign_up_as_admin_window)
    main_frame_sign_up_as_admin_window.pack()

    canvas_sign_up_as_admin_window = Canvas(main_frame_sign_up_as_admin_window, width = 1300, height = 750)
    canvas_sign_up_as_admin_window.pack()
    canvas_sign_up_as_admin_window.create_image(0,0, anchor = NW, image = image_sign_up_as_admin_window)

    frame_above_sign_up_as_admin_canvas = Frame(main_frame_sign_up_as_admin_window, bg = 'Black')
    canvas_sign_up_as_admin_window.create_window(750,180, anchor =NW, window = frame_above_sign_up_as_admin_canvas)

    frame_above_sign_up_as_admin_canvas_bottom = Frame(main_frame_sign_up_as_admin_window, bg = 'Black')
    canvas_sign_up_as_admin_window.create_window(750,610, anchor =NW, window = frame_above_sign_up_as_admin_canvas_bottom)

    #THESE ARE FOR THE LABELS FOR THE SIGN UP AS GUEST
    label_fname = Label(frame_above_sign_up_as_admin_canvas, font = font_for_sign_up_as_guest, bg = 'Black', fg = 'White',text = 'First Name')
    label_fname.grid(row = 0, column = 0, padx = (45,40), sticky = W, pady = 10)

    label_lname = Label(frame_above_sign_up_as_admin_canvas, font = font_for_sign_up_as_guest, bg = 'Black', fg = 'White', text = 'Last Name')
    label_lname.grid(row = 1, column = 0, padx = (45,40), sticky = W, pady =10)

    label_email = Label(frame_above_sign_up_as_admin_canvas, font = font_for_sign_up_as_guest, bg = 'Black', fg = 'White', text = 'Email')
    label_email.grid(row = 2, column = 0, padx = (45,40), sticky = W, pady =10)
    
    label_username = Label(frame_above_sign_up_as_admin_canvas, font = font_for_sign_up_as_guest, bg = 'Black', fg = 'White', text = 'Username')
    label_username.grid(row = 3, column = 0, padx = (45,40), sticky = W, pady =10)

    label_password = Label(frame_above_sign_up_as_admin_canvas, font = font_for_sign_up_as_guest, bg = 'Black', fg = 'White', text = 'Password')
    label_password.grid(row = 4, column = 0,padx = (45,40), sticky = W, pady =10)

    #THESE ARE THE ENTRY WIDGETS FOR THE SIGN UP AS GUEST
    global entry_fname
    entry_fname = Entry(frame_above_sign_up_as_admin_canvas, font = font_for_sign_in_entry,width = 18, borderwidth =1, bg = 'Black', fg = 'White' )
    entry_fname.grid(row = 0, column = 1, sticky = W+E, ipady = 3, pady = 10, padx =13)

    global entry_lname
    entry_lname = Entry(frame_above_sign_up_as_admin_canvas, font = font_for_sign_in_entry, width = 18 ,borderwidth =1, bg = 'Black', fg = 'White' )
    entry_lname.grid(row =1, column = 1, sticky = W+E, ipady = 3, pady =10, padx =13)

    global entry_email
    entry_email= Entry(frame_above_sign_up_as_admin_canvas, font = font_for_sign_in_entry, width = 18 ,borderwidth =1, bg = 'Black', fg = 'White' )
    entry_email.grid(row =2, column = 1, sticky = W+E, ipady = 3, pady =10, padx =13)

    global entry_username
    entry_username = Entry(frame_above_sign_up_as_admin_canvas, font = font_for_sign_in_entry, width = 18 ,borderwidth =1, bg = 'Black', fg = 'White' )
    entry_username.grid(row =3, column = 1, sticky = W+E, ipady = 3, pady =10, padx =13)

    global entry_password
    entry_password = Entry(frame_above_sign_up_as_admin_canvas, show = '*', font = font_for_sign_in_entry, width = 18 ,borderwidth =1, bg = 'Black', fg = 'White' )
    entry_password.grid(row =4, column = 1, sticky = W+E, ipady = 3, pady =10, padx =13)

    #THIS IS THE LABEL FOR THE SECURITY QUESTION
    label_security_question = Label(frame_above_sign_up_as_admin_canvas, font = font_for_sign_up_as_guest, bg = 'Black', fg = 'White', text = 'Security Question:')
    label_security_question.grid(row = 5, column = 0, columnspan =2,padx = (45,40), sticky = W, pady =10)

    #THIS IS THE OPTION MENU
    global variable_for_option_menu
    variable_for_option_menu = StringVar()
    variable_for_option_menu.set('What is the name of your first Pet?')

    option_menu_for_security_questions = OptionMenu(frame_above_sign_up_as_admin_canvas, variable_for_option_menu, 'What is the name of your first Pet?', 'Who is you favorite artist?', 'What is the middle name of your mother?', 'What elementary school did you attend?', 'In what town or city did your mother and father meet?', 'In what town or city was your first full time job?')
    option_menu_for_security_questions.config(bg = 'Black', fg = 'White', highlightbackground = 'black', highlightcolor = 'black', font = font_for_option_menu)
    option_menu_for_security_questions.grid(row = 6, column = 0, columnspan = 2, ipadx = 10, ipady = 7, padx = 5, pady = 10)
    
    #THIS IS THE LABEL FOR THE ANSWER IN SECURITY QUESTION
    label_security_question_answer = Label(frame_above_sign_up_as_admin_canvas, font = font_for_sign_up_as_guest, bg = 'Black', fg = 'White', text = 'Answer')
    label_security_question_answer.grid(row = 7, column = 0,padx = (45,40), sticky = W, pady =10)
    
    #THIS IS FOR THE ENTRY OF THE SECURITY QUESTION ANSWER
    global entry_security_question
    entry_security_question = Entry(frame_above_sign_up_as_admin_canvas, font = font_for_sign_in_entry, width = 18 ,borderwidth =1, bg = 'Black', fg = 'White' )
    entry_security_question.grid(row =7, column = 1, sticky = W+E, ipady = 3, pady =10, padx =13)
    
    #THESE ARE FOR THE BUTTONS BELOW
    button_submit_sign_up_as_admin = Button(frame_above_sign_up_as_admin_canvas_bottom, text = 'Sign Up!', bg = '#e99314', fg = 'black', font = font_for_option_menu, command = submit_sign_up)
    button_submit_sign_up_as_admin.grid(row = 0, column = 0, ipady = 9, ipadx = 40, padx = (50,0), sticky = W+E)

    button_back_sign_up_as_admin = Button(frame_above_sign_up_as_admin_canvas_bottom, text = 'Back', bg = '#363636', fg = 'white', font = font_for_option_menu, command = back_sign_up_as_admin)
    button_back_sign_up_as_admin.grid(row = 0, column = 1, ipady = 9, ipadx = 40, padx = (10,50), sticky = W+E)


def submit_sign_up():

    #THIS IS TO CHECK IF THE ACCOUNT IS ADMIN OR NOT
    if admin_or_not:
        admin_status = 'Admin'
    else:
        admin_status = 'Not Admin'

    #THIS IS TO CHECK WHETHER ALL THE BOXES ARE FILLED
    if entry_lname.get() == '' or entry_fname.get() == '' or entry_email.get() == '' or entry_username.get() == '' or entry_password.get() == '' or entry_security_question.get() == '':
        
        #THE IF ELSE HERE IS NECCESSARY TO KNOW THE PARENT OF THE MESSAGE BOX
        if admin_status == 'Admin':
            messagebox.showerror('ERROR!', 'Please fill all the boxes!', parent = sign_up_as_admin_window)
        else:
            messagebox.showerror('ERROR!', 'Please fill all the boxes!', parent = sign_up_as_guest_window)

    #HERE I CREATE THE DATABASE FOR USER INFORMATION
    else:
        conn = sqlite3.connect('Essentials_Hub_Database.db')
        curs = conn.cursor()

        curs.execute("""
                    create table if not exists Users_Information(
                        FirstName text,
                        LastName text,
                        Email text,
                        Username text PRIMARY KEY,
                        Password text,
                        SecurityQuestion text,
                        SecurityQuestionAnswer text,
                        AccountType text
                    )
                    """)

        #THIS IS TO PUT ALL THE ENTRIES INTO THE DATABASE
        try:
            
            curs.execute('insert into Users_Information values (:fname, :lname, :email, :username, :password, :squestion, :squestionans, :atype)',
            {
                'fname': entry_fname.get(),
                'lname': entry_lname.get(),
                'email':entry_email.get(),
                'username': entry_username.get(),
                'password': entry_password.get(),
                'squestion': variable_for_option_menu.get(),
                'squestionans': entry_security_question.get(),
                'atype': admin_status
            })
            conn.commit()
            
            #THE IF ELSE HERE IS NECCESSARY TO KNOW THE PARENT OF THE MESSAGE BOX
            if admin_status == 'Admin':
                messagebox.showinfo('SUCCESS!', 'Sign-up complete!', parent = sign_up_as_admin_window)
                sign_up_as_admin_window.destroy
                main_login_window()
            else:
                messagebox.showinfo('SUCCESS!', 'Sign-up complete!', parent = sign_up_as_guest_window)
                sign_up_as_guest_window.destroy()
                main_login_window()
        
        #THIS IS FOR THE ERROR BOX WHEN THERE IS SIMILAR USERNAMES SINCE USERNAME IS PKEY
        except:
            if admin_status == 'Admin':
                messagebox.showerror('ERROR!', 'Username is already taken!', parent = sign_up_as_admin_window)
            else:
                messagebox.showerror('ERROR!', 'Username is already taken!', parent = sign_up_as_guest_window)
            

def back_sign_up_as_admin():
    sign_up_as_admin_window.destroy()
    sign_up()


# ======================================================START====================================================================

#THIS FOR THE LAUNCHER
root = Tk()
root.geometry('1300x500+100+50')
root.title('Welcome to Essentials Hub!')
main_frame = Frame(root)
main_frame.pack()

canvas_launcher = Canvas(main_frame, width = 1300, height = 750)
canvas_launcher.pack()
image_launcher = ImageTk.PhotoImage(Image.open('PICTURES\image_launcher.jpg'))
canvas_launcher.create_image(0,0, anchor = NW, image = image_launcher)

frame_above_canvas_left = Frame(main_frame, bg = 'Black')
canvas_launcher.create_window(375,275, anchor =NW, window = frame_above_canvas_left)

frame_above_canvas_right = Frame(main_frame, bg = 'Black')
canvas_launcher.create_window(675,275, anchor =NW, window = frame_above_canvas_right)

button_exit = Button(frame_above_canvas_right, text = 'Exit Program', bg = 'black', fg = 'white', command = exit_launcher)
button_exit.grid(row = 0, column = 0, ipady = 15, ipadx = 100, sticky = W)

button_launch = Button(frame_above_canvas_left, text = 'Login Window', bg = '#e99314', fg = 'Black', command = main_login_window)
button_launch.grid(row = 0, column = 0, ipady = 15, ipadx = 100, sticky = W)

# button_launch = Button(frame_above_canvas_left, text = 'Login Window', command = main_login_window)
# button_launch.pack()


# ======================================================IMAGES==================================================================


image_main_login_cover = ImageTk.PhotoImage(Image.open('PICTURES\image_main_cover.jpg'))

image_main_login_top_of_main_rec = ImageTk.PhotoImage(Image.open("PICTURES\image_top_of_main_cover.jpg"))

image_sign_up_window = ImageTk.PhotoImage(Image.open('PICTURES\image_second_main_cover.jpg'))

image_sign_up_as_guest_window = ImageTk.PhotoImage(Image.open('PICTURES\image_sign_up_as_guest.jpg'))

image_sign_up_as_admin_window = ImageTk.PhotoImage(Image.open('PICTURES\image_sign_up_as_admin.jpg'))

image_forgot_password_1 = ImageTk.PhotoImage(Image.open('PICTURES\image_forgot_password_1.jpg'))

image_forgot_password_2 = ImageTk.PhotoImage(Image.open('PICTURES\image_forgot_password_2.jpg'))

image_forgot_password_3 = ImageTk.PhotoImage(Image.open('PICTURES\image_forgot_password_3.jpg'))

image_forgot_password_4 = ImageTk.PhotoImage(Image.open('PICTURES\image_forgot_password_4.jpg'))

image_sign_in_as_guest_cover = ImageTk.PhotoImage(Image.open('PICTURES\image_main_page.jpg'))

# ==============================================================================================================================

# ======================================================FONTS===================================================================

font_for_username_and_password = Font(family = 'Gotham Book', size = 14)

font_for_login_check_button = Font(family = 'Gotham', size = 11)

font_for_sign_in_sign_up = Font(family = 'Gotham', size = 9)

font_for_sign_up_as_guest = Font(family = 'Gotham Book', size = 14)

font_for_the_sign_up_labels =Font(family = 'Gotham', size = 12)

font_for_sign_in_entry = Font(family = 'Gotham', size = 13)

font_for_option_menu = Font(family = 'Gotham', size = 10)

font_for_message_box = Font(family = 'Gotham', size = 12)

font_for_forgot_pw_security_question =Font(family = 'Gotham', size = 13)

font_for_welcoming_user = Font(family = 'Gotham Black', size = 10)
# ==============================================================================================================================

root.mainloop()
=======
