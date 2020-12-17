# Purposeful Groups

(A stand-alone app)

### Intuitive group randomizing app that incorporates student preferences and teacher objectives

## Table of Contents
* [Background](#Background)
* [Features](#Features)
* [Technologies Used](#Technologies-Used)
* [Functionality](#Functionality)
* [Design](#Design)
* [Running Locally](#Running-Locally)

## Background
Our school was investigating ways to help students better learn and apply 21st Century Skills like critical thinking, collaboration, communication, and problem solving to their coursework.  My personal experience with group work as a student in school was rarely positive.  One or two people did the work while the others socialized.  On the other hand, I had some experiences as an adult where collaboration had led to new insights and better products.  If students knew how to work well together like that, they might be able to reach deeper understandings of mathematical concepts and have the support they needed to become effective problem solvers, communicators, and collaborators rather than just apply memorized procedures.

I also read a study about how students don't tend to mix outside of their friend groups, which makes sense.  However, it means that students are not learning how to communicate and work with people who are different from them, especially with people who have skin color different from their own.  We teachers have been trying to identify and change the systemic racism in our school and society in any way we can.  Increasing opportunities for students to have positive collaborative experiences with ALL of their classmates seems like a small step toward decreasing inequities.

How do I, as a teacher, facilitate group work so that it contributes positively to student learning and relationships?  Beyond all the strategies one can read in articles and books, at some point the teacher has to assign students to groups (or let them self-select, but that means they are back with their friends again).  Random groups are often suggested.  If they are changed frequently, then students know they only have to put up with someone in their group for a short time if they happen not to like them.  But any teacher can probably attest that there always seems to be some combination of students that just really cannot function together.  To try to keep track and check for those combinations every time a random group is formed is one more thing on top of all the others that a teacher needs to track.  Furthermore, I was afraid that the navigation of social relationships (especially in middle school) would often use up too much of students' brainspace leaving less for learning the math concepts that are our focus.  

What I needed was a tool that could randomize groups while also taking into account some student preferences and my teacher goals for an activity.  The Purposeful Groups App was my answer.  I collected data from students in each class about their past experiences working with each of their classmates.  When students work on a low risk activity like comparing homework answers to create a group answer page (with the option for any member to disagree with an answer in the end), I use the "New Partners" setting.  The app starts with pairs of students who report not having worked together, randomizing them into the requested group size, and then filling in with students remaining.  When students are going to work on a challenging math task and thus need to be comfortable sharing their ideas and questions, I use the "Preferred Partners" setting.  The app starts with pairs of students who report that they work well together, randomizing them into the requested group size, and filling in with remaining students.  Students who cannot function well together often self-report on the survey or I go in and update the data as needed; the app avoids putting those students together.

## Features
* Uses data collected through student surveys
* Accepts input from teacher with regard to group size (2, 3, or 4)
* Accepts input from teacher about whether to create groupings of students who haven't worked together much or who really work together well
* Accepts input about students who should not be included for that day's grouping (absent or opting out of groupwork for some reason)
* Creates random groups BUT first sorts pairings according to criteria
* Displays groups in a seating arrangement format so students will know where to sit and who their groupmates are
* Displays names of anyone who has not been placed in a group (due to class number not evenly divisible by group size)
* Display size can be increased/decreased for visibility
* Buttons to allow for easy re-randomization and returns to choosing class data or options
* Stand alone app that can be easily installed on teacher's computer and not dependent on internet nor risking any student data on the internet (other than the original survey done through Google Forms)

## Technologies Used
* Python -- I don't remember why I chose this language.  I knew nothing about languages and their benefits or drawbacks.  I was able to find some books about getting started with Python, so I gave it a try.
* Pandas -- I wanted to be able to use data from a spreadsheet.  In my research, this was the library that surfaced.
* Tkinter -- I needed some GUIs for the teacher to use and final groups to be displayed.  This library enabled me to create a somewhat responsive final classroom seating arrangement.
* PyInstaller -- I wanted an easy way to install and access my app on a school computer.  This tool allowed me to package everything into one executable file.
* Google Apps Script -- Creating the survey forms for each of my classes was time-consuming and error prone.  Writing a script streamlined the creation of these Google Forms.
* HTML, CSS, JSON -- all used in writing the survey form creation script
* Google sheets/Excel spreadsheets -- Google Forms returns the data in spreadsheet form.  I prefer Excel.

## Screenshots

![Select datafile](/images/choose_file.png?raw=true "Choosing a Datafile")
![Teacher Options](/images/teacher_options.png?raw=true "Teacher Options")
![Pairs](/images/pairs.png?raw=true "Pairs")
![Groups of 3](/images/groups_of_3.png?raw=true "Groups of 3")
![Groups of 4](/images/groups_of_4.png?raw=true "Groups of 4")

## Functionality
When started, the app asks the user to select a data file.  With Python and pandas being new to me and knowing I would be the only user, I didn't take the time to figure out how to fully clean the data that is returned from the survey.  It seemed more efficient for this first version if I took care of those steps by hand in the Excel file.

The next screen allows the teacher to check the names of any students who are absent or not participating.  The teacher also selects whether groups should consist of 2, 3, or 4 people.  Finally, the teacher indicates whether the app should prioritize pairings of students who have not worked much together (New Partners) or pairings of students who work well together (Preferred Partners).

The app creates the groups and displays them in a seating arrangement configured for my classroom.  Allowing a teacher the flexibilty to change the classroom layout is one feature that would be nice to add.  At the bottom of the screen, the app lists the names of any students who still need a group.

The classroom layout screen has 2 buttons to allow for zooming in and out.  There is a button for randomizing the groups according to the same settings as well as a button for returning to the settings screen in order to change them.  Another button leads to the selecting class data interface. 

## Design
Frankly, I was so excited just to have created something that worked!  There is a lot of room for improvement in the aesthetics of this app. I am sure the code needs to be refactored in a huge way. First, though, I wanted to test it in the classroom to see what I liked and didn't.  Teaching does not leave enough time and energy for a project like this, so any updates needed to wait until summer 2020.  And then COVID hit.

When we finally reach post-COVID and there's a possibility that one or more teachers would find an app like this useful, I would love to refactor and improve it.  

## Running Locally
Option 1:
*  Download PurposefulGroups.exe and the SampleDataColors.csv. files
*  Run PurposefulGroups

Option 2:
* Clone
* Install
* Run PurposefulGroups.py


