import numpy as np
import pandas as pd
import random
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import filedialog

#Variables that will be needed in multiple places
x=set()  # Set of pairs with 1 and 2
y=set()  # Set of pairs with 3 and either 1 or 2
v=set()  # set of pairs with both 3
q=set()  # set of pairs with at least one 4 but no 5
not_part = set()  #set of students not participating

class thisApp:
    def __init__(self, parent):
        self.parent = parent
        self.temp2 = pd.DataFrame([])
        self.formatted_pairs_final = []
        self.formatted_groups_final = []
        self.missed_final = []
        self.names = []
        self.option1=''
        self.option2=''
        self.leftoversOK=''
        Ask_for_File(self.parent)

def center(toplevel):     #centers the dialog box on the screen
    toplevel.update_idletasks()
    # w = 600
    # h = 100
    w = toplevel.winfo_width()
    h = toplevel.winfo_height()
    positionRight = int(toplevel.winfo_screenwidth()/2 - w/2)
    positionDown = int(toplevel.winfo_screenheight()/3 - h/2)
    # toplevel.geometry("{}x{}+{}+{}".format(w, h, positionRight, positionDown))
    toplevel.geometry("+{}+{}".format(positionRight, positionDown))

class Ask_for_File:    #asks user for the cvs file containing the class data

    # read data into a pandas data frame and make the names column the index
    def Read_Data(self,FileName):
        temp = pd.read_csv(FileName,index_col=1)  #note: may need to change index col = 1
        temp = temp.dropna(how='all') #drop blank rows and continue to call it temp
        temp = temp.dropna(axis=1, how='any')  #drop blank columns
        temp = temp.drop(columns=['Timestamp'])  #drop the timestamp column

        # remove words from columns leaving only 1-5 and NaN (for "this is me!")
        for num in range(len(temp.columns)):
            dftemp = temp.iloc[:,num].str.extract(r'(\d+)', expand=False)
            temp.iloc[:,num]=dftemp  #replace old column with new values
        thisApp.temp2 = temp
        thisApp.names=temp.index.tolist()
    
    def browse_button(self):
        # Allow user to select a file
        filename = filedialog.askopenfile()
        self.Read_Data(filename)
        self.sets_of_pairs(thisApp.temp2)
        self.frame.destroy()
        Offer_Options(self.parent)
     
    # sort pairs of students according to whether they work well together,
    # haven't worked together, or are less than ideal at working together
    def sets_of_pairs(self, temp1):
        for row in range(len(temp1.index)):
            for col in range(len(temp1.columns)):
                    #get one person's rating of pair
                score = temp1.loc[temp1.index[row],temp1.index[col]]
                    #get other person's rating of pair
                score2 = temp1.loc[temp1.index[col],temp1.index[row]]
                if (score =='1' or score =='2') and (score2 =='1' or score2 =='2'):
                    pair = self.partners(row, col, temp1)
                    if pair not in x:  
                        x.add(pair)  #put names in set without duplicates
                elif (score =='3' and (score2 =='2' or score2 == '1')) or \
                     ((score =='2' or score == '1') and score2 == '3'):
                    pair = self.partners(row, col, temp1)
                    if pair not in y:  
                        y.add(pair)  #put names in set without duplicates
                elif score == '3' and score2 == '3':
                    pair = self.partners(row, col, temp1)
                    if pair not in v:  
                        v.add(pair)  #put names in set without duplicates
                elif (score == '4' and score2 !='5') or (score !='5' and score2 == '4'):
                    pair = self.partners(row, col, temp1)
                    if pair not in q:
                        q.add(pair)

    def __init__(self, parent):
        self.parent = parent
        self.parent.attributes('-alpha', 0.0)
            #keeps the dialog box invisible until it gets centered

        self.parent.title("Which file?")
        self.frame = ttk.Frame(self.parent, borderwidth=5, relief="sunken", width=800, height=400)
        # self.frame = ttk.Frame(self.parent, borderwidth=30, width=700, height=100)
        self.frame.grid(column=0, row=0, sticky='nwes')
        self.instructions = ttk.Label(self.frame,text="Please select the file that has the data.",
                                      font=('Verdana',15),background='gray93',foreground='gray0')
        self.instructions.grid(column=3, row=1)
        self.button2 = ttk.Button(self.frame, text="Browse", command=self.browse_button)
        self.button2.grid(row=1, column=1)
        center(self.parent)
        self.parent.attributes('-alpha', 1.0)
            #makes the dialog box visible now that it's centered

    def partners(self, person1num, person2num, temp2):     #put names in alphabetical order
        if temp2.index[person1num] < temp2.index[person2num]:     
            pair2 = (temp2.index[person1num],temp2.index[person2num])
        else:
            pair2 = (temp2.index[person2num],temp2.index[person1num])
        return pair2

