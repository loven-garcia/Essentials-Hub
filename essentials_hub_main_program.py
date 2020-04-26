#THIS IS THE MAIN PY FILE

from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter.font import Font
import sqlite3
import smtplib
import string
import random
import final_scrape
from datetime import datetime
import pandas as pd
from pandastable import Table
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import json
import requests
# ======================================================FUNCTIONS===============================================================


def exit_launcher():
    """
    Destroy's the root window, closing the whole application
    """

    root.destroy()


def main_login_window():
    """
    This is the main window of the program. The window includes
    the main sign-up window, sign-in form, and the forgot password
    feature
    """
    preload_web_scrape_data()
    
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


def on_entry_click_username(event):
    """
    This function is for the lable 'username'
    above the entrybox for the username
    """

    global firstclick_username
    if firstclick_username:
        firstclick_username = False
        entry_for_username.delete(0, 'end') 


def on_entry_click_password(event):
    """
    This function is for the lable 'username'
    above the entrybox for the username
    """

    global firstclick_password
    if firstclick_password:
        firstclick_password = False
        entry_for_password.delete(0, 'end') 
        entry_for_password.config(show = '*')


def sign_in():
    """
    This is the business logic for signing in the program
    """

        
    #THIS IS TO CHECK WHETHER ALL THE BOXES ARE FILLED. IF NOT, AN ERROR BOX WILL APPEAR
    if entry_for_username.get() == '' or entry_for_password.get() == '':
        messagebox.showerror('ERROR!', 'Please fill all the boxes!', parent = main_window)

    else:
        #GLOBALIZING THE USERNAME FOR THE NEXT WINDOW (FOR WELCOMING USER)
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

        #THIS IS FOR THE DELETION OF USERNAME AND PASSEWORD ON THE ENTRY BOX
        entry_for_username.delete(0, END)
        entry_for_password.delete(0, END)


