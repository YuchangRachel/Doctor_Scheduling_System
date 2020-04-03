# Online medical appointment system Project
## Aim of the project:
Simulation of an online medical appointment system using a hybrid architecture of TCP and UDP sockets.

## Project Description:
The program runs in 3 phases: user authentication, scheduling an appointment at an available time, getting estimated cost of visit from the scheduled doctor by sending insurance information.
We have the health center server for authenticating users and reserving time slots, 2 patients and 2 doctors.
Communication between the health center server and patients in the first 2 phases is through TCP sockets. In the last phase, communication between the doctors and the patients is through UDP sockets.

In the first phase, patients connect with the health center server on a static port using TCP socket. On successful authentication by the server, they can continue to phase 2 and ask for available time slots for appointment.

In the second phase, the server will send a list of available time slots to the patient. The patient chooses one time slot and, if that has not already been reserved, that slot is reserved for the asking patient. The server sends doctor's port number, associated with that time slot, on which the patient will now connect in phase 3.

In the third phase, the patient sets up a Bidirectional UDP connection with the stipulated doctor on the received doctor port number. The patient sends his insurance information to the doctor, who replies on the same UDP port with the estimated cost of the visit related to that insurance.

## Files:
1. healthcenterserver.py - This is the code for the health center server. It reads the username and password information of authentic users from users.txt and the availabilities and doctors's information from availabilities.txt. It is responsible for authenticating the patients, scheduling appointments and sending doctors's information to them. <br />
2. doctor1.py - This is the code for Doctor 1. It reads Insurance information from doc1.txt and sends the estimated cost of visit associated with each insurance type to the patients.<br />
3. doctor2.py -  This is the code for Doctor 2. It reads Insurance information from doc2.txt and sends the estimated cost of visit associated with each insurance type to the patients.<br />
4. patient1.py - This is the code for Patient 1. It reads username and password of patient 1 from patient1.txt and the type of insurance from patient1insurance.txt. It communicates with the health center server on a dynamic TCP port and with the doctors on a dynamic UDP port.<br />
5. patient2.py - This is the code for Patient 2. It reads username and password of patient 2 from patient2.txt and the type of insurance from patient2insurance.txt. It communicates with the health center server on a dynamic TCP port and with the doctors on a dynamic UDP port.
<br />

## To run the program:
The processes must be run in the following order in terminal:
healthcenterserver.py > doctor1.py = doctor2.py > patient1.py = patient2.py

## For compilation :
After editing python file, should write a command line:chmod u+x filename in certain directory in terminal

## After clean compilation, run the code:
./filename

## need optimize
should show updated time schedule to patients??
