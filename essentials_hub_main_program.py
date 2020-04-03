
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



# ======================================================START====================================================================

#THIS FOR THE LAUNCHER
root = Tk()
root.geometry('1300x500+100+50')
root.title('Welcome to Essentials Hub!')
main_frame = Frame(root)
main_frame.pack()

canvas_launcher = Canvas(main_frame, width = 1300, height = 750)
canvas_launcher.pack()
image_launcher = ImageTk.PhotoImage(Image.open('launcher.jpg'))
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


image_main_login_cover = ImageTk.PhotoImage(Image.open('main_cover.jpg'))

image_main_login_top_of_main_rec = ImageTk.PhotoImage(Image.open('top_of_main_cover.jpg'))

image_sign_up_window = ImageTk.PhotoImage(Image.open('second_main_cover.jpg'))

image_sign_up_as_guest_window = ImageTk.PhotoImage(Image.open('sign_up_as_guest.jpg'))

image_sign_up_as_admin_window = ImageTk.PhotoImage(Image.open('sign_up_as_admin.jpg'))

image_forgot_password_1 = ImageTk.PhotoImage(Image.open('forgot_password_1.jpg'))

image_forgot_password_2 = ImageTk.PhotoImage(Image.open('forgot_password_2.jpg'))

image_forgot_password_3 = ImageTk.PhotoImage(Image.open('forgot_password_3.jpg'))

image_forgot_password_4 = ImageTk.PhotoImage(Image.open('forgot_password_4.jpg'))

image_sign_in_as_guest_cover = ImageTk.PhotoImage(Image.open('main_page.jpg'))

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