def logout():
    """
    Logout by destroying the main window for the guests
    and reopening the main login window
    """

    sign_in_as_guest_window.destroy()
    main_login_window()


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

    button_for_facts_statistics = Button(frame_above_canvas_bottom_part, text = 'Facts & Statistics', font =font_for_sign_in_sign_up, bg = 'black', fg = 'white', command = facts_and_statistics)
    button_for_facts_statistics.grid(row = 0, column = 1, ipadx = 7, ipady = 3, padx=(40,0))

    button_for_blog_section = Button(frame_above_canvas_bottom_part, text = 'Blog Section', font =font_for_sign_in_sign_up, bg = 'black', fg = 'white')
    button_for_blog_section.grid(row = 0, column = 2, ipadx = 7, ipady = 3, padx=(40,0))

    button_for_about_us = Button(frame_above_canvas_bottom_part, text = 'About Us', font =font_for_sign_in_sign_up, bg = 'black', fg = 'white')
    button_for_about_us.grid(row = 0, column = 3, ipadx = 7, ipady = 3, padx=(60,0))

    
    def online_shop():
    """
    This function is for the main window of the
    online shop window. This includes all the
    necessary widgets
    """

    sign_in_as_guest_window.destroy()

    global online_shop_main_window
    online_shop_main_window = Toplevel(root)
    online_shop_main_window.geometry('1300x750+100+50')
    main_frame_for_main_window = Frame(online_shop_main_window)
    main_frame_for_main_window.pack()

    image_canvas = Canvas(main_frame_for_main_window, width=1300, height=750)
    image_canvas.pack()
    image_canvas.create_image(0, 0, anchor=NW, image=image_online_shop)

    global frame_left_side
    frame_left_side = Frame(main_frame_for_main_window, bg ='#050505')
    image_canvas.create_window(120,340, anchor = NW, window = frame_left_side)

    global frame_right_side
    frame_right_side = Frame(main_frame_for_main_window, bg ='#050505')
    image_canvas.create_window(690,200, anchor = NW, window = frame_right_side)


    label_enter_product_id= Label(frame_left_side, font = font_for_label_for_product_id, bg = '#050505', fg = 'White',text = 'Product Id: ')
    label_enter_product_id.grid(row = 0, column = 0, pady =10, sticky = W, padx =(0, 25))

    global entry_for_product_id
    entry_for_product_id= Entry(frame_left_side, width = 15 ,borderwidth =1, bg = '#050505', fg = 'White', font = font_for_label_for_product_id )
    entry_for_product_id.grid(row = 0, column = 1, pady = 10, sticky = W+E)

    label_enter_quantity= Label(frame_left_side, font = font_for_label_for_product_id, bg = '#050505', fg = 'White',text = 'Quantity:   ')
    label_enter_quantity.grid(row = 1, column = 0, sticky = W, padx =(0, 25), pady = 10)

    global entry_for_quantity
    entry_for_quantity= Entry(frame_left_side, width = 15 ,borderwidth =1, bg = '#050505', fg = 'White', font = font_for_label_for_product_id )
    entry_for_quantity.grid(row = 1, column = 1, pady = 10, sticky = W+E)

    button_add_to_cart = Button(frame_left_side, text = 'Add to Cart', bg = '#FF9900',fg = 'Black', font = font_for_online_shop_button, command = add_to_cart)
    button_add_to_cart.grid(row = 3, column = 0, pady = (25, 10), ipadx =15, ipady = 7)

    button_view_my_cart = Button(frame_left_side, text = 'View my Cart', bg = '#FF9900',fg = 'Black', font = font_for_online_shop_button, command = view_my_cart)
    button_view_my_cart.grid(row = 3, column = 1, pady = (25, 10), ipadx =15, ipady = 7, sticky = W)

    button_save_receipt = Button(frame_left_side, text = 'Save Receipt', bg = '#FF9900',fg = 'Black', font = font_for_online_shop_button)
    button_save_receipt.grid(row = 4, column = 0, ipadx =13, ipady = 7)

    label_for_search= Label(frame_right_side, font = font_for_online_shop_search, bg = '#050505', fg = 'White', text = 'Search by Name')
    label_for_search.grid(row = 0, column = 0)

    global entry_search
    entry_search= Entry(frame_right_side, width = 9, borderwidth =1, bg = '#050505', fg = 'White', font = font_for_online_shop_search)
    entry_search.grid(row = 0, column = 1, pady = 5, padx = 7)

    button_search = Button(frame_right_side, text = 'Search', bg = '#050505',fg = 'White', font = font_for_online_shop_button, command = search_by_name)
    button_search.grid(row = 0, column = 2, ipadx =6, padx = 3)

    button_show_all_products = Button(frame_right_side, text = 'Show all products', bg = '#050505',fg = 'White', font = font_for_online_shop_button, command = show_all_products)
    button_show_all_products.grid(row = 0, column = 3, ipadx = 6, padx = 3)

    button_online_shop_go_back = Button(frame_right_side, text='Back', bg='#050505', fg='White', font = font_for_online_shop_button, command = online_shop_back)
    button_online_shop_go_back.grid(row=2, column=0, pady=5, ipadx =11, padx = (0,5), sticky = W+E)

    button_online_shop_exit = Button(frame_right_side, text='Exit', bg='#050505', fg='White', font = font_for_online_shop_button, command = online_shop_exit)
    button_online_shop_exit.grid(row=2, column=1, pady=5, ipadx = 11, padx =5, sticky = W+E)

    #BY CALLING THE INITIALIZE_DATA_VIEWER(), WE ARE PUTTING THE TABLE TO THE LABEL INSIDE THE RIGHT FRAME
    initialize_data_viewer()

    #THE SHOPPING CART NEEDS TO BE DELETED EVERYTIME THE FUNCTION IS CALLED
    conn = sqlite3.connect('Essentials_Hub_Database.db')
    curs = conn.cursor()
    curs.execute('delete from my_shopping_cart')
    conn.commit()
    
 
def initialize_data_viewer():
    """
    This is to initialize/load the data from
    the database and place it to the label
    """

    conn = sqlite3.connect('Essentials_Hub_Database.db')
    df = pd.read_sql_query('select * from Product_Inventory', conn)

    global label_for_viewer
    label_for_viewer = Label(frame_right_side)
    label_for_viewer.grid(row=1, column=0, pady=10, columnspan=4)

    pt = Table(label_for_viewer, dataframe=df)
    for i in range(3):
        pt.expandColumns()

    label_for_viewer.config(text=pt.show())

    
 def show_all_products():
    initialize_data_viewer()


    
    
def preload_web_scrape_data():
    """
    Funtion for preloading all the data
    inside final_scrape.py
    """


    final_scrape.day_by_day()
    final_scrape.for_total_deaths_total_recovered()
    final_scrape.pui_pum_tested()
    final_scrape.picture()

    final_scrape.by_sex()
    final_scrape.cases_outside_ph()
    final_scrape.by_region()
    final_scrape.by_age()
    final_scrape.api()


