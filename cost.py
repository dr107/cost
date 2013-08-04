#! /usr/bin/env python

import sys,os,time,locale
import cPickle as p
from datetime import date, timedelta, datetime
#fName='/home/dan/cost/.cost_save'
YR=time.strftime('%Y')#'2013'
MONTHS=['January', 'February', 'March', 'April', 'May', 'June',\
	'July', 'August', 'September', 'October', 'November', 'December']
SMONTHS=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
DAYS=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
SDAYS=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

"""
TODO:
#prompt the user for category if none is given
#print -c
#better option parser?
make sure all features actually fucking work
make a substantial sample save file for me/other people to play with
port this shit to windows
#rewrite README.md to account for the release features.
"""

def findDay(day):
    assert day in DAYS, "wtf man"
    """Given that day is a day of the week, find the most recent day, in the form of a datetime object"""
    #myday=time.localtime()
    l=getTime(7)
    for date in l:
        if date.strftime('%A')==day: return date
    else: return time.localtime()

def rmday(d, l):
    """d is the dict. l a list of strings. It can either be ['Weekday'], ['Month', 'Date'],
    ['Month', 'Date', 'Year']. Entirely remove the day from the record"""
    #assert l[0] in DAYS or l[0]+' '+l[1] in d.keys() or l[0]+' 0'+l[1] in d.keys(), '\n\ncheck yo self'

    l[0]=l[0].title() 
    if l[0] in SMONTHS: l[0]=MONTHS[SMONTHS.index(l[0])]
    if l[0] in SDAYS: l[0]=DAYS[SDAYS.index(l[0])]

    if l[0] in MONTHS: del d[l[0]+' '+l[1]+' '+(l[2] if len(l)>2 else YR)]
    elif l[0] in DAYS: del d[findDay(l[0]).strftime('%B %d %Y')]

def remove(d, l):
    """Interactively correct mistakes with the user. l can either be ['Weekday'], ['Month', 'Date'],
    ['Month', 'Date', 'Year'] """
    #assert l[0] in DAYS or l[0]+' '+l[1] in d.keys() or l[0]+' 0'+l[1] in d.keys(), '\n\ncheck yo self'


    l[0]=l[0].title()
    if l[0] in SMONTHS: l[0]=MONTHS[SMONTHS.index(l[0])]
    if l[0] in SDAYS: l[0]=DAYS[SDAYS.index(l[0])]

    if l[0] in MONTHS:
        x=date(int(l[2] if len(l)>2 else YR), int(l[0]), int(l[1]))
    elif l[0] in DAYS:
        x=findDay(l[0])
    else: raise KeyError()
    
    s=x.strftime('%B %d %Y')
    print s
    t=list(d[s])
    for i in range(len(t)):
        print '   '+str(i)+'--'+t[i][t[i].find(';')+2:]
    ind=int(raw_input('Which cost would you like to remove?\n'))
    t.pop(ind)
    d[s]=tuple(t)
    #>this line
    #>costanza.jpg
    #d[l[0]+' '+l[1]+' '+(l[2] if len(l)>2 else YR) if l[0] in MONTHS else findDay(l[0]).strftime('%B %d %Y')]=tuple(t)



def getTime(j):
    """
    Return a list of datetime objects representing j days back from today

    """

    l=[]
    day=date.today()
    for i in range(j):
        l.append(day)
        day-=timedelta(1)
    l.reverse()
    return l
            

def _printWkdays():
    """Print the days of the week. Testing purposes only."""
    l=getTime(7)
    for day in l:
        print time.strftime('%A %B %d %Y',day)
    print

