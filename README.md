NOTE: CSV data files for training and testing data must be added to project folder manually due to file sizes.
NOTE: RealTimeObjectDetection folder for training and testing model must be added to project folder manually due to file sizes.

# Audible ON

***
## Table of Contents
1. [Project Overview](#project-overview)
    * [Our Vision](#our-vision)
    * [Key Features](#key-features)
    * [Known Bugs and Limitations](#known-bugs)
2. [Technologies](#technologies)
3. [Build, Install, and Run New Releases](#new-releases)
    * [Configure Environment](#configure-env)
    * [How to Download and Install New Release](#download-install-release)
    * [How to Run New Release](#run-release)
4. [Team Contributions](#team-contributions)
    * [Meet Our Team](#team)
    * [Contributions](#contributions)
5. [Resources](#resources)



***
<a name = "project-overview"></a>
## Project Overview
Audible ON is an application that utilizes the client’s camera on their device to record and translate gestures from the American Sign Language (ASL) into legible text and/or audible speech, and vice versa (from either text or speech to ASL). Both hearing impaired and non-hearing impaired clients will be able to use this application to communicate with one another in a variety of situations. Audible ON utilizes several other libraries and computing systems such as Google MediaPipe and a Convolutional Neural Network (CNN) to add additional features that will allow user flexibility. Such features will be listed below in the features list.

As technology and medicine advance each year, communication between hearing impaired and non-hearing impaired individuals needs improvement to communicate. Audible ON seeks to allow both groups to communicate with each other without the need for an interpreter. Audible ON’s goal is to allow the hearing impaired to assimilate into society easier by communicating with the general public just as easily as the general public communicates with each other without the need for a live interpreter.

<a name = "our-vision"></a>
### Our Vision
Our vision for this project is to be a truly inclusive project that will allow members of a frequently overlooked and unheard community be able to communicate and utilize technology designed with their needs prioritized.

<a name = "features"></a>
### Key Features
The AudibleON Platform is equipped with the following features:
* Real time sign language words/phrases detection of with a CNN model of trained on the following phrases: 'I love you', 'telephone', 'hello', 'yes', 'no', 'stand', 'mom', 'I'
* Real time sign language letter detection using Google MediaPipe
* ASL to text output with translated audio on Flask Application
* Text to ASL output with translated input into video playlist in ASL
* Audio to ASL output with transcribed input used for creation of video playlist in assimilate
* User account creation and management with MySQL database
* Connect online feature to support web chat with messages translated from input ASL to text, and input text or audio to ASL. Supports multiple users simultaneously on the platform.
* Help page with instructions for using each feature in the application
* Mobile application connected to Flask app and database to allow users to log in from their phone

***
<a name = "known-bugs"></a>
### Known Bugs and Limitations
* Lighting and latency impacts for the CNN model result in only a few of the trained phrases being able to be detected
* CNN model when first activated on user account takes some time to start up, and results in a backlog of frames on the camera class's 'to process' stack. The 'Restart' button was used to clear the stack and avoid latency impacts.
* Application error when user attempts to create account with email associated with previously registered account.
* Videos for text to ASL are not preloaded when retrieved from the server despite preload statements.
* Audio file for audio to ASL does not alert user when time out occurs.
* Deployment to AWS EC2 instance was attempted but while the majority of the Flask application was workable, the integration of the models onto the server resulted in significant errors that crash the server. To demonstrate the application's ability to serve multiple users, Ngrok was used during the demo and is recommend to create a reverse proxy for users to log onto the application as it runs on a local host.
* Text to ASL feature does not give output in 'true' ASL form; to be more accurate to the needs of the deaf community, a robust natural language processing algorithm would need to be developed to capture the variety of grammatical rules used in constructing ASL sentences.
* Deaf users in the chat room are unable to text their communication to other users and are limited only to the translated output from both the alphabet and the CNN models.
* Login flashed message does not appear on Translate page immediately after logging in, but instead appears on next page that is accessed right after leaving the Translate page.

***
<a name = "technologies"></a>
## Technologies
* Jupyter Notebook for training and testing models
* Pycharm IDE

### Libraries
Many libraries were utilized in the development of this project, and can be found in the ```requirements.txt``` file within the repository.
* Google's MediaPipe
* Keras
* NumPy
* OpenCV
* Tensorflow

***
<a name = "new-releases"></a>
## Build, Install, and Run New Releases
<a name = "configure-env"></a>
### Configure Environment
In order to prepare your environment for building and running the AudibleON program, please follow [these detailed instructions](https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html) for the creation of your environment to utilize the Tensorflow Object Detection API. For this project, Tensorflow v2.8.0 was used and can be installed on Windows or Linux following the above tutorial. If you do not have CUDA compatible GPU, that section of the tutorial can be skipped. Be sure to run the necessary installation confirmation commands listed in the document to confirm that you have correctly installed Tensorflow.

Following the installation of Tensorflow and its necessary additional packages, please install the rest of the packages necessary in your Python environment using the following command with the requirements.txt file found in the repository.
If using pip: ```pip install -r requirements.txt```
If using conda: ```conda install --file requirements.txt```

Following the successful installation of these packages, with your environment activated, navigate to the ```project-audibleon``` folder and execute ```python main.py```. Throughout the development process, the program was built and run JetBrains' PyCharm IDE, where it can similarly be run with the Python interpreter configured to match the virtual environment containing the packages necessary for its execution.

To open the application with a reverse proxy (as demonstrated in the demo), ngrok can be used; to begin, set up a user account and password for your associated account [here](https://ngrok.com/). Follow the instructions to authenticate your account through the command line. When complete, enter the following command in the terminal to activate the reverse proxy: ```ngrok http 5000```. After starting up the AudibleON application using the instructions in the previous paragraph, follow the link generated in the terminal for the ngrok command to access the site online from any device.

Releases:
[v0.1.0-beta Audible ON Software Pre-Release](https://github.com/Capstone-Projects-2022-Spring/project-audibleon/releases/tag/v0.1.0-beta)

<a name = "download-install-release"></a>
### How to Download and Install Mobile App Release
Included in our latest pre-release v0.1.0-beta is an apk file corresponding to our current version of our mobile application. On your Android device, click on the apk file provided in the release to begin downloading and installation. We recommend using SAI apks installer, however any installer recommended by android upon clicking on the file will suffice. As this mobile application is not setup officially with android, there will be warnings regarding android's lack of knowledge of the developer and the potential dangers of installing an app with an unknown author. These warnings are safe to be ignored to proceed with the installation process.

<a name = "run-release"></a>
### How to Run Mobile App Release
After the app is officially installed on your android device you can open it simply by clicking on the app icon in your apps folder. Once you have done so you can begin navigating the app and its minimal features. For example, by clicking 'Start', you will be taken to the 'Login' page, and by clicking 'Create an account' on that 'Login' page, you will be taken to a 'Sign Up' page. Both pages currently lack registering or logging in functionality, however for purposes of testing navigation, feel free to click the 'start' button. By clicking the 'Skip' button, you will navigate to the 'Home' page. It is on this page that only the 'Start Translation', 'Web Application', and 'Exit' buttons are functional. By clicking the 'Start Translation' button you will be directed to a 'Translation' page where you will be prompted with permission request to use your camera. By allowing access, you can then click on the toggle switch in the top right of the page to open the camera. If you are not seeing frames, it is recommended that you press the back button on the page and click the 'Start Translation' button again to resolve said conflict. Once you are seeing frames, you can either display frames in RGB (color) or grayscale by clicking on the word button in the top left part of the 'Translation' page. You can stop reading frames by clicking on the toggle switch again to move the slider back to its original position. Do this as many time as you would like. You can return to the 'Home' page by clicking the back button on the 'Translation' page or by using your device's back functionality. Once there you can view our currently deployed web application and click on some menu options to attempt to access other pages. Finally, by clicking the 'Exit' button on the 'Home' page, you can close out of the entire app.

***
<a name = "team-contributions"></a>
## Team Contributions

<a name = "team"></a>
### Meet Our Team
#### [Shakirah D. Cooper](https://github.com/ArchaePi)
#### [Rachel Lazzaro](https://github.com/rlazz)
#### [Ben Westburg](https://github.com/tun60968)
#### [Mahmood Ahmed](https://github.com/RaymondLaubert)
#### [Juan-Carlo Villamor Mercado](https://github.com/JC-127)
#### [Raymond Laubert](https://github.com/MoodAhmed)


***
<a name = "resources"></a>
## Resources
The following resources were used for the completion of this project.
https://google.github.io/mediapipe/solutions/hands.html </br>
https://github.com/google/mediapipe/</br>
https://github.com/nicknochnack/RealTimeObjectDetection</br>
https://www.signasl.org/ </br>
***