def facts_and_statistics():
    """
    This function is for the main window of the
    facts and statistics page.
    """

    sign_in_as_guest_window.destroy()

    global facts_and_statistics_window
    facts_and_statistics_window = Toplevel(root)
    facts_and_statistics_window.geometry('1300x750+100+50')
    
    main_frame = Frame(facts_and_statistics_window)
    main_frame.pack()

    canvas_facts_and_statistics = Canvas(main_frame, width = 1300, height = 750)
    canvas_facts_and_statistics.pack()
    canvas_facts_and_statistics.create_image(0,0, anchor = NW, image = image_tracker)

    global image_map
    image_map = ImageTk.PhotoImage(Image.open('PICTURES/image_svg.png'))


    canvas_facts_and_statistics.create_text(1100, 720, font = font_for_date_today, text = final_scrape.dates[0] , fill = 'white')
    canvas_facts_and_statistics.create_image(860, 90, anchor = NW, image = image_map)
    canvas_facts_and_statistics.create_text(255,205, font = font_for_tracker_case_today, text = final_scrape.api_total_cases, fill = '#e99314')
    canvas_facts_and_statistics.create_text(255, 245, font = font_for_tracker_additional, text = f'+{final_scrape.api_additional_cases_today}', fill = 'white')
    canvas_facts_and_statistics.create_text(255, 390, font = font_for_tracker_case_today, text = final_scrape.api_total_deaths, fill = 'red')
    canvas_facts_and_statistics.create_text(250, 425, font = font_for_tracker_additional, text = f'+{final_scrape.api_additional_deaths_today}', fill = 'white')
    canvas_facts_and_statistics.create_text(255, 570, font = font_for_tracker_case_today, text = final_scrape.api_total_recoveries, fill = 'green')
    canvas_facts_and_statistics.create_text(250, 610, font = font_for_tracker_additional, text = f'+{final_scrape.api_additional_recoveries_today}', fill = 'white')
    canvas_facts_and_statistics.create_text(590, 215, font = font_for_tracker_case_today, text = final_scrape.pui, fill = 'white')
    canvas_facts_and_statistics.create_text(590, 405, font = font_for_tracker_case_today, text = final_scrape.pum, fill = 'white')
    canvas_facts_and_statistics.create_text(590, 585, font = font_for_tracker_case_today, text = final_scrape.tested, fill = 'white')


    #FRAME FOR THE BUTTONS BELOW
    frame_for_buttons_below = Frame(facts_and_statistics_window, bg = '#050505')
    canvas_facts_and_statistics.create_window(100,690, anchor = NW, window = frame_for_buttons_below)

    #BUTTONS BELOW

    button_for_page_2 = Button(frame_for_buttons_below, text = 'Page 2', font = font_for_facts_and_statistics_button, bg ='#e99314', fg = 'Black', command = facts_and_statistics_2)
    button_for_page_2.grid(row = 0, column = 0, ipadx = 18, ipady =8, padx=(0,10))

    button_for_page_graphs = Button(frame_for_buttons_below, text = 'Graphs', font = font_for_facts_and_statistics_button, bg ='#e99314', fg = 'Black', command = graphs_page_1)
    button_for_page_graphs.grid(row = 0, column = 1, ipadx = 18, ipady =8, padx=(0,10))

    button_for_page_facts = Button(frame_for_buttons_below, text = 'Facts', font = font_for_facts_and_statistics_button, bg ='#e99314', fg = 'Black')
    button_for_page_facts.grid(row = 0, column = 2, ipadx = 18, ipady =8, padx = (0,10))

    button_for_chatbot = Button(frame_for_buttons_below, text = 'Chatbot', font = font_for_facts_and_statistics_button, bg ='#e99314', fg = 'Black')
    button_for_chatbot.grid(row = 0, column = 2, ipadx = 18, ipady =8, padx = (0,10))

    button_for_page_back = Button(frame_for_buttons_below, text = 'Back', font = font_for_facts_and_statistics_button, bg ='#e99314', fg = 'Black')
    button_for_page_back.grid(row = 0, column = 3, ipadx = 18, ipady =8, command = back_facts_statistics)


