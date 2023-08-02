Author: Alistair Bevan
Date: 2023-08-02

Hall Measurement System
Supplementary Details


Overview:
This file contains supplementary information to go alongside the Hall_GUI_documentation file. It outlines the procedure for cloning the
git repository to the new lab computer account, and syncing the local repository (on the lab computer) with the remote repository (on GitHub).
I am by no means a pro at using GitHub, so these are just one set of instructions to get to the desired results; they may not be the most
efficient or best methods. Details of important updates will also be included here.

Installation Instructions:
1. If git is not installed, get it from https://git-scm.com/downloads.
2. Go to the location on your computer you would like the repository to be in, right-click and select "Git Bash Here". It may look slightly
   different and you may need to click "Show more options" to see it.
3. Type "git clone -b branch-name https://github.com/AlistairBevan/Hall.git" to clone the repository. Replace "branch-name" with the branch you
   would like to be on. For instance, mocvd-updates is the most up to date branch.
4. To run the program, ensure PyQt5, numpy, PyVisa and PyQtChart are also installed.

Update Instructions:
1. Open the local repository folder (named "Hall"), right-click, and select "Git Bash Here."
2. Check that you are on the correct branch by typing "git branch". To switch branches, type "git checkout branch-name".
3. To update your local repository with the latest changes, type "git pull".

Precautions:
Avoid making code changes in your local repository without being signed into GitHub. This should ensure smooth pushing and pulling of changes.


Updates:
- 2023-08-02: Directories in GUI-main and custom-widgets were changed so that the user is "mocvd"