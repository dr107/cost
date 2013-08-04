cost
========

Cost is a command line utility designed to help one track, view, and understand one's daily
expenses quickly and easily. The usage is a tad complex, but if you learn it, you'll be able
to quickly and cleanly record and access your financial information.

The usage is:
    
    cost [command] [options] [arguments]

The commands and their specifications are as follows:

**add:**

Add adds an entry to the record. There are no options.
The arguments are fairly flexible. If you want to add 
an entry for today, type 

    cost add [item] [cost] [category (optional)]

Adding a category will allow you to eventually use the breakdown command, which will give you 
a brief analysis of your expenses. If you do not give this argument, you will be prompted for
it, but if you just hit return, the cost will be put in the 'Misc.' category. 

If you forgot to add an entry, and want to add one for
a previous day, you can type the day first. If you give 
a day of the week, the cost will be added to the most 
recent day. Otherwise, you can give a month and date.
Feel free to use uncapitalized month/day names or 
abbreviations.

So if you want to add a cost for July 22, 2013 (and today is the 23rd), all of these are equivalent:

    cost add Monday coffee 2.11
    cost add mon coffee 2.11
    cost add July 22 coffee 2.11
    cost add jul 22 coffee 2.11
    cost add July 22 2013 coffee 2.11

You get the idea.

**print:**

Prints some portion of the record. It has 3 options, -w, which tells it to 
only print seven days' worth of records, -m, which is the same for a 30 days,
and -c, which tells it to print the categories of the entries.

With no arguments, this will print the entire record in chronological order.
Depending on how long you've been using this, it might be long. However, you can use
the -w and -m options to shorten it to the desired length.

You can also print an individual day's entries using input similar to that in add, i.e.
      
      cost print Monday
      cost print July 22
      cost print July 22 2012
     
etc.


If you give it any other word, it assumes that you are referencing some expense you
want to better understand, and will print all instances of that cost. So, the input

      cost print coffee

will print all instances of coffee in the record.


**sum:**

Gets totals over periods of time. It has two options, -w and -m (which have the same idea they
do in **print**).

With no arguments, it takes the sum of all entries, which may not be very useful. So if
you want your expenses for the week, type
    
    cost sum -w

or use -m for the month.    

Also, similarly to print, if you want to know how much you have spent on a particular item
over time, you can give that item as an argument. So typing

     cost print coffee

Would give you the total cost of coffee since the record has been established.
Also,

     cost print -w coffee

Would do the same for this week.

**breakdown:**

This has the potential to be an extremely powerful tool for understanding your expenses. If you were
dilligent in consistently giving (correctly spelled) category names to **add**, this will give you a
breakdown of the percentages of total expenditures each category occupies. It also has the -w and -m
options if you want to understand the most recent week or month.

Finally:

**rm-entry,** and **rm-day:** **clear-record**:
Correct mistakes. Both of these take a day as an argument (in the same way as add and print).
**rm-entry** will interactively delete a cost with you by numbering the entries for the given day
and asking you for the number of the erroneous entry. **rm-day** will remove a certain day
and all of its entries from the record. 


**clear-record:**
This takes no arguments or options, and simply 
moves your saved record to another file, allowing you to start anew, without destroying it.
Bear in mind that if you do this twice, or delete the old record, it will be lost.