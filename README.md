# Students' Dorms Website

## Why did I create the project?
There is an xlsx file that describes where every student resides.
This file is unorganized, complex to read and understand for students and also hard to manage.

## My solution
My solution is to create a website for the dorms that will organize the way people can view where they reside in the dorms
and organize the way the responsible guy on this website manages it.

## What does the website include
This homepage will include the buildings in the dorms.
Each building is a section that has its own apartments.
Every apartment data is shown in a modal.
Every modal includes:
- apartment number
- apartment gender
- number of bedrooms in the apartment
Every bedroom has a number of bunk beds and regular beds(known as aminach beds) and every bed will include a person sleeping on that bed, so that's how you will know who resides in which room. 
After all that, there is a filter option near the building sections.

Second of all, there is the residents page known as "/residents" that will include all the existing residents known on the website which we can then easily embed to each room (notice that a resident can only be embedded in one bed at a time and can not be embedded in two or more beds, no matter which room or apartment or building at the time). A resident will have the following data - serial number, full name, frame(to know to which class he belongs), gender, distance(to know the indication of how far physically he is from the dorms), entering date(when he first entered the dorms) and eventually exiting date(when he will leave the dorms).

The residents page will also have a filter section.
We will be filtering by: 
- Full name
- Frame
- Gender
- Distance
- Entering and exiting date.

## Technologies
The website was built using Python (Flask, wtforms, sqlite3), HTML (Including bootstrap for decorations), Javascript and SQL.