class Offer_Options:
    def type_partners(self):
        thisApp.option1 = self.likeold.get()
        
    def type_groups(self):
        thisApp.option2 = self.pairgroup.get()
        
    def tally(self):
        not_part.clear()
        #creates a set of students who are not participating
        for key, value in self.checked_dict.items():
            if value.get() > 0:
                not_part.add(key)
        self.NumStudents =  len(thisApp.names)-len(not_part)
        self.information.config(text=str(self.NumStudents)+' students participating today')
        
    def done_button(self):
                
        if thisApp.option2 ==1:                   #check whether partners or groups are desired
            if thisApp.option1 == 1:              #check whether to stack preferred or new first
                thisApp.formatted_pairs_final, thisApp.missed_final = \
                                               format_partners(x,y,v,q,not_part)
            else:
                thisApp.formatted_pairs_final, thisApp.missed_final = \
                                               format_partners(v,y,q,x,not_part)
        elif thisApp.option2 ==2:
            if thisApp.option1 == 1:
                thisApp.formatted_groups_final, thisApp.missed_final = \
                                                format_groups(x,y,v,q,not_part)
                    # reshuffles and pairs students again up to five times
                    #if there are more than three people without a group
                i = 0                   
                while len(thisApp.missed_final) > 3 and i < 5:
                    thisApp.formatted_groups_final, thisApp.missed_final = \
                                                    format_groups(x,y,v,q,not_part)
                    i = i + 1
            else:
                thisApp.formatted_groups_final, thisApp.missed_final = \
                                                format_groups(v,y,q,x,not_part)
                    # reshuffles and pairs students again up to five times
                    #if there are more than three people without a group
                i = 0                   
                while len(thisApp.missed_final) > 3 and i < 5:
                    thisApp.formatted_groups_final, thisApp.missed_final = \
                                                    format_groups(v,y,q,x,not_part)
                    i = i + 1
        else:
            if thisApp.option1 == 1:
                thisApp.formatted_groups_final, thisApp.missed_final = \
                                                  format_triplets(x,y,v,q,not_part)
                    # reshuffles and pairs students again up to five times
                    #if there are more than two people without a group
                i = 0                   
                while len(thisApp.missed_final) > 2 and i < 5:
                    thisApp.formatted_groups_final, thisApp.missed_final = \
                                                  format_triplets(x,y,v,q,not_part)
                    i = i + 1
            else:
                thisApp.formatted_groups_final, thisApp.missed_final = \
                                                  format_triplets(v,y,q,x,not_part)
                    # reshuffles and pairs students again up to five times
                    #if there are more than two people without a group
                i = 0                   
                while len(thisApp.missed_final) > 2 and i < 5:
                    thisApp.formatted_groups_final, thisApp.missed_final = \
                                                  format_triplets(v,y,q,x,not_part)
                    i = i + 1
                
            
        self.frame.destroy()
        if thisApp.option2 ==1:
            drawclass(self.parent, thisApp.formatted_pairs_final, thisApp.missed_final)
        else:
            drawclass(self.parent, thisApp.formatted_groups_final, thisApp.missed_final)
                
    def __init__ (self,parent):
        self.parent = parent
        self.parent.attributes('-alpha', 0.0)
            #keeps the dialog box invisible until it gets centered

        self.parent.title("Which options?")
        self.frame = ttk.Frame(self.parent, borderwidth=5, relief="sunken", width=800, height=400)
        self.frame.grid(column=0, row=0, sticky='nwes')
        
        self.part1 = ttk.Frame(self.frame)
        self.part1.grid(column = 0, row = 0)
        self.part2 = ttk.Frame(self.frame)
        self.part2.grid(column=0, row=1)
        self.part3 = ttk.Frame(self.frame)
        self.part3.grid(column=1, row=0, rowspan=2)
        
            #creates checkbuttons to select students not participating
        self.checked_dict = {}
        self.checked_dict.clear()
        not_part.clear()
        for student in thisApp.names:
            self.checked_dict[student] = IntVar()
            self.checked_dict[student].set(0)
            st_name = ttk.Checkbutton(self.part2, text = student,
                                      variable=self.checked_dict[student], command=self.tally)
            st_name.grid(column=0, sticky='w')
        self.instructions2 = ttk.Label(self.part1,text="Select any students not participating",
                                       font=('Verdana',15), background='gray94',foreground='gray0')
        self.instructions2.grid(column=0, row=0)
        
        self.NumStudents =  len(thisApp.names)-len(not_part)
        self.information = ttk.Label(self.part3, text = str(self.NumStudents)+
                                     ' students participating today',
                                     font=('Verdana',15), background='gray94',foreground='gray0')
        self.information.grid(column=1, row = 3)
        
        self.instructions3 = ttk.Label(self.part3,text="What size groups?",
                                       font=('Verdana',15), background='gray94',foreground='gray0')
        self.instructions3.grid(column=1, row=5)
        self.pairgroup = IntVar(parent,1)
        thisApp.option2 = 1 #set default value to match default selection
        R3 = ttk.Radiobutton(self.part3, text="Partners", variable=self.pairgroup, value=1,
                              command=self.type_groups)
        R3.grid(column=1,row=6)
        R5 = ttk.Radiobutton(self.part3, text="Groups of 3", variable=self.pairgroup, value =3,
                             command=self.type_groups)
        R5.grid(column=1,row=7)
        R4 = ttk.Radiobutton(self.part3, text="Groups of 4", variable=self.pairgroup, value=2,
                             command=self.type_groups)
        R4.grid(column=1,row=8)
        
        self.instructions1 = ttk.Label(self.part3,text="What kind of partners/groups do you want?",
                                      font=('Verdana',15),background='gray94',foreground='gray0')
        self.instructions1.grid(column=1, row=10)
        self.likeold = IntVar(parent,1)
        thisApp.option1 = 1  #set default value to match default selection
        R1 = ttk.Radiobutton(self.part3, text="Preferred Partners", variable=self.likeold, value=1,
                             command=self.type_partners)
        R1.grid(column=1, row=11)
        R2 = ttk.Radiobutton(self.part3, text="New Partners", variable=self.likeold, value=2,
                             command=self.type_partners)
        R2.grid(column=1, row=12)
        
        donebutton = ttk.Button(self.part3, text="Done", command=self.done_button)
        donebutton.grid(row=18, column=2)
        
        center(self.parent)
        self.parent.attributes('-alpha', 1.0)
            #makes the dialog box visible now that it's centered
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

    # this function creates a list of partners with preference to those who want to work together