def printData(data, cat=False):
    """
    Print the data with pretty formatting. Eg:

    Monday, July 22
       coffee: 2.11
       ...

    Print the year as well if it's not this year.
    """
    for d in data:
        print d[0].strftime('%A, %B %d') if d[0].strftime('%Y')==YR else d[0].strftime('%A, %B %d %Y')
        for d1 in d[1]:
            c=d1.split(';')[0].title()
            c='('+c+') '
            print '   '+(c if cat else '')+d1[d1.find(';')+2:d1.rfind(':')].title()+': '+locale.currency(float(d1[d1.rfind(':')+2:]))

def printDay(d, day, cat=False):
    """Print the given day with pretty formatting. """
    data=getData(d)
    day[0]=day[0].title()
    if day[0] in SMONTHS: day[0]=MONTHS[SMONTHS.index(day[0])]
    if day[0] in SDAYS: day[0]=DAYS[SDAYS.index(day[0])]

    if day[0] in DAYS:
        s=findDay(day[0]).strftime('%B %d %Y')
        spl=s.split(' ')
        x=date(int(spl[2]), int(MONTHS.index(spl[0]))+1, int(spl[1]))
    else:
        #s=day[0]+' '+day[1]+' '+(day[2] if len(day)>2 else YR)
        x=date(int(day[2] if len(day)>2 else YR), int(MONTHS.index(day[0]))+1, int(day[1]))
    data=[da for da in data if da[0]==x]
    printData(data)
    
def printItem(d, item, ndays):
    """Print all days in which an item occurs, and the occurances of that item.
    This implementation is really nasty, but it works."""
    data=getData(d)
    if ndays>0: data=[x for x in data if x[0] in getTime(ndays)]
    for thing in data:# thing: (datetime, (costs))
        for cost in thing[1]:
            if cost.split(' ')[0][:-1]==item:
                print thing[0].strftime('%A, %B %d')
                for c in thing[1]:
                    if c.split(' ')[0][:-1]==item:
                        print '   '+c[c.find(';')+2:]

def sumItem(d, item, ndays=-1):
    """Sum all expenses for a certain item and return it as a float.
    l is either [item], or [-w, item]"""
    data=getData(d)
    if ndays>0: data=[x for x in data if x[0] in getTime(ndays)]
    res=0.0
    for t in data:
        for cost in t[1]:
            s=cost[cost.find(';')+2:cost.find(':')]
            if s==item.title() or s==item:
                res+=float(cost.split(' ')[-1])
    return res
    
def getData(d):
    """Take the dict. Return a really compelex data structure of the form:
    [(datetime,(costs...)), ...], where datetime is a datetime object.
    The list is sorted by date."""
    data = [(datetime.strptime(k, '%B %d %Y').date(), v) 
        for k, v in d.items()]
    data.sort()
    return data

def printAll(d, cat):
    data=getData(d)
    printData(data, cat)

def printTime(d, ndays, cat):
    l=getTime(ndays)    
    data=getData(d)
    data=[d for d in data if d[0] in l]
    printData(data, cat)

def printWk(d, cat):
    printTime(d, 7, cat)

def sumAll(d):
    data=getData(d)
    res=0
    for d in data:
        for cost in d[1]:
            res+=float(cost[cost.rfind(':')+2:])
    return res

def sumTime(d, ndays=7):
    data=getData(d)
    l=getTime(ndays)
    data=[d for d in data if d[0] in l]
    res=0
    for d in data:
        for cost in d[1]:
            res+=float(cost[cost.rfind(':')+2:])
    return res