def facts_and_statistics_2():
    global facts_and_statistics_window_2
    facts_and_statistics_window_2 = Toplevel(root)
    facts_and_statistics_window_2.geometry('1300x750+100+50')

    main_frame = Frame(facts_and_statistics_window_2)
    main_frame.pack()

    canvas_facts_and_statistics = Canvas(main_frame, width=1300, height=750)
    canvas_facts_and_statistics.pack()
    canvas_facts_and_statistics.create_image(0, 0, anchor=NW, image=image_tracker_2)

    canvas_facts_and_statistics.create_text(250, 210, font=font_for_tracker_case_today,
                                            text=final_scrape.api_fatality_rate, fill='red')
    canvas_facts_and_statistics.create_text(660, 210, font=font_for_tracker_case_today,
                                            text=final_scrape.api_recovery_rate, fill='green')
    canvas_facts_and_statistics.create_text(1030, 210, font=font_for_tracker_case_today, text=final_scrape.api_admitted,
                                            fill='white')

    frame_for_total_cases_region = Frame(facts_and_statistics_window_2, bg='#050505')
    canvas_facts_and_statistics.create_window(175, 365, anchor=NW, window=frame_for_total_cases_region, width=217,
                                              height=275)

    frame_for_total_deaths_region = Frame(facts_and_statistics_window_2, bg='#050505')
    canvas_facts_and_statistics.create_window(560, 365, anchor=NW, window=frame_for_total_deaths_region, width=217,
                                              height=275)

    frame_for_total_recovered_region = Frame(facts_and_statistics_window_2, bg='#050505')
    canvas_facts_and_statistics.create_window(930, 365, anchor=NW, window=frame_for_total_recovered_region, width=217,
                                              height=275)

    # FOR THE CASES PER REGION
    scrollbar_1 = Scrollbar(frame_for_total_cases_region, troughcolor='#050505', bg='#050505',
                            activebackground='#050505', highlightbackground='#050505', highlightcolor='#050505',
                            highlightthickness=0)
    scrollbar_1.pack(side=RIGHT, fill=Y)

    listbox_for_region_total_cases = Listbox(frame_for_total_cases_region, bg='#050505', fg='white', height=15,
                                             width=30, font=font_for_listbox_region, borderwidth=0,
                                             highlightthickness=0)
    listbox_for_region_total_cases.pack()

    for (a, b) in zip(final_scrape.region_cases, final_scrape.region):
        if a == 0 or a == 1:
            listbox_for_region_total_cases.insert(END, f'{a} case', b, '⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯')
        else:
            listbox_for_region_total_cases.insert(END, f'{a} cases', b, '⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯')

    listbox_for_region_total_cases.config(yscrollcommand=scrollbar_1.set)
    scrollbar_1.config(command=listbox_for_region_total_cases.yview, troughcolor='#050505', bg='#050505',
                       activebackground='#050505')

    # FOR DEATHS PER REGION
    scrollbar_2 = Scrollbar(frame_for_total_deaths_region, troughcolor='#050505', bg='#050505',
                            activebackground='#050505', highlightbackground='#050505', highlightcolor='#050505',
                            highlightthickness=0)
    scrollbar_2.pack(side=RIGHT, fill=Y)

    listbox_for_region_deaths = Listbox(frame_for_total_deaths_region, bg='#050505', fg='white', height=15, width=30,
                                        font=font_for_listbox_region, borderwidth=0, highlightthickness=0)
    listbox_for_region_deaths.pack()

    for (a, b) in zip(final_scrape.region_deaths, final_scrape.region):
        if a == 0 or a == 1:
            listbox_for_region_deaths.insert(END, f'{a} death', b, '⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯')
        else:
            listbox_for_region_deaths.insert(END, f'{a} deaths', b, '⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯')

    listbox_for_region_deaths.config(yscrollcommand=scrollbar_2.set)
    scrollbar_2.config(command=listbox_for_region_deaths.yview, troughcolor='#050505', bg='#050505',
                       activebackground='#050505')

    # FOR RECOVERIES PER REGION
    scrollbar_3 = Scrollbar(frame_for_total_recovered_region, troughcolor='#050505', bg='#050505',
                            activebackground='#050505', highlightbackground='#050505', highlightcolor='#050505',
                            highlightthickness=0)
    scrollbar_3.pack(side=RIGHT, fill=Y)

    listbox_for_region_recovered = Listbox(frame_for_total_recovered_region, bg='#050505', fg='white', height=15,
                                           width=30, font=font_for_listbox_region, borderwidth=0, highlightthickness=0)
    listbox_for_region_recovered.pack()

    for (a, b) in zip(final_scrape.region_recovered, final_scrape.region):
        if a == 0 or a == 1:
            listbox_for_region_recovered.insert(END, f'{a} recovery', b, '⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯')
        else:
            listbox_for_region_recovered.insert(END, f'{a} recoveries', b, '⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯')

    listbox_for_region_recovered.config(yscrollcommand=scrollbar_3.set)
    scrollbar_3.config(command=listbox_for_region_recovered.yview, troughcolor='#050505', bg='#050505',
                       activebackground='#050505')

    # FRAME FOR THE BUTTONS BELOW
    frame_for_buttons_below = Frame(facts_and_statistics_window_2, bg='#050505')
    canvas_facts_and_statistics.create_window(500, 690, anchor=NW, window=frame_for_buttons_below)

    # BUTTONS BELOW
    button_for_page_graphs = Button(frame_for_buttons_below, text='Graphs', font=font_for_facts_and_statistics_button,
                                    bg='#e99314', fg='Black')
    button_for_page_graphs.grid(row=0, column=0, ipadx=18, ipady=8, padx=(0, 10))

    button_for_chatbot = Button(frame_for_buttons_below, text='Chatbot', font=font_for_facts_and_statistics_button,
                                bg='#e99314', fg='Black')
    button_for_chatbot.grid(row=0, column=1, ipadx=18, ipady=8, padx=(0, 10))

    button_for_page_back = Button(frame_for_buttons_below, text='Back', font=font_for_facts_and_statistics_button,
                                  bg='#e99314', fg='Black')
    button_for_page_back.grid(row=0, column=2, ipadx=18, ipady=8)