def create_pairings(k,m,n,s,t):

    best_pairs = list(k)
    random.shuffle(best_pairs)

    maybe_pairs = list(m)
    random.shuffle(maybe_pairs)

    new_pairs = list(n)
    random.shuffle(new_pairs)

    soso_pairs = list(s)
    random.shuffle(soso_pairs)

    used = set()   #set of names that have already been used
    groups = []    #list of partner groups

        #checks that students are not listed twice and that they are not
        #on the non-participating list.
    for p in range(len(best_pairs)):
        if (best_pairs[p][0] not in used and best_pairs[p][0] not in t) \
           and (best_pairs[p][1] not in used and best_pairs[p][1] not in t):
            used.update(best_pairs[p])
            groups.append(best_pairs[p])

    for p in range(len(maybe_pairs)):
        if (maybe_pairs[p][0] not in used and maybe_pairs[p][0] not in t) \
           and (maybe_pairs[p][1] not in used and maybe_pairs[p][1] not in t):
            used.update(maybe_pairs[p])
            groups.append(maybe_pairs[p])
            
    for p in range(len(new_pairs)):
        if (new_pairs[p][0] not in used and new_pairs[p][0] not in t) \
           and (new_pairs[p][1] not in used and new_pairs[p][1] not in t):
            used.update(new_pairs[p])
            groups.append(new_pairs[p])
            
    for p in range(len(soso_pairs)):
        if (soso_pairs[p][0] not in used and soso_pairs[p][0] not in t) \
           and (soso_pairs[p][1] not in used and soso_pairs[p][1] not in t):
            used.update(soso_pairs[p])
            groups.append(soso_pairs[p])
            
    missed = []
    for person in thisApp.temp2.index:   # check for students without partners
        if person not in used and person not in t:  # but also not on non-participating list
            missed.append(person)
 
    return groups, missed