def addComplete(d, l):
    """Here be over-wrought user input parsing"""
    
    l=[s.title() for s in l]
    if l[0] in SMONTHS: l[0]=MONTHS[SMONTHS.index(l[0])]
    if l[0] in SDAYS: l[0]=DAYS[SDAYS.index(l[0])]
    
    if l[0] in MONTHS:
        if len(l)==6: # year and category given
            addRetro(d, l[0], l[1], l[3], l[4], l[2], l[5].title())
        elif len(l)==5:
            # year or category given
            try: # year given
                y=int(l[2]) # see if it's a valid year. If not, assume it's an item
                y=str(y)
                catSug=getMostRecentCat(d, l[3])
                category=raw_input("Type the category of this item (hit enter to put it in "+catSug+")\n")
                addRetro(d, l[0], l[1], l[3], l[4], y, category.title() if category!='' else catSug)
            except ValueError: #category given
                addRetro(d, l[0], l[1], l[2], l[3], YR, l[4].title())
                                    
        elif len(l)==4: # neither year nor category given
            catSug=getMostRecentCat(d, l[2])
            category=raw_input("Type the category of this item (hit enter to put it in "+catSug+")\n")
            addRetro(d, l[0], l[1], l[2], l[3], YR, category.title() if category!='' else catSug)
        else:
            print 'Something is wrong with your input.\nCheck README.md for more details'
    
    elif l[0] in DAYS:
        day=findDay(l[0]).strftime('%B %d %Y').split(' ')
        if len(l)==3:
            catSug=getMostRecentCat(d, l[1])
            category=raw_input("Type the category of this item (hit enter to put it in "+catSug+")\n")
            addRetro(d, day[0], day[1], l[1], l[2], day[2], category.title() if category!='' else catSug)
        elif len(l)==4:
            addRetro(d, day[0], day[1], l[1], l[2], day[2], l[3].title())
        else:
            print 'Something is wrong with your input.\nCheck README.md for more details'

    else:
        if len(l)==2:
            catSug=getMostRecentCat(d, l[0])
            category=raw_input("Type the category of this item (hit enter to put it in "+catSug +")\n")
            addCost(d, l[0], l[1], category.title() if category!='' else 'Misc.')
        elif len(l)==3:
            addCost(d, l[0], l[1], l[2].title())
        else: 
            print 'Something is wrong with your input.\nCheck README.md for more details'

def addRetro(d, mon, date, name, price, year, cat):
    s=mon+' '+date+' '+year
    if s not in d.keys():
        d[s]=(cat+'; '+name+': '+price,)
    else:
        d[s]=tuple(list(d[s])+[cat+'; '+name+': '+price])
        
def addCost(d, name, price, cat='Misc.'):
    if today() not in d.keys():
        d[today()]=(cat+'; '+name+': '+price,)
    else:
        d[today()]=tuple(list(d[today()])+[cat+'; '+name+': '+price])
    
def today():
    return time.strftime('%B %d %Y')

def mkPickle():
    p.dump({}, open(fName, 'wb'))

def startup():
    global fName
    fName=os.path.dirname(os.path.realpath(__file__))
    fName+='/' if os.name=='posix' else '\\'
    fName+='.cost_save'

def getCatSet(d, ndays=-1):
    """Return a set of the categories present in d """
    s=set()
    data=getData(d)
    if ndays!=-1:
        l=getTime(ndays)
        data=[x for x in data if x[0] in l]
    for t in data:
        for cost in t[1]:
            s.add(cost.split(';')[0].title())
    return s
        
def sumCat(d, cat, ndays=-1):
    """Return the sum of all expenses in category cat ndays back from today.
    If ndays is -1, sum over all time"""
    res=0.0
    data=getData(d)
    if ndays!=-1:
        l=getTime(ndays)
        data=[x for x in data if x[0] in l]
    for t in data:
        for cost in t[1]:
            if cost.split(';')[0].title()==cat:
                res+=float(cost.split(' ')[-1])
    return res
                
def breakdown(d, ndays=-1):
    tot=sumTime(d, ndays) if ndays>0 else sumAll(d)
    s=getCatSet(d, ndays)
    s=list(s)
    l=[]
    for el in s:
        l.append(sumCat(d, el, ndays))    
    print 'Breakdown of costs over '+('the last '+str(ndays)+' days' if ndays>0 else 'all time')+' by category:'
    print 'Total expenses: '+locale.currency(tot)
    for i in range(len(s)):
        print '   '+s[i]+' constituted '+str(round((l[i]/tot*100),2))+'% ('+locale.currency(l[i])+')'
        
