# CPSC 471: Programming Assignment
A simplified FTP server and client using socket programming.

## Names and email addresses
- Anar Otgonbaatar anarotgo@csu.fullerton.edu
- Jose Gonzalez jgonzam@csu.fullerton.edu
- 
- 

## Language


## How to execute
Start two terminals in VS code

naviate each to the folder:
cd sendfile

for the first terminal (and to start the server), enter:
py sendfileserv.py 1234

for the second terminal (start the client), enter:
py sendfilecli.py 127.0.0.1 1234

use the various commands on the client terminal:
fpt> ls           (see the files in the folder)
ftp> get file.txt (retrieve a file from the server)
ftp> put file.txt (send a file from the client)
fpt> quit         (quit session)




## Notes
server and client can communicate, must put sendfileserv.py and sendfilecli in each of their own seprate folders, and transfer a file between them.