def format_partners(a,b,c,d,e):
    # run the function create_pairings and get out a list of groups
    # and a list of missed students
    groups2, missed2 = create_pairings(a,b,c,d,e)

    # reshuffles and pairs students again up to five times
    # if there is more than one person without a partner
    i = 0                   
    while len(missed2) > 1 and i < 5:
        groups2, missed2 = create_pairings(a,b,c,d,e)
        i = i + 1

    #format the pairs nicely and create blank pairs to fill the remaining desks
    formatted_pairs = []
    for couple in range(len(groups2)):
        formatted_pairs.append(" " + groups2[couple][0] + " & " + groups2[couple][1])
    while couple < 19:
        formatted_pairs.append("  ")
        couple = couple + 1
                
    return formatted_pairs, missed2

def create_groups(pool,groups2,used2):    
        # checks that students are not listed twice
    short_list2=pool.copy()
    for p in range(len(pool)):
        if pool[p][0] not in used2 and pool[p][1] not in used2:
            n=0
            while n < (len(short_list2)):
                
                if (short_list2[n][0] not in used2 and short_list2[n][0] not in pool[p]) \
                   and (short_list2[n][1] not in used2 and short_list2[n][1] not in pool[p]):
                       
                    ch_pr1 = (pool[p][0],short_list2[n][0])
                    ch_pr1 = sorted(ch_pr1)
                    ch_pr1 = tuple(ch_pr1)
                    ch_pr2 =(pool[p][0],short_list2[n][1])
                    ch_pr2 = sorted(ch_pr2)
                    ch_pr2 = tuple(ch_pr2)
                    ch_pr3 =(pool[p][1],short_list2[n][0])
                    ch_pr3 = sorted(ch_pr3)
                    ch_pr3 = tuple(ch_pr3)
                    ch_pr4 =(pool[p][1],short_list2[n][1])
                    ch_pr4 = sorted(ch_pr4)
                    ch_pr4 = tuple(ch_pr4)
                
                    if ch_pr1 in pool and ch_pr2 in pool and ch_pr3 in pool and ch_pr4 in pool:
                        keep_group = (pool[p][0],pool[p][1],short_list2[n][0],short_list2[n][1])
                        groups2.append(keep_group)
                            # add will add the strings without breaking them into letters
                            # but add will only add one item to the set at a time
                            # update can handle multiple items, but breaks strings into letters
                        used2.add(ch_pr1[0])   
                        used2.add(ch_pr1[1])   
                        used2.add(ch_pr4[0])   
                        used2.add(ch_pr4[1])
                        short_list2.remove(pool[p])
                        short_list2.remove(short_list2[n-1])
                        n=len(short_list2)
                    else:
                        n=n+1
                        
                else:
                    n=n+1
            
    return short_list2, groups2, used2

