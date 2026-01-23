# Face Recognition System 

A real-time Face Recognition system built with Python. This project allows you to register authorized users and automatically detects whether a person in front of the camera is a **known User** or a **Stranger**.

## Key Features

* **Real-time Detection:** Identifies faces instantly using webcam feed.
* **Add New User:** Easy process to register new faces into the database.
* **Stranger Alert:** Automatically labels unregistered faces as "Stranger" or "Unknown".
* **User Validation:** Matches detected faces against the stored dataset.

## Screenshots

| Registering User | Recognizing Face | Stranger Detection |
| :---: | :---: | :---: |
| ![Register](./assets/Screenshot%20from%202025-12-12%2018-06-05.png) | ![Recognize](./assets/Screenshot%20from%202025-12-12%2018-06-16.png) | ![Stranger](./assets/Screenshot%20from%202025-12-12%2018-06-43.png) |


## Dependencies

To run this project, you need Python installed along with the following libraries:

* opencv-config-python
* numpy
* pillow

## Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/username/face-recognition-system.git
    cd face-recognition-system
    ```

2.  **Install requirements**
    ```bash
    pip install -r requirements.txt
    ```

## Usage
```bash
python3 1scanning.py
```

## How to run the program

### 1. Add a New User
Choose 1 to run the registration script to capture a face and save it to the database. Then press 'q' to finish it.
### 2. Recognizing face
Choose 2 to try system to recognize the face who added in step 1, if the face is register the "owner" will show up, if not "stranger" will show up. Then press 'q' to finish it.
### 3. Close Program
Choose 3 to close the program