def graphs_page_1():
    facts_and_statistics_window.destroy()

    global graphs_page_1_window
    graphs_page_1_window = Toplevel(root)
    graphs_page_1_window.geometry('1920x1080')
    main_frame = Frame(graphs_page_1_window)
    main_frame.pack()

    canvas_graphs_page_1 = Canvas(main_frame, width=1920, height=1080)
    canvas_graphs_page_1.pack()
    canvas_graphs_page_1.create_image(0, 0, anchor=NW, image=image_for_tracker_graphs)

    # THIS IS THE FRAME FOR THE UPPER CHART
    frame_for_top_graph = Frame(main_frame)
    canvas_graphs_page_1.create_window(120, 15, anchor=NW, window=frame_for_top_graph)

    frame_for_bottom_graphs_if = Frame(main_frame)
    canvas_graphs_page_1.create_window(120, 400, anchor=NW, window=frame_for_bottom_graphs_if)

    # FRAME FOR THE BUTTONS
    frame_for_graphs_buttons = Frame(main_frame, bg='#050505')
    canvas_graphs_page_1.create_window(600, 780, anchor=NW, window=frame_for_graphs_buttons)

    # STYLE OF THE CHART
    plt.style.use('dark_background')

    # FIGURE SIZE
    figure_1 = Figure(figsize=(13, 3.2), dpi=100)
    # FIGURE COLOR, OUTSIDE OF CHART
    figure_1.set_facecolor('#050505')
    subplot_1 = figure_1.add_subplot(111)
    subplot_1.plot(final_scrape.total_dates, final_scrape.total_cases, marker='o', color='y')
    # TITLE
    subplot_1.set_title('Day by day Cases')
    # LABEL X AXIS
    subplot_1.set_xlabel('Days')
    # LABEL YAXIS
    subplot_1.set_ylabel('Number of Cases')
    figure_1.set_tight_layout(True)
    subplot_1.set_facecolor('#050505')
    subplot_1.grid(alpha=0.1)
    for tick in subplot_1.xaxis.get_ticklabels():
        tick.set_rotation(40)
    subplot_1.tick_params(color='white', labelcolor='white')
    canvas1 = FigureCanvasTkAgg(figure_1, frame_for_top_graph)
    canvas1.get_tk_widget().pack()

    toolbar1 = NavigationToolbar2Tk(canvas1, frame_for_top_graph)
    canvas1._tkcanvas.pack()

    # FIGURE SIZE
    figure_6 = Figure(figsize=(13, 3.2), dpi=100)
    # FIGURE COLOR, OUTSIDE OF CHART
    figure_6.set_facecolor('#050505')
    subplot_6 = figure_6.add_subplot(111)
    subplot_6.plot(final_scrape.total_dates, final_scrape.total_deaths_day, marker='.', color='r')
    subplot_6.plot(final_scrape.total_dates, final_scrape.total_recoveries_day, marker='.', color='g')
    # TITLE
    subplot_6.set_title('Deaths and Recoveries per day')
    # LABEL X AXIS
    subplot_6.set_xlabel('Days')
    # LABEL YAXIS
    subplot_6.set_ylabel('Number of Cases')
    figure_6.set_tight_layout(True)
    subplot_6.set_facecolor('#050505')
    subplot_6.grid(alpha=0.1)
    for tick in subplot_6.xaxis.get_ticklabels():
        tick.set_rotation(40)
    subplot_6.tick_params(color='white', labelcolor='white')
    canvas6 = FigureCanvasTkAgg(figure_6, frame_for_bottom_graphs_if)
    canvas6.get_tk_widget().pack()

    toolbar6 = NavigationToolbar2Tk(canvas6, frame_for_bottom_graphs_if)
    canvas6._tkcanvas.pack()

    #BUTTONS
    button_for_graphs_page_1 = Button(frame_for_graphs_buttons, text='Page 1',
                                      font=font_for_facts_and_statistics_button, bg='black', fg='white', state = DISABLED)
    button_for_graphs_page_1.grid(row=0, column=0, ipadx=7, ipady=5, padx=3)

    button_for_graphs_page_2 = Button(frame_for_graphs_buttons, text='Page 2',font=font_for_facts_and_statistics_button, bg='black', fg='white',command=graphs_page_2)
    button_for_graphs_page_2.grid(row=0, column=1, ipadx=7, ipady=5, padx=3)

    button_for_graphs_page_3 = Button(frame_for_graphs_buttons, text='Page 3',font=font_for_facts_and_statistics_button, bg='black', fg='white', command = graphs_page_3)
    button_for_graphs_page_3.grid(row=0, column=2, ipadx=7, ipady=5, padx=3)

    button_for_graphs_back = Button(frame_for_graphs_buttons, text='Back', font=font_for_facts_and_statistics_button,bg='black', fg='white', command = back_graph1)
    button_for_graphs_back.grid(row=0, column=3, ipadx=7, ipady=5, padx=3)


def graphs_page_2():
    try:
        graphs_page_1_window.destroy()
    except:
        pass


    global graphs_page_2_window
    graphs_page_2_window = Toplevel(root)
    graphs_page_2_window.geometry('1920x1080')
    main_frame = Frame(graphs_page_2_window)
    main_frame.pack()

    canvas_graphs_page_2 = Canvas(main_frame, width = 1920, height = 1080)
    canvas_graphs_page_2.pack()
    canvas_graphs_page_2.create_image(0,0, anchor = NW, image = image_for_tracker_graphs)

    #THIS IS THE FRAME FOR THE UPPER CHART
    frame_for_top_graph = Frame(main_frame)
    canvas_graphs_page_2.create_window(120,15, anchor = NW, window = frame_for_top_graph)

    frame_for_bottom_graphs = Frame(main_frame)
    canvas_graphs_page_2.create_window(800,15, anchor = NW, window = frame_for_bottom_graphs)

    # FRAME FOR THE BUTTONS
    frame_for_graphs_buttons_2 = Frame(main_frame, bg='#050505')
    canvas_graphs_page_2.create_window(600, 780, anchor=NW, window=frame_for_graphs_buttons_2)



    figure_4 = Figure(figsize=(6.3, 7), dpi = 100)
    figure_4.set_facecolor('#050505')
    subplot_4 = figure_4.add_subplot(111)
    subplot_4.barh(final_scrape.region[::-1], final_scrape.region_cases[::-1], color = '#FFC000', log = True)
    for index, value in enumerate(final_scrape.region_cases[::-1]):
        subplot_4.text(value, index, str(value), va = 'center', fontsize = 8, fontweight = 'bold')
    subplot_4.set_title('Number of cases per Region in the Philippines')
    subplot_4.set_xlabel('Number of Cases')
    subplot_4.set_ylabel('Regions')
    figure_4.set_tight_layout(TRUE)
    subplot_4.set_facecolor('#050505')
    subplot_4.grid(alpha = 0.1)
    subplot_4.tick_params(color = 'white', labelcolor = 'white')
    canvas4 = FigureCanvasTkAgg(figure_4, frame_for_top_graph)
    canvas4.get_tk_widget().pack()

    toolbar4 = NavigationToolbar2Tk(canvas4, frame_for_top_graph)
    canvas4._tkcanvas.pack()


    figure_5 = Figure(figsize=(6.3, 7), dpi = 100)
    figure_5.set_facecolor('#050505')
    subplot_5 = figure_5.add_subplot(111)
    subplot_5.barh(final_scrape.age_group[::-1], final_scrape.age_number_of_case[::-1], color = '#FF6347', height = 0.6)
    for index, value in enumerate(final_scrape.age_number_of_case[::-1]):
        subplot_5.text(value, index, str(value), va = 'center', fontsize = 8, fontweight = 'bold')
    subplot_5.set_title('Number of Cases per Age Group in the Philippines')
    subplot_5.set_xlabel('Number of Cases')
    subplot_5.set_ylabel('Age Groups')
    figure_5.set_tight_layout(TRUE)
    subplot_5.set_facecolor('#050505')
    subplot_5.grid(alpha = 0.1)
    subplot_5.tick_params(color = 'white', labelcolor = 'white')
    canvas5 = FigureCanvasTkAgg(figure_5, frame_for_bottom_graphs)
    canvas5.get_tk_widget().pack()

    toolbar5 = NavigationToolbar2Tk(canvas5, frame_for_bottom_graphs)
    canvas5._tkcanvas.pack()

    button_for_graphs_page_1 = Button(frame_for_graphs_buttons_2, text='Page 1',
                                      font=font_for_facts_and_statistics_button, bg='black', fg='white', command = back_graph_2)
    button_for_graphs_page_1.grid(row=0, column=0, ipadx=7, ipady=5, padx=3)

    button_for_graphs_page_2 = Button(frame_for_graphs_buttons_2, text='Page 2',
                                      font=font_for_facts_and_statistics_button, bg='black', fg='white',
                                      state =DISABLED)
    button_for_graphs_page_2.grid(row=0, column=1, ipadx=7, ipady=5, padx=3)

    button_for_graphs_page_3 = Button(frame_for_graphs_buttons_2, text='Page 3',
                                      font=font_for_facts_and_statistics_button, bg='black', fg='white', command = graphs_page_3)
    button_for_graphs_page_3.grid(row=0, column=2, ipadx=7, ipady=5, padx=3)

    button_for_graphs_back = Button(frame_for_graphs_buttons_2, text='Back', font=font_for_facts_and_statistics_button,
                                    bg='black', fg='white',command = back_graph_2)
    button_for_graphs_back.grid(row=0, column=3, ipadx=7, ipady=5, padx=3)

