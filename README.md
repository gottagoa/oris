# oris
Website of Oris Clinic 
Medical Clinic 'Oris' is a website with elements of CRM system, designed to organize the work of a medical clinic and improve interaction with patients and specialists.
The project is developed using various technologies such as Django, HTML, CSS, JavaScript and Django REST framework serializers. 
Below are the main functionalities and tools used in the project:

Tools:

Django: A framework for developing web applications in Python.
HTML and CSS: For creating user interface and visual design.
JavaScript: For implementing interactive elements on web pages.
Django REST framework serializers: For converting data between JSON format and Python objects.
Bootstrap: A single-page Bootstrap template was used, which was divided into separate pages and adapted for user-friendliness.
Database: SqLite3

Functionality:

Registration and Authentication:
Users can register on the site using their email.
Email authentication is required for site access.


Profile Management:
Registered users have access to their profiles.
They can edit their data, including contact information and other personal details.
Password changes are also possible.

Admin Panel:
An administrative panel was created, allowing administrators to manage data without code intervention.
All data models, such as specialists, departments, services, and others, are available for editing in the administrative panel.


User Types:
Two user types exist: specialists and patients.
The administrator (superuser) can assign user statuses via the administrative panel.


Personal Dashboard:
Each user (patient or specialist) has their own personal dashboard.
Doctor dashboards differ from patient dashboards.


Specialist Information:
Administrators can input information about specialists, such as education, certificates, work experience, and other characteristics.
This information is available for visitors to the site.


Information about Clinic Departments:
The site presents information about various clinic departments.
Users can view lists of specialists working in each department.


Information about Services Provided:
Lists of services offered by the clinic are displayed.
Reviews:


Users can leave reviews about the clinic's services and individual specialists.
Reviews can be general or linked to a specific doctor.
Reviews include a rating from 1 to 5 stars.
Reviews are displayed in modal windows.


User Interface:
A one-page Bootstrap template was used, adapted for the project.
CSS and JavaScript elements were configured to enhance the visual structure and interactivity of the site.


CRM System Elements:
A feature for scheduling appointments with doctors through the site was added.
Two methods of appointment booking exist: through a doctor's profile and through the main page.
Available doctor hours are considered when booking.


Personal Dashboard:
Doctor dashboards include sections for managing appointment schedules and reviewing patient medical histories.
Patients can view appointment history and medical records.


Frequently Asked Questions Section:
A separate model was created for frequently asked questions and answers.
A limited number of questions is displayed on the main page, with all questions available on a separate page.


Gallery:
A gallery model with images was added.
Administrators can manage the gallery through the administrative panel.


Awards Model:
A model was created to display awards, certificates, and achievements received by the clinic and specialists.


Contact Information:
Contact details are provided on the site, including a Google Maps address with a route, icons for accessing social networks, and contact phone and email.
Serializers:

Django REST framework serializers are used, for example, when booking appointments to exchange data in JSON format. This facilitates interaction with the API and data exchange.
This project offers a wide range of functionality for the clinic, its specialists, and patients, with a focus on user convenience and data management through the administrative panel.