def format_groups(a,b,c,d,e):

    best_picks = list(a)
    random.shuffle(best_picks)

    next_picks = list(b)
    random.shuffle(next_picks)
    
    new_picks = list(c)
    random.shuffle(new_picks)

    soso_picks = list(d)
    random.shuffle(soso_picks)

    used = set()   #set of names that have already been used
    used.update(e)  #add name(s) of non participating students to used set
    groups = []    #list of established groups
   
    short_list, groups, used = create_groups(best_picks,groups,used)
    short_list.extend(next_picks)
    short_list, groups, used = create_groups(short_list,groups,used)
    short_list.extend(new_picks)
    short_list, groups, used = create_groups(short_list,groups,used)
    short_list.extend(soso_picks)
    short_list, groups, used = create_groups(short_list,groups,used)
    
    missed = []
    for person in thisApp.temp2.index:   # check for students without partners
        if person not in used: 
            missed.append(person)

#    #check whether students in missed gave scores of '5'
#    thisApp.leftoversOK='T'
#    pairing_missed = [(missed[p1], missed[p2]) for p1 in range(len(missed)) \
#for p2 in range(p1+1,len(missed))]
#    print(pairing_missed)
#    for pairing in pairing_missed:
#            #get one person's rating of pair
#        score = thisApp.temp2.loc[pairing[0],pairing[1]]
#            #get other person's rating of pair
#        score2 = thisApp.temp2.loc[pairing[1],pairing[0]]
#        print(score, score2)
#        if score == '5' or score2 == '5':
#            thisApp.leftoversOK='F'
#    print(thisApp.leftoversOK)
            
    return groups, missed

def create_triplets(pool, groups2, used2):
    
    shrinking=pool.copy()
    for pair in pool:
        for name in thisApp.names:
            if pair[0] not in used2 and pair[1] not in used2 and name not in used2 and \
               name not in pair:
                ch_pr1 = (pair[0],name)
                ch_pr1 = sorted(ch_pr1)
                ch_pr1 = tuple(ch_pr1)
                ch_pr2 = (pair[1],name)
                ch_pr2 = sorted(ch_pr1)
                ch_pr2 = tuple(ch_pr1)
                if ch_pr1 in pool and ch_pr2 in pool:
                    keep_group = (pair[0],pair[1],name,"   ")
                    groups2.append(keep_group)
                    used2.add(pair[0])   
                    used2.add(pair[1])   
                    used2.add(name)
                    shrinking.remove(pair)
    
    return shrinking, groups2, used2

def format_triplets(k,m,n,s,t):
    
    best_pairs = list(k)
    random.shuffle(best_pairs)

    maybe_pairs = list(m)
    random.shuffle(maybe_pairs)

    new_pairs = list(n)
    random.shuffle(new_pairs)

    soso_pairs = list(s)
    random.shuffle(soso_pairs)

    used = set()   #set of names that have already been used
    used.update(t)  #add name(s) of non participating students to used set
    groups = []    #list of triplet groups
    
    short_list, groups, used = create_triplets(best_pairs, groups, used)
    short_list.extend(maybe_pairs)
    short_list, groups, used = create_triplets(short_list, groups, used)
    short_list.extend(new_pairs)
    short_list, groups, used = create_triplets(short_list, groups, used)
    short_list.extend(soso_pairs)
    short_list, groups, used = create_triplets(short_list, groups, used)

    missed = []
    for person in thisApp.temp2.index:   # check for students without partners
        if person not in used: 
            missed.append(person) 

    return groups, missed

    