def parseOpts(av):
    """Parse options into a set of characters """
    se=set()
    for s in av:
        if s[0]=='-':
            s=s[1:]
            for char in s:
                se.add(char)
    
    return se

def getMostRecentCat(d, name):
    """If name is an entry in d, return the last category 
    it was entered in, otherwise return 'Misc.' """
    data=getData(d)
    data.reverse()
    for t in data:
        for cost in t[1]:
            if cost[cost.find(';')+2:cost.rfind(':')].title()==name.title():
                return cost[:cost.find(';')]
    return 'Misc.'

if __name__=='__main__':
    startup()
    if not os.path.isfile(fName): mkPickle()
    d=p.load(open(fName,'rb'))
    locale.setlocale( locale.LC_ALL, '' )
    ops=parseOpts(sys.argv)
    #print d
    if len(sys.argv)==1:
        print 'Usage: cost [command] [options] [arguments]'
        print 'See README.md for more details'

    elif sys.argv[1]=='add':
        addComplete(d, sys.argv[2:])
        
    elif sys.argv[1]=='print': 
        sys.argv=filter(lambda s: s[0]!='-', sys.argv)
        if len(sys.argv)==2:
            if 'w' in ops: printWk(d, 'c' in ops)
            elif 'm' in ops: printTime(d, 30, 'c' in ops)
            else: printAll(d, 'c' in ops)
        elif sys.argv[2].title() in (MONTHS+DAYS+SMONTHS+SDAYS):
            printDay(d, sys.argv[2:], 'c' in ops)
        else:
            printItem(d, sys.argv[2], 'w' in ops)

    elif sys.argv[1]=='sum':
        sys.argv=filter(lambda s: s[0]!='-', sys.argv)
        if len(sys.argv)==2 and 'w' in ops:
            print 'Weekly total: $'+str(sumTime(d, 7))
        elif len(sys.argv)==2 and 'm' in ops:
            print 'Monthly total: $'+str(sumTime(d, 30))
        elif len(sys.argv)>2:
            if 'w' in ops:
                print 'Total spent on '+sys.argv[2]+' this week is: '+\
                    locale.currency(sumItem(d, sys.argv[2], 7), grouping=True)
            elif 'm' in ops:
                print 'Total spent on '+sys.argv[2]+' this month is: '+\
                    locale.currency(sumItem(d, sys.argv[2], 30), grouping=True)
            else:
                print 'Total spent on '+sys.argv[2]+' is: '+locale.currency(sumItem(d, sys.argv[2]), grouping=True)
        else:
            print 'Grand total: $'+str(sumAll(d))

    elif sys.argv[1]=='breakdown':
        if 'w' in ops or 'week'==sys.argv[-1]: breakdown(d, 7)
        elif 'm' in ops or 'month'==sys.argv[-1]: breakdown(d, 30)
        else: breakdown(d)

    elif sys.argv[1]=='rm-entry':
        remove(d, sys.argv[2:])

    elif sys.argv[1]=='rm-day':
        rmday(d, sys.argv[2:])

    elif sys.argv[1]=='clear-record':
        yn=raw_input("This command clears all records of your expenses to this point.\n"+\
                         "The record as it stands will be stored in the cost directory as <dir>/.cost_old\n"+\
                         "If you're hell-bent on expunging all records, delete that file manually\n"+\
                         "Are you sure you want to proceed [y/N]\n"
                     )
        if yn.lower()=='y':
            p.dump(d, open(fName[:fName.rfind('/')]+'/.cost_old' if os.name=='posix' else fName[:fName.rfind('\\')]+'\.cost_save', 'wb'))
            d={}
            
    else:
        print 'Usage: cost [command] [options] [arguments]'
        print 'See README.md for more details'
        
    p.dump(d, open(fName, 'wb'))
