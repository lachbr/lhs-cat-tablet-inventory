# Tablet Inventory System

This is the new tablet inventory system, used for keeping inventory of all tablets, issues that occur with them, and the students/faculty who use tablets.

## Dependencies
* Python 3
* via pip:
  * pyqt5==5.12.2
  * pywin32
  * pyad
  * panda3d
  * xlwt
  * xlrd
  * pyinstaller
* Qt Designer (for editing the UI)
* nsis

### How to build
1) Ensure all dependencies are installed
2) Ensure current branch is production
3) Ensure client and netclient are set to connect to production server (c2031svcat2)
#### Skip 4-5 if only netclient needs rebuilding
4) Run build_client.bat
5) Run run_genhash.bat
   * Hash built_client\\client.exe
   * Output to built_client\\client_hash.txt
#### Skip 6-7 if only client needs rebuilding
6) Run build_netclient.bat
7) Run run_genhash.bat
   * Hash built_netclient\\netclient.exe
   * Output to built_netclient\\netclient_hash.txt
8) Upload output files (client.exe, client_hash.txt, netclient.exe, netclient_hash.txt) to ftp://c2031snas2/TabletInventory2020
9) Ensure c2031svcat2 has latest commits from production branch

### How to build installer
1) Complete steps 1-8 above
2) Run NSIS gui
3) Use script installer.nsi
4) Build installer
5) Upload installer to ftp://c2031snas2/TabletInventory2020

---

There are 3 parts to it:
* Server
* Client (Students/Faculty)
* Net Client (Net Assistants)

## Server
The server is the central part of the system. Both the client and net client connect to the server and communicate with it. It handles requests from clients to retrieve/update information for a tablet or student, and performs the actual queries on Active Directory and the Inventory database.

## Client
The client is the student/faculty side of the system. Its only purpose is to allow students/faculty to come in, scan their tablet, and submit a new issue (broken tablet form).

## Net Client
The net client is the net assistant side of the system. It allows net assistants to view the entire tablet and student inventories and update information. This part is used to log updates for a tablet issue, assign tablets to students, change whether or not a student has turned in internet agreement forms, etc.

## Active Directory Intertwinement
While there is a dedicated database for storing information specific to the inventory system, all students and tablets already exist in Active Directory. This means we can reference them by their Active Directory GUID and query useful information from there (such as a student's name and email, or a tablet's PCSB tag, etc), rather than duplicating data.

For tablets in Active Directory, the PCSB Tag is encoded in the tablet's CN (Common Name). For instance, a tablet in Active Directory with CN `C2031T0440532` has PCSB Tag `044-0532`. The only information that must be stored directly in our database and does not exist in Active Directory is the tablet's Device Model and Serial Number, which must be manually entered in by net assistants. Information that we store for each Tablet: `Active Directory GUID`, `Device Model`, `Serial Number`

For students/faculty, their names, grade levels, email addresses, and whether or not they are in CAT are already stored in Active Directory. Information that we store for each student: `Active Directory GUID`, `CAT Internet Agreement Turned In?`, `PCSB Internet Agreement Turned In?`, `Insurance Paid?`, `Insurance Paid Amount`. A student that has turned in both internet agreement forms and paid insurance is eligible to be assigned to tablet.

## Student -> Tablet Link
To assign students to tablets, there is a separate database table which simply stores the student's Active Directory GUID, and their assigned tablet's Active Directory GUID. This allows us to look up a tablet by student, or a student by tablet.