def graphs_page_3():
    try:
        graphs_page_2_window.destroy()
    except:
        pass


    global graphs_page_3_window
    graphs_page_3_window = Toplevel(root)
    graphs_page_3_window.geometry('1920x1080')
    main_frame = Frame(graphs_page_3_window)
    main_frame.pack()

    canvas_graphs_page_3 = Canvas(main_frame, width = 1920, height = 1080)
    canvas_graphs_page_3.pack()
    canvas_graphs_page_3.create_image(0,0, anchor = NW, image = image_for_tracker_graphs)

    #THIS IS THE FRAME FOR THE UPPER CHART
    frame_for_top_graph = Frame(main_frame)
    canvas_graphs_page_3.create_window(120,15, anchor = NW, window = frame_for_top_graph)

    frame_for_upper_right = Frame(main_frame)
    canvas_graphs_page_3.create_window(800,15, anchor = NW, window = frame_for_upper_right)

    frame_for_bottom_right = Frame(main_frame)
    canvas_graphs_page_3.create_window(800,400, anchor = NW, window = frame_for_bottom_right)

    # FRAME FOR THE BUTTONS
    frame_for_graphs_buttons_3 = Frame(main_frame, bg='#050505')
    canvas_graphs_page_3.create_window(600, 780, anchor=NW, window=frame_for_graphs_buttons_3)

    x = np.arange(len(final_scrape.outside_region))
    figure_6 = Figure(figsize=(6.3, 7), dpi = 100)
    figure_6.set_facecolor('#050505')
    subplot_6 = figure_6.add_subplot(111)
    subplot_6.set_yticks(np.arange(len(final_scrape.outside_region)))
    subplot_6.set_yticklabels(final_scrape.outside_region[::-1])
    subplot_6.barh(x-0.26, final_scrape.outside_confirmed_cases[::-1], color = '#FFC000', height = 0.25, label = 'Cases')
    subplot_6.barh(x, final_scrape.outside_recovered[::-1], color = '#87CEEB', height = 0.25, label = 'Recoveries')
    subplot_6.barh(x+0.26, final_scrape.outside_deaths[::-1], color = '#FF6347', height = 0.25, label = 'Deaths')
    subplot_6.legend()

    for index, value in enumerate(final_scrape.outside_confirmed_cases[::-1]):
        subplot_6.text(value, index-0.26, str(value), va = 'center', fontsize = 8, fontweight = 'bold')
    for index, value in enumerate(final_scrape.outside_recovered[::-1]):
        subplot_6.text(value, index, str(value), va = 'center', fontsize = 8, fontweight = 'bold')
    for index, value in enumerate(final_scrape.outside_deaths[::-1]):
        subplot_6.text(value, index+0.26, str(value), va = 'center', fontsize = 8, fontweight = 'bold')

    subplot_6.set_title('Number of cases per Region in the Philippines')
    subplot_6.set_xlabel('Number of Cases')
    subplot_6.set_ylabel('Regions')
    figure_6.set_tight_layout(TRUE)
    subplot_6.set_facecolor('#050505')
    subplot_6.grid(alpha = 0.1)
    subplot_6.tick_params(color = 'white', labelcolor = 'white')
    canvas6 = FigureCanvasTkAgg(figure_6, frame_for_top_graph)
    canvas6.get_tk_widget().pack()

    toolbar6 = NavigationToolbar2Tk(canvas6, frame_for_top_graph)
    canvas6._tkcanvas.pack()


    figure_7 = Figure(figsize= (5.5, 3.1), dpi = 100)
    figure_7.set_facecolor('#050505')
    subplot_7 = figure_7.add_subplot(111)
    subplot_7.set_title('Number of cases among Men and Women', pad = 3)
    color = ['#8f2a2a', '#14af8c']
    explode = [0.1, 0]
    subplot_7.pie(final_scrape.sex_number_of_case, labels = final_scrape.sex, colors = color, explode = explode, wedgeprops = {'edgecolor': '#050505', 'linewidth': 1}, startangle = 45, autopct = '%1.1f%%')
    canvas7 = FigureCanvasTkAgg(figure_7, frame_for_upper_right)
    canvas7.get_tk_widget().pack()
    toolbar7 = NavigationToolbar2Tk(canvas7, frame_for_upper_right)
    canvas7._tkcanvas.pack()

    figure_8 = Figure(figsize= (5.5, 3.1), dpi = 100)
    figure_8.set_facecolor('#050505')
    subplot_8 = figure_8.add_subplot(111)
    subplot_8.set_title('Number of deaths among Men and Women', pad = 3)
    color = ['#8f2a2a', '#14af8c']
    explode = [0.1, 0]
    subplot_8.pie(final_scrape.sex_number_of_deaths, labels = final_scrape.sex, colors = color, explode = explode, wedgeprops = {'edgecolor': '#050505', 'linewidth': 1}, startangle = 45, autopct = '%1.1f%%')
    canvas8 = FigureCanvasTkAgg(figure_8, frame_for_bottom_right)
    canvas8.get_tk_widget().pack()
    toolbar8 = NavigationToolbar2Tk(canvas8, frame_for_bottom_right)
    canvas8._tkcanvas.pack()

    button_for_graphs_page_1 = Button(frame_for_graphs_buttons_3, text='Page 1',
                                      font=font_for_facts_and_statistics_button, bg='black', fg='white', command = graphs_page_1)
    button_for_graphs_page_1.grid(row=0, column=0, ipadx=7, ipady=5, padx=3)

    button_for_graphs_page_2 = Button(frame_for_graphs_buttons_3, text='Page 2',
                                      font=font_for_facts_and_statistics_button, bg='black', fg='white', command = back_graph_3)
    button_for_graphs_page_2.grid(row=0, column=1, ipadx=7, ipady=5, padx=3)

    button_for_graphs_page_3 = Button(frame_for_graphs_buttons_3, text='Page 3',
                                      font=font_for_facts_and_statistics_button, bg='black', fg='white', state=  DISABLED)
    button_for_graphs_page_3.grid(row=0, column=2, ipadx=7, ipady=5, padx=3)

    button_for_graphs_back = Button(frame_for_graphs_buttons_3, text='Back', font=font_for_facts_and_statistics_button,
                                    bg='black', fg='white',command = back_graph_3)
    button_for_graphs_back.grid(row=0, column=3, ipadx=7, ipady=5, padx=3)


def back_facts_statistics():
    facts_and_statistics_window.destroy()
    sign_in_as_guest()

def back_graph1():
    try:
        graphs_page_1_window.destroy()
        facts_and_statistics()
    except:
        pass

def back_graph_2():
    try:
        graphs_page_2_window.destroy()
        graphs_page_1()
    except:
        pass

def back_graph_3():
    try:
        graphs_page_3_window.destroy()
        graphs_page_2()
    except:
        pass


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
        forgot_password_fourth_window.destroy()
        main_login_window()

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

image_tracker = ImageTk.PhotoImage(Image.open('PICTURES\image_tracker.jpg'))

image_for_tracker_graphs = ImageTk.PhotoImage(Image.open('PICTURES\image_tracker_graphs.jpg'))

image_online_shop = ImageTk.PhotoImage(Image.open('PICTURES\image_main_online_shop.jpg'))

image_tracker_2 = ImageTk.PhotoImage(Image.open('PICTURES\image_tracker_2.jpg'))


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

font_for_tracker_case_today = Font(family = 'Gotham Black', size = 35)

font_for_listbox_region = Font(family = 'Gotham', size = 14)

font_for_tracker_additional = Font(family = 'Gotham', size = 17)

font_for_date_today = Font(family = 'Gotham', size = 10)

font_for_facts_and_statistics_button = Font(family = 'Gotham', size = 10)

font_for_label_for_product_id = Font(family='Gotham', size=16)

font_for_online_shop_button = Font(family='Gotham', size=11)

font_for_online_shop_search = Font(family='Gotham', size=13)


# ==============================================================================================================================

root.mainloop()
