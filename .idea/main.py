#------------------------------ BLOOD BANK MANAGEMENT SYSTEM ------------------------------
# This code is written by Parin Shah as a part of internal assesement for the subject, Software Engineering

#------------------------- Imported Classes -------------------------

from tkinter import *
import tkinter as tkr
import sqlite3
import pandas as pd
import csv
from tkinter import messagebox as ms
import re
import subprocess
from collections import deque

class BBMS():
    def __init__(self, master):
        self.master = master
        self.fname = StringVar()
        self.lname = StringVar()
        self.email = StringVar()
        self.mobile = StringVar()
        self.bloodgroup = StringVar()
        self.gender = StringVar()
        self.username = StringVar()
        self.password = StringVar()

        self.cur_user = StringVar()

        self.dname = StringVar()
        self.dmobile = StringVar()
        self.dbloodgroup = StringVar()
        self.rname = StringVar()
        self.rmobile = StringVar()
        self.rbloodgroup = StringVar()

        self.login()

        root.title('Blood bank')
        root.config(bg="#d8d8d8")
        root.attributes("-fullscreen", True)
        root.bind("<Escape>", exit)

#------------------------------ Login -------------------------------

    def login(self):
        self.headl = Label(self.master, text='Login', font=('Helvetica', 35, 'bold'), bg='#e9c7ff', padx=20, pady=20, relief="groove")
        self.headl.pack(pady=100)
        self.lgnf = Frame(self.master, highlightthickness='1.5', highlightbackground='#000000')
        self.lgnf.pack(side=TOP)

        Label(self.lgnf, text="Username: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(sticky=W + E, pady=15, padx=10)
        Entry(self.lgnf, textvariable=self.username, font=('Helvetica', 18)).grid(row=0, column=1)

        Label(self.lgnf, text="Password: ", font=('Helvetica', 18, 'bold'), padx=15, pady=5).grid(sticky=W + E, pady=15, padx=10)
        Entry(self.lgnf, textvariable=self.password, font=('Helvetica', 18), show='*').grid(row=1, column=1)

        btn_login = Button(self.lgnf, text="Login", font=('Helvetica', 18), command=self.logdb).grid(row=2, columnspan=4, pady=20)

        lbl_lgn = Label(self.lgnf, text="Register", fg="Blue", font=('Helvetica', 12))
        lbl_lgn.grid(sticky=E, column=3, padx=10)
        lbl_lgn.bind('<Button-1>', self.tgl_regis)

    def logdb(self):
        if(self.username.get() =='' or self.password.get() == ''):
            ms.showerror('Error', 'Please fill all the fields')
            return

        logon = pd.read_csv('user_db.csv')
        s1 = self.username.get()
        s2 = self.password.get()
        self.cur_user = s1

        f = open('login.txt', 'w+')
        f.write(s1)
        f.close()

        ulist = logon['Username'].tolist()
        plist = logon['Password'].tolist()
        l = len(ulist)

        for i in range(l):
            if(s1 == ulist[i] and s2 == plist[i]):
                u = ulist[i]
                p = plist[i]
                break
            else:
                u = ''
                p = ''

        if(u == s1 and p == s2):
            ms.showinfo('Success', 'Login Successful')
            self.tgl_dash()
        else:
            ms.showerror('Try Again...', 'Invalid Credentials')

#--------------------------- Registration ---------------------------

    def regis(self):
        self.headr = Label(self.master, text='Registration', font=('Helvetica', 35, 'bold'), bg='#e9c7ff', padx=20, pady=20, relief="groove")
        self.headr.pack(pady=100)
        self.regf = Frame(self.master, highlightthickness='1.5', highlightbackground='#000000', padx=15)
        self.regf.pack(side=TOP)

        Label(self.regf, text="First Name: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(sticky=W + E, pady=15, padx=10)
        Entry(self.regf, textvariable=self.fname, font=('Helvetica', 18)).grid(row=0, column=1)

        Label(self.regf, text="Last Name: ", font=('Helvetica', 18, 'bold'), padx=15, pady=5).grid(row=0,column=2)
        Entry(self.regf, textvariable=self.lname, font=('Helvetica', 18)).grid(row=0, column=3)

        Label(self.regf, text="Email Id: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(sticky=W + E, pady=15, padx=10)
        Entry(self.regf, textvariable=self.email, font=('Helvetica', 18)).grid(row=1, column=1)

        Label(self.regf, text="Mobile No: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(row=1, column=2)
        Entry(self.regf, textvariable=self.mobile, font=('Helvetica', 18)).grid(row=1, column=3)

        bg_list = {' A+ ', ' A- ', ' B+ ', ' B- ', ' O+ ', ' O- ', ' AB+ ', ' AB- '}
        self.bloodgroup.set('Select Your Blood Group')
        Label(self.regf, text="Blood Group: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(sticky=W + E, pady=15, padx=10)
        bg_dropdown = OptionMenu(self.regf, self.bloodgroup, *bg_list).grid(sticky=W + E, row=2, column=1)

        gender_list = {'Male', 'Female', 'Other'}
        self.gender.set('Select Your Gender')
        Label(self.regf, text="Gender: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(row=2, column=2)
        gen_dropdown = OptionMenu(self.regf, self.gender, *gender_list).grid(sticky=W + E, row=2, column=3)

        Label(self.regf, text="Username: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(sticky=W + E, pady=15, padx=10)
        Entry(self.regf, textvariable=self.username, font=('Helvetica', 18)).grid(row=3, column=1)

        Label(self.regf, text="Password: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(row=3, column=2)
        Entry(self.regf, textvariable=self.password, font=('Helvetica', 18), show="*").grid(row=3, column=3)

        btn_regis = Button(self.regf, text="Register", font=('Helvetica', 18), command=self.regdb)
        btn_regis.grid(row=4, columnspan=4, padx=10)

        lbl_regis = Label(self.regf, text="Login", fg="Blue", font=('Helvetica', 12))
        lbl_regis.grid(sticky=E, column=3, padx=10)
        lbl_regis.bind('<Button-1>', self.tgl_login)

    def regdb(self):
        data = pd.read_csv("user_db.csv")
        lg_data = pd.DataFrame(data)
        emverf = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        mobverf = re.compile("(0/91)?[6-9][0-9]{9}")

        if(self.fname.get() == '' or self.lname.get() == '' or self.username.get() == '' or self.password.get() == '' or len(self.bloodgroup.get()) > 5 or len(self.gender.get()) > 8):
            ms.showerror('Error', 'Please fill all the fields!')
            return

        if(re.search(emverf,self.email.get()) == None):
            ms.showerror('Error', 'Enter a valid email!')
            return

        if(mobverf.match(self.mobile.get()) == None):
            ms.showerror('Error', 'Enter a valid mobile number!')
            return

        with open('user_db.csv', 'r') as f:
            last = deque(csv.reader(f), 1)[0]
            i = int(last[0])
        new_row = {'Sr. No.':i+1, 'Fname':self.fname.get(), 'Lname':self.lname.get(), 'Email':self.email.get(), 'Mobile':self.mobile.get(), 'BloodGroup':self.bloodgroup.get(), 'Gender':self.gender.get(), 'Username':self.username.get(), 'Password':self.password.get()}
        lg_data = lg_data.append(new_row, ignore_index=True)
        lg_data.to_csv('user_db.csv',index=0)
        self.ir += 1
        ms.showinfo('Success', 'Registration Successful \nRedirecting to Login Page')
        self.tgl_login()

#---------------------------- Dash Board ----------------------------

    def dashboard(self):
        self.headb = Label(self.master, text='Dash Board', font=('Helvetica', 28, 'bold'), bg='#e9c7ff', padx=20, pady=20, relief="groove")
        self.headb.pack(pady=100)
        self.dashf = Frame(self.master, highlightthickness='1.5', highlightbackground='#000000')
        self.dashf.pack(side=TOP)

        f = open('login.txt', 'r')
        u = f.read()

        content = []
        with open('user_db.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                content.append(row)

        x = 0
        l = len(content)
        for i in range(l):
            if(u == content[i][1]):
                x = i
                break
            else:
                continue

        Label(self.dashf, text="First Name: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(sticky=E, pady=15, padx=10)
        Label(self.dashf, text=content[x][1], font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(row=0,column=1)

        Label(self.dashf, text="Last Name: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(sticky=E, pady=15, padx=10)
        Label(self.dashf, text=content[x][2], font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(row=1,column=1)

        Label(self.dashf, text="Email Id: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(sticky=E, pady=15, padx=10)
        Label(self.dashf, text=content[x][3], font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(row=2,column=1)

        Label(self.dashf, text="Mobile: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(sticky=E, pady=15, padx=10)
        Label(self.dashf, text=content[x][4], font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(row=3,column=1)

        Label(self.dashf, text="Blood Group: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(sticky=E, pady=15, padx=10)
        Label(self.dashf, text=content[x][5], font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(row=4,column=1)

        Label(self.dashf, text="Gender: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(sticky=E, pady=15, padx=10)
        Label(self.dashf, text=content[x][6], font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(row=5,column=1)

        btn_don = Button(self.dashf, text="Donors", font=('Helvetica', 18), bg='#e9c7ff', command=self.tgl_dtod).grid(row=6, column = 0, sticky=W + E, pady=10, padx=10)
        btn_rec = Button(self.dashf, text="Receivers", font=('Helvetica', 18), bg='#e9c7ff', command=self.tgl_dtor).grid(row=6, column = 1,  sticky=W + E, pady=10, padx=10)
        btn_hos = Button(self.dashf, text="   Hospitals   ", font=('Helvetica', 18), bg='#e9c7ff', command=self.tgl_dtoh).grid(row=6, column = 2, sticky=W + E, pady=10, padx=10)

#------------------------------ Donors ------------------------------

    def donor(self):
        self.headd = Label(self.master, text='Donors', font=('Helvetica', 28, 'bold'), bg='#e9c7ff', padx=20, pady=20, relief="groove")
        self.headd.pack(pady=100)
        self.donf = Frame(self.master, bg='#d1f1fd', highlightthickness='1.5', highlightbackground='#000000')
        self.donf.pack(side=TOP)

        contentd = []
        with open('donor_db.csv', 'r') as csvfiled:
            csvreaderd = csv.reader(csvfiled)
            for row in csvreaderd:
                contentd.append(row)

        i = 0
        for i in range(len(contentd)):
            Label(self.donf, text=contentd[i][0], font=('Helvetica', 18, 'bold'), bg='#d1f1fd', relief='sunken', padx=5, pady=5).grid(row=i+1, column=0, sticky=W + E)
            Label(self.donf, text=contentd[i][1], font=('Helvetica', 18, 'bold'), bg='#d1f1fd', relief='sunken', padx=5, pady=5).grid(row=i+1, column=1, sticky=W + E)
            Label(self.donf, text=contentd[i][2], font=('Helvetica', 18, 'bold'), bg='#d1f1fd', relief='sunken', padx=5, pady=5).grid(row=i+1, column=2, sticky=W + E)
            Label(self.donf, text=contentd[i][3], font=('Helvetica', 18, 'bold'), bg='#d1f1fd', relief='sunken', padx=5, pady=5).grid(row=i+1, column=3, sticky=W + E)

        lbl_dash = Label(self.donf, text="Home", fg="Blue", font=('Helvetica', 12), bg='#d1f1fd')
        lbl_dash.grid(sticky=W, column=0, row=i+2, padx=10)
        lbl_dash.bind('<Button-1>', self.tgl_dtodash)

        lbl_don = Label(self.donf, text="Add New", fg="Blue", font=('Helvetica', 12), bg='#d1f1fd')
        lbl_don.grid(sticky=E, column=3, row=i+2, padx=10)
        lbl_don.bind('<Button-1>', self.tgl_adon)

    def addonor(self):
        self.headad = Label(self.master, text='New Donor', font=('Helvetica', 35, 'bold'), bg='#e9c7ff', padx=20, pady=20, relief="groove")
        self.headad.pack(pady=100)
        self.addf = Frame(self.master, highlightthickness='1.5', highlightbackground='#000000', padx=15)
        self.addf.pack(side=TOP)

        Label(self.addf, text="Name: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(sticky=W + E, pady=15, padx=10)
        Entry(self.addf, textvariable=self.dname, font=('Helvetica', 18)).grid(row=0, column=1)

        Label(self.addf, text="Mobile: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(sticky=W + E, pady=15, padx=10)
        Entry(self.addf, textvariable=self.dmobile, font=('Helvetica', 18)).grid(row=1, column=1)

        bg_list = {' A+ ', ' A- ', ' B+ ', ' B- ', ' O+ ', ' O- ', ' AB+ ', ' AB- '}
        self.dbloodgroup.set('Select Your Blood Group')
        Label(self.addf, text="Blood Group: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(sticky=W + E, pady=15, padx=10)
        bg_dropdown = OptionMenu(self.addf, self.dbloodgroup, *bg_list).grid(sticky=W + E, row=2, column=1)

        btn_add = Button(self.addf, text="Add", font=('Helvetica', 18), command=self.addd).grid(row=3, columnspan=4, padx=10, pady=10)

    def addd(self):
        data = pd.read_csv("donor_db.csv")
        lg_data = pd.DataFrame(data)
        mobverf = re.compile("(0/91)?[6-9][0-9]{9}")

        if(self.dname.get() == '' or len(self.dbloodgroup.get()) > 5):
            ms.showerror('Error', 'Please fill all the fields!')
            return

        if(mobverf.match(self.dmobile.get()) == None):
            ms.showerror('Error', 'Enter a valid mobile number!')
            return

        with open('donor_db.csv', 'r') as f:
            last = deque(csv.reader(f), 1)[0]
            i = int(last[0])
        new_row = {'Sr. No.':i+1, 'Name':self.dname.get(), 'Mobile':self.dmobile.get(), 'BloodGroup':self.dbloodgroup.get()}
        lg_data = lg_data.append(new_row, ignore_index=True)
        lg_data.to_csv('donor_db.csv',index=0)
        self.iad += 1
        ms.showinfo('Success', 'Donor Added')
        self.tgl_don()

#---------------------------- Recievers -----------------------------

    def receiver(self):
        self.headrc = Label(self.master, text='Receivers', font=('Helvetica', 28, 'bold'), bg='#e9c7ff', padx=20, pady=20, relief="groove")
        self.headrc.pack(pady=100)
        self.recf = Frame(self.master, bg='#d1f1fd', highlightthickness='1.5', highlightbackground='#000000')
        self.recf.pack(side=TOP)

        contentr = []
        with open('receiver_db.csv', 'r') as csvfiler:
            csvreaderr = csv.reader(csvfiler)
            for row in csvreaderr:
                contentr.append(row)

        for i in range(len(contentr)):
            Label(self.recf, text=contentr[i][0], font=('Helvetica', 18, 'bold'), bg='#d1f1fd', relief='sunken', padx=5, pady=5).grid(row=i+1, column=0, sticky=W + E)
            Label(self.recf, text=contentr[i][1], font=('Helvetica', 18, 'bold'), bg='#d1f1fd', relief='sunken', padx=5, pady=5).grid(row=i+1, column=1, sticky=W + E)
            Label(self.recf, text=contentr[i][2], font=('Helvetica', 18, 'bold'), bg='#d1f1fd', relief='sunken', padx=5, pady=5).grid(row=i+1, column=2, sticky=W + E)
            Label(self.recf, text=contentr[i][3], font=('Helvetica', 18, 'bold'), bg='#d1f1fd', relief='sunken', padx=5, pady=5).grid(row=i+1, column=3, sticky=W + E)

        lbl_dash = Label(self.recf, text="Home", fg="Blue", font=('Helvetica', 12), bg='#d1f1fd')
        lbl_dash.grid(sticky=W, column=0, row=i+2, padx=10)
        lbl_dash.bind('<Button-1>', self.tgl_rtodash)

        lbl_rec = Label(self.recf, text="Add New", fg="Blue", font=('Helvetica', 12), bg='#d1f1fd')
        lbl_rec.grid(sticky=E, column=3, row=i+2, padx=10)
        lbl_rec.bind('<Button-1>', self.tgl_arec)

    def adreceiver(self):
        self.headar = Label(self.master, text='New Receiver', font=('Helvetica', 35, 'bold'), bg='#e9c7ff', padx=20, pady=20, relief="groove")
        self.headar.pack(pady=100)
        self.adrf = Frame(self.master, highlightthickness='1.5', highlightbackground='#000000', padx=15)
        self.adrf.pack(side=TOP)

        Label(self.adrf, text="Name: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(sticky=W + E, pady=15, padx=10)
        Entry(self.adrf, textvariable=self.rname, font=('Helvetica', 18)).grid(row=0, column=1)

        Label(self.adrf, text="Mobile: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(sticky=W + E, pady=15, padx=10)
        Entry(self.adrf, textvariable=self.rmobile, font=('Helvetica', 18)).grid(row=1, column=1)

        bg_list = {' A+ ', ' A- ', ' B+ ', ' B- ', ' O+ ', ' O- ', ' AB+ ', ' AB- '}
        self.rbloodgroup.set('Select Your Blood Group')
        Label(self.adrf, text="Blood Group: ", font=('Helvetica', 18, 'bold'), padx=5, pady=5).grid(sticky=W + E, pady=15, padx=10)
        bg_dropdown = OptionMenu(self.adrf, self.rbloodgroup, *bg_list).grid(sticky=W + E, row=2, column=1)

        btn_add = Button(self.adrf, text="Add", font=('Helvetica', 18), command=self.addr).grid(row=3, columnspan=4, padx=10, pady=10)

    def addr(self):
        data = pd.read_csv("receiver_db.csv")
        lg_data = pd.DataFrame(data)
        mobverf = re.compile("(0/91)?[6-9][0-9]{9}")

        if(self.rname.get() == '' or len(self.rbloodgroup.get()) > 5):
            ms.showerror('Error', 'Please fill all the fields!')
            return

        if(mobverf.match(self.rmobile.get()) == None):
            ms.showerror('Error', 'Enter a valid mobile number!')
            return

        with open('receiver_db.csv', 'r') as f:
            last = deque(csv.reader(f), 1)[0]
            i = int(last[0])
        new_row = {'Sr. No.':i+1, 'Name':self.rname.get(), 'Mobile':self.rmobile.get(), 'BloodGroup':self.rbloodgroup.get()}
        lg_data = lg_data.append(new_row, ignore_index=True)
        lg_data.to_csv('receiver_db.csv',index=0)
        self.iar += 1
        ms.showinfo('Success', 'Receiver Added')
        self.tgl_rec()

#---------------------------- Hospitals -----------------------------

    def hosp(self):
        self.headh = Label(self.master, text='Nearby Hospitals', font=('Helvetica', 28, 'bold'), bg='#e9c7ff', padx=20, pady=20, relief="groove")
        self.headh.pack(pady=100)
        self.hospf = Frame(self.master, bg='#d1f1fd', highlightthickness='1.5', highlightbackground='#000000')
        self.hospf.pack(side=TOP)

        contenth = []
        with open('hosp_db.csv', 'r') as csvfileh:
            csvreaderh = csv.reader(csvfileh)
            for row in csvreaderh:
                contenth.append(row)

        for i in range(len(contenth)):
            Label(self.hospf, text=contenth[i][0], font=('Helvetica', 18, 'bold'), bg='#d1f1fd', relief='sunken', padx=5, pady=5).grid(row=i+1, column=0, sticky=W + E)
            Label(self.hospf, text=contenth[i][1], font=('Helvetica', 18, 'bold'), bg='#d1f1fd', relief='sunken', padx=5, pady=5).grid(row=i+1, column=1, sticky=W + E)
            Label(self.hospf, text=contenth[i][2], font=('Helvetica', 18, 'bold'), bg='#d1f1fd', relief='sunken', padx=5, pady=5).grid(row=i+1, column=2, sticky=W + E)
            Label(self.hospf, text=contenth[i][3], font=('Helvetica', 18, 'bold'), bg='#d1f1fd', relief='sunken', padx=5, pady=5).grid(row=i+1, column=3, sticky=W + E)

        lbl_dash = Label(self.hospf, text="Home", fg="Blue", font=('Helvetica', 12), bg='#d1f1fd')
        lbl_dash.grid(sticky=E, column=3, row=i+2, padx=10)
        lbl_dash.bind('<Button-1>', self.tgl_htodash)

#-------------------------- Toggle Functions ------------------------

    def tgl_regis(self, event=None):
        self.headl.destroy()
        self.lgnf.destroy()
        self.regis()

    def tgl_login(self, event=None):
        self.headr.destroy()
        self.regf.destroy()
        self.login()

    def tgl_dash(self, event=None):
        self.headl.destroy()
        self.lgnf.destroy()
        self.dashboard()

    def tgl_don(self, event=None):
        self.headad.destroy()
        self.addf.destroy()
        self.donor()

    def tgl_rec(self, event=None):
        self.headar.destroy()
        self.adrf.destroy()
        self.receiver()

    def tgl_adon(self, event=None):
        self.headd.destroy()
        self.donf.destroy()
        self.addonor()

    def tgl_arec(self, event=None):
        self.headrc.destroy()
        self.recf.destroy()
        self.adreceiver()

    def tgl_dtodash(self, event=None):
        self.headd.destroy()
        self.donf.destroy()
        self.dashboard()

    def tgl_rtodash(self, event=None):
        self.headrc.destroy()
        self.recf.destroy()
        self.dashboard()

    def tgl_htodash(self, event=None):
        self.headh.destroy()
        self.hospf.destroy()
        self.dashboard()

    def tgl_dtod(self):
        self.headb.destroy()
        self.dashf.destroy()
        self.donor()

    def tgl_dtor(self):
        self.headb.destroy()
        self.dashf.destroy()
        self.receiver()

    def tgl_dtoh(self):
        self.headb.destroy()
        self.dashf.destroy()
        self.hosp()

#--------------------------- Driver Code ----------------------------
root = Tk()
BBMS(root)
root.mainloop()