# draws classroom
class drawclass:
    
    def decrease(self):
        self.labelsize.set(self.labelsize.get()-5)
        self.labelfont.configure(size = self.labelsize.get())

    def increase(self):
        self.labelsize.set(self.labelsize.get()+5)
        self.labelfont.configure(size = self.labelsize.get())       
                
    def __init__(self, parent,formatted_sets,missed3):
        self.parent = parent
        s = ttk.Style()
        s.configure('TFrame')
        s.configure('gray1.TFrame',background='gray1')
#        s.configure('TButton.label',background='cyan')
        s.configure('TLabel',background='gray1',foreground='yellow')

        self.frame = ttk.Frame(self.parent, borderwidth=5, relief="sunken")
        self.frame.grid(column=0, row=0, sticky='nwes')
        
        s.configure('red.TFrame', background = 'red')
        self.topframe = ttk.Frame(self.frame, style='gray1.TFrame')
        self.topframe.grid(row=0, columnspan=2, sticky='nsew')
        
        self.bigger=ttk.Button(self.topframe,text="Make bigger", command=self.increase)
        self.bigger.grid(column=0,row=0, sticky='ne',padx=10)
        self.smaller=ttk.Button(self.topframe,text="Make smaller", command=self.decrease)
        self.smaller.grid(column=1, row=0, sticky='nw',padx=10)
        self.front_label = ttk.Label(self.topframe,text="Front of Room")
        self.front_label.grid(column=3, row=0, sticky='we')
        self.front_label.config(font=('Verdana',15))
        self.door_label = ttk.Label(self.topframe,text="Door ")
        self.door_label.grid(column=5, row=1, sticky='e')
        self.door_label.config(font=('Verdana',15))
        
        s.configure('blue.TFrame', background = 'blue')
        self.windowframe = ttk.Frame(self.frame, style='gray1.TFrame')
        self.windowframe.grid(column=0, row=1, rowspan=5, sticky='nsew')

        self.win_labels =[]
        for letter in range(len(list('WINDOWS'))):
            self.winvar = StringVar()
            self.winvar.set(list('WINDOWS'[letter]))
            self.win_labels.append(self.winvar)       
            self.window_label = ttk.Label(self.windowframe,textvariable=self.winvar)
            self.window_label.grid(column=0, row=letter, sticky='ew',padx=(5,10))
            self.window_label.configure(font=('Verdana',15))
        
        s.configure('green.TFrame', background = 'green')
        self.desks = ttk.Frame(self.frame, style='gray1.TFrame')
        self.desks.grid(column=1,row=1, columnspan=4, rowspan=5, sticky='nwes')

        self.labelsize = IntVar()
        self.labelsize.set(15)
                
        self.labelfont = tkFont.Font(family = 'Verdana', size = self.labelsize.get())

        if thisApp.option2 == 1:      # want partners
            self.parent.title("Partners")
            self.partnerlabels = []   # makes a list so that it doesn't show
                                      # just the last pair repeated in all desks
            num2=0
            for r in range(5):
                for c in range(4):
                    self.partnerlabel = StringVar()
                    self.partnerlabel.set(formatted_sets[num2]) 
                    self.partnerlabels.append(self.partnerlabel)
                    self.pair_desks = ttk.Label(self.desks, textvariable=self.partnerlabel,
                                                relief='groove',borderwidth=2,
                                                font=self.labelfont,background='slate blue')
                    count=r*4+c+1
                    if count<19:
                        if c%2 == 0:
                            self.pair_desks.grid(column=c, row=r, sticky='nwes',padx=(0,30),
                                                 pady=10, ipadx=5, ipady=5)
                        else:
                            self.pair_desks.grid(column=c, row=r, sticky='nwes',padx=(30,0),
                                                 pady=10, ipadx=5, ipady=5)
                        num2 = num2 + 1

                    
        
        else:                        # want groups of 3 or 4
            self.parent.title("Groups")
            self.grouplabels = []
            count = len(formatted_sets)
            while count < 12:
                formatted_sets.append(("  ","   ","   ","   "))
                count = count + 1
            
            num2=0
            for r in range(3):
                for c in range(4):
                    self.group1 = LabelFrame(self.desks, relief='flat',background='slate blue')
                    self.group2 = LabelFrame(self.desks, relief='flat',background='slate blue')
                    
                    count=r*4+c+1
                    if count<11 or (thisApp.option2 == 3 and len(thisApp.names)>30) or \
                       (thisApp.option2 ==3 and count<11):
                        
                        self.group2.grid(column=c*3, row=r, sticky='nwes', pady=10)
                        self.group1.grid(column=c*3+1, row=r, sticky='nwes', pady=10)
                       
                        for i in range(4):
                            self.grouplabel = StringVar()
                            self.grouplabel.set(formatted_sets[num2][i])
                            self.grouplabels.append(self.grouplabel)
                            
                            if i%2 == 0:
                                self.student1 = ttk.Label(self.group2,
                                                          textvariable=self.grouplabel,
                                                          borderwidth=2, font=self.labelfont,
                                                          background='slate blue')
                                if i == 0:
                                    self.student1.grid(column=0, row=0,sticky='nwe',pady=5,
                                                       padx=(0,10), ipadx=5, ipady=5)
                                else:
                                    self.student1.grid(column=0,row=1, sticky='new',pady=5,
                                                       padx=(0,10), ipadx=5, ipady=5)

                            else:
                                self.student1 = ttk.Label(self.group1,
                                                          textvariable=self.grouplabel,
                                                          borderwidth=2, font=self.labelfont,
                                                          background='slate blue')
                                if i == 1:
                                    self.student1.grid(column=0, row=1,sticky='ne',pady=5,
                                                       ipadx=5, ipady=5)
                                else:
                                    self.student1.grid(column=0,row=0, sticky='ne',pady=5, 
                                                       ipadx=5, ipady=5)
                        num2 = num2 + 1

        s.configure('yellow.TFrame', background = 'yellow')
        self.helpful = ttk.Frame(self.frame, style='gray1.TFrame')
        self.helpful.grid(row=6, columnspan=2,sticky='nsew')
        
        s.configure('purple.TFrame', background = 'purple')
        self.bottom = ttk.Frame(self.frame, style='gray1.TFrame')
        self.bottom.grid(row=7, columnspan=2,sticky='nsew')

        #Print the name of any students without partners
        self.partnerlabels2=[]
        num3=0
        for num3 in range(len(missed3)):
            self.partnerlabel2 = StringVar()
            
            if thisApp.option2 == 1:      # want partners
                self.partnerlabel2.set("%s needs a partner." % (missed3[num3]))
            else:
                self.partnerlabel2.set("%s needs a group." %(missed3[num3]))
                
            self.partnerlabels2.append(self.partnerlabel2)
            self.message = ttk.Label(self.helpful, textvariable=self.partnerlabel2,
                                     foreground = 'red', font=('Verdana', 20))
            self.message.grid(column=1,row=num3, sticky='e')
        self.back_label = ttk.Label(self.bottom,text="Back of Room")
        self.back_label.grid(column=4, row=1, sticky='we')
        self.back_label.config(font=('Verdana',15))
            
        self.redo = ttk.Button(self.bottom,text="Randomize Again", command=self.rand_again)
        self.redo.grid(column=0, row=2,padx=10)
        self.newclass = ttk.Button(self.bottom,text="New Class", command=self.new_class)
        self.newclass.grid(column=1,row=2,padx=10)
        self.newoptions = ttk.Button(self.bottom, text="New Options", command=self.new_options)
        self.newoptions.grid(column=2,row=2,padx=10)
             
        self.parent.geometry("+10+10")
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.frame.grid_columnconfigure(0,weight=1)
        self.frame.grid_columnconfigure(1,weight=4)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=10)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        
        self.topframe.grid_columnconfigure(2,weight=3)
        self.topframe.grid_columnconfigure(4,weight=3)
        
        self.helpful.grid_columnconfigure(0,weight=3)
        self.helpful.grid_columnconfigure(2,weight=1)
        self.bottom.grid_columnconfigure(3,weight=2)
        self.bottom.grid_columnconfigure(5,weight=3)
        
        self.desks.grid_columnconfigure(2,weight=1,minsize=40)
        self.desks.grid_columnconfigure(5,weight=1, minsize=10)
        self.desks.grid_columnconfigure(8,weight=1, minsize=40)

     
    def rand_again(self):
        self.frame.destroy()
        if thisApp.option2 ==1:                   #check whether partners or groups are desired
            if thisApp.option1 == 1:              #check whether to stack preferred or new first
                thisApp.formatted_pairs_final, thisApp.missed_final = \
                                               format_partners(x,y,v,q,not_part)
            else:
                thisApp.formatted_pairs_final, thisApp.missed_final = \
                                               format_partners(v,y,q,x,not_part)
        elif thisApp.option2 ==2:
            if thisApp.option1 == 1:
                thisApp.formatted_groups_final, thisApp.missed_final = \
                                                format_groups(x,y,v,q,not_part)
                    # reshuffles and pairs students again up to five times
                    #if there are more than three people without a group
                i = 0                   
                while len(thisApp.missed_final) > 3 and i < 5:
                    thisApp.formatted_groups_final, thisApp.missed_final = \
                                                    format_groups(x,y,v,q,not_part)
                    i = i + 1
            else:
                thisApp.formatted_groups_final, thisApp.missed_final = \
                                                format_groups(v,y,q,x,not_part)
                    # reshuffles and pairs students again up to five times
                    #if there are more than three people without a group
                i = 0                   
                while len(thisApp.missed_final) > 3 and i < 5:
                    thisApp.formatted_groups_final, thisApp.missed_final = \
                                                    format_groups(v,y,q,x,not_part)
                    i = i + 1
        else:
            if thisApp.option1 == 1:
                thisApp.formatted_groups_final, thisApp.missed_final = \
                                                  format_triplets(x,y,v,q,not_part)
                    # reshuffles and pairs students again up to five times
                    #if there are more than two people without a group
                i = 0                   
                while len(thisApp.missed_final) > 2 and i < 5:
                    thisApp.formatted_groups_final, thisApp.missed_final = \
                                                  format_triplets(x,y,v,q,not_part)
                    i = i + 1
            else:
                thisApp.formatted_groups_final, thisApp.missed_final = \
                                                  format_triplets(v,y,q,x,not_part)
                    # reshuffles and pairs students again up to five times
                    #if there are more than two people without a group
                i = 0                   
                while len(thisApp.missed_final) > 2 and i < 5:
                    thisApp.formatted_groups_final, thisApp.missed_final = \
                                                  format_triplets(v,y,q,x,not_part)
                    i = i + 1
                    
        if thisApp.option2 ==1:
            drawclass(self.parent, thisApp.formatted_pairs_final, thisApp.missed_final)
        else:
            drawclass(self.parent, thisApp.formatted_groups_final, thisApp.missed_final)
        
    def new_class(self):
        x.clear()
        y.clear()
        v.clear()
        q.clear()
        not_part.clear()
        self.frame.destroy()
        Ask_for_File(self.parent)
        
    def new_options(self):
        self.frame.destroy()
        Offer_Options(self.parent)
          
def main():
    root = Tk()
    thisApp(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()