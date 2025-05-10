# --- DR. PILL GUI with Fingerprint + Facial Recognition Integration ---
from guizero import App, Box, PushButton, Text, TextBox, info, error
import os
import serial
import serial.tools.list_ports
import adafruit_fingerprint
import subprocess
import time
import mysql.connector
import face_recognition
import cv2
import numpy as np
from picamera2 import Picamera2
import time
import pickle
import shutil
import json
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import Label
from imutils import paths  

current_method = "Unknown"  # Default, will be set during login

db = mysql.connector.connect(
    host="172.20.10.4",
    user="useradmin",
    password="12345678",
    database="fingerprint_logs"
)
cursor = db.cursor()
current_popup = None  # <-- Add this near the top of your file (global variable)

def update_datetime():
    now = datetime.now()
    time_str = now.strftime("%I:%M:%S %p")
    date_str = now.strftime("%B %d, %Y")
    datetime_text.value = f"{date_str}   |   {time_str}"
    app.after(1000, update_datetime)  # Update every second


# --- App Config ---
app = App(title="Dr. Pill")
app.fullscreen = True
text_size = int(app.width * 0.03)
spacing = int(app.height * 0.02)
button_height = 7
PASSWORDS = {"Admin": "1", "Staff": "2", "Patient": "3"}
current_popup = None # Handles window popup
current_profile = None  # Handles profile set


# Load pre-trained face encodings
print("[INFO] loading encodings...")
with open("encodings.pickle", "rb") as f:
    data = pickle.loads(f.read())
    known_face_encodings = data["encodings"]
    known_face_names = data["names"]

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

# Initialize our variables
cv_scaler = 4 # this has to be a whole number

face_locations = []
face_encodings = []
face_names = []
start_time = time.time()

# --- USB CDC Setup for STM32 ---
def find_STM32_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "STM" in port.description or "ACM" in port.device:
            return port.device
    return None
STM_port = find_STM32_port()
if STM_port:
    cdc = serial.Serial(STM_port, 115200, timeout = 1)
    print(f"Connected to STM32 via {STM_port}")
else:
    print("STM32 CDC connection failed!")
    cdc = None

# --- Fingerprint Setup ---
uart = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

# --- Fingerprint Scan Text ---
fingerprint_text = Text(app, text="Place Index Finger On Scanner", size=text_size, visible=False)

FINGERPRINT_USERS = {}
FINGERPRINT_FILE = "fingerprint_users.json"

def load_fingerprint_users():
    global FINGERPRINT_USERS
    if os.path.exists(FINGERPRINT_FILE):
        with open(FINGERPRINT_FILE, "r") as f:
            FINGERPRINT_USERS = json.load(f)
    else:
        FINGERPRINT_USERS = {}

def save_fingerprint_users():
    with open(FINGERPRINT_FILE, "w") as f:
        json.dump(FINGERPRINT_USERS, f)

load_fingerprint_users()
# --- Facial Recognition Scan Text ---
facial_text = Text(app, text="Align Face With Camera", size=text_size, visible=False)

# --- Facial Recognition Mapping ---
FACIAL_USERS = {}
FACIAL_FILE = "facial_users.json"

def load_facial_users():
    global FACIAL_USERS
    if os.path.exists(FACIAL_FILE):
        with open(FACIAL_FILE, "r") as f:
            FACIAL_USERS = json.load(f)
    else:
        FACIAL_USERS = {}

def save_facial_users():
    with open(FACIAL_FILE, "w") as f:
        json.dump(FACIAL_USERS, f)

load_facial_users()

PIN_USERS = {}
PIN_FILE = "pin_users.json"

def load_pin_users():
    global PIN_USERS
    if os.path.exists(PIN_FILE):
        with open(PIN_FILE, "r") as f:
            PIN_USERS = json.load(f)
    else:
        PIN_USERS = {}

def save_pin_users():
    with open(PIN_FILE, "w") as f:
        json.dump(PIN_USERS, f)

load_pin_users()


def perform_action(action_name):
    if action_name == "TEST_MOTORS":
        if cdc is None:
            info("Error", "STM32 CDC connection not available.")
            go_back()
            return
        try:
            cdc.reset_input_buffer()
            cdc.write(b"TEST_MOTORS\n")
            start_time = time.time()
            response = "" 
            while (time.time() - start_time) < 15:
                line = cdc.readline().decode(errors="ignore").strip()
                print(f"[STM32] {line}")
                response+=line
                if "MOTOR_TEST_OK" in response:
                    info("Success", "All motors tested successfully!")
                    go_back()
                    return
            info("Error", "Motor test timeout or failed. Check STM32 connection.")
        except serial.SerialException:
            info("Connection Error", "Could not communicate with STM32.")
        go_back()
    else:
        info("Action Completed", f"{action_name} action performed successfully!")
        go_back()
   

def retrain_database():
    train_model()
    info("Success", "Facial recognition database retrained!")

def show_dispense_menu():
    hide_all_screens()
    pill_number_box.value = ""
    pill_count_box.value = ""
    dispense_screen.show()

def send_dispense_command():
    global current_method
    current_method = "Dispense Command"
    
    pill_num = pill_number_box.value.strip()
    pill_count = pill_count_box.value.strip()

    if not pill_num.isdigit() or not pill_count.isdigit():
        info("Error", "Pill number and count must be numbers.")
        return

    pill_num = int(pill_num)
    pill_count = int(pill_count)

    if pill_num < 1 or pill_num > 8 or pill_count < 1:
        info("Error", "Invalid pill number or count.")
        return

    command = f"DISPENSE {pill_num} {pill_count}\n"

    try:
        cdc.reset_input_buffer()
        cdc.write(command.encode())

        while True:
            response = cdc.readline().decode(errors="ignore").strip()
            if response:
                print(f"[STM32] {response}")
                if "DISPENSE_DONE" in response:
                    # ✅ Run conveyor belt before displaying the success message
                    pill_info = f"Pill {pill_num} x{pill_count}"
                    
                    sql = "INSERT INTO login_records (user_id, confidence, status, method, pill_dispensed) VALUES (%s, %s, %s, %s, %s)"
                    values = (0, 0, "Success", "Dispense Command", pill_info)
                    cursor.execute(sql, values)
                    db.commit()
                    
                    perform_action("TEST_MOTORS")
                    info("Success", "Pills dispensed successfully!")
                    break
                elif "INVALID_CMD" in response:
                    info("Error", "Invalid dispense command sent to STM32.")
                    break
    except Exception as e:
        info("Error", f"Failed to communicate with STM32: {e}")

# --- Helper Functions ---
def hide_all_screens():
    global current_popup
    if current_popup:
        current_popup.destroy() 
        current_popup = None

    start_screen.hide()
    main_menu.hide()
    auth_method_screen.hide()
    password_window.hide()
    profile_panel.hide()
    dispense_screen.hide()  
    manage_users_screen.hide()
    add_user_screen.hide()
    remove_user_screen.hide()
    view_user_screen.hide()
    
def switch_panel(profile):
    global current_profile
    current_profile = profile

    hide_all_screens()
    profile_panel.show()
    profile_text.value = f"Welcome, {profile}!"
    admin_options.hide()
    staff_options.hide()
    patient_options.hide()

    if profile == "Admin":
        admin_options.show()
    elif profile == "Staff":
        staff_options.show()
    else:
        patient_options.show()

def logout():
    global current_profile
    current_profile = None
    hide_all_screens()
    main_menu.show()


def go_back():
    hide_all_screens()
    
    if current_profile == "Admin":
        profile_panel.show()
        admin_options.show()
    elif current_profile == "Staff":
        profile_panel.show()
        staff_options.show()
    elif current_profile == "Patient":
        profile_panel.show()
        patient_options.show()
    else:
        main_menu.show() 

def show_manage_users_menu():
    hide_all_screens()
    manage_users_screen.show()

def show_add_user_screen():
    hide_all_screens()
    add_user_screen.show()

def show_remove_user_screen():
    hide_all_screens()
    remove_user_screen.show()

def show_view_users_screen():
    hide_all_screens()
    view_user_screen.show()

def update_password_entry(number):
    password_entry.value += str(number)

def delete_last_digit():
    password_entry.value = password_entry.value[:-1]

def verify_password():
    global current_method
    current_method = "PIN"
    
    entered_pin = password_entry.value.strip()
    matched_user = None

    # First: check hardcoded role PINs
    if entered_pin == PASSWORDS[selected_profile]:
        sql = "INSERT INTO login_records (user_id, confidence, status, method) VALUES (%s, %s, %s, %s)"
        current_method = "Numpad"
        values = (0, 0, "Success", current_method)
        cursor.execute(sql, values)
        db.commit()
        
        password_window.hide()
        switch_panel(selected_profile)
        return

    # Second: check PIN_USERS
    for name, data in PIN_USERS.items():
        if data["pin"] == entered_pin and data["role"].lower() == selected_profile.lower():
            matched_user = name
            break

    if matched_user:
        password_window.hide()
        info("Success", f"Welcome, {matched_user.title()}!")
        switch_panel(selected_profile)
    else:
        sql = "INSERT INTO login_records (user_id, confidence, status, method) VALUES (%s, %s, %s, %s)"
        values = (0, 0, "Failed", current_method)
        cursor.execute(sql, values)
        db.commit()
        error_message.value = "Incorrect PIN. Try again."
        password_entry.value = ""

def request_auth_method(profile):
    global selected_profile
    selected_profile = profile
    hide_all_screens()
    auth_label.value = f"Choose Authentication Method:"
    auth_method_screen.show()

def show_password_screen():
    hide_all_screens()
    password_label.value = f"Enter {selected_profile} password:"
    password_entry.value = ""
    error_message.value = ""
    password_window.show()

def process_frame(frame, selected_role):
    global face_locations, face_encodings, face_names

    # Resize the frame for performance
    resized_frame = cv2.resize(frame, (0, 0), fx=(1/cv_scaler), fy=(1/cv_scaler))
    rgb_resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

    # Detect faces and their encodings
    face_locations = face_recognition.face_locations(rgb_resized_frame)
    face_encodings = face_recognition.face_encodings(rgb_resized_frame, face_locations)

    face_names = []

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # Find the best match
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]

            # Check if the recognized name matches the selected role
            if FACIAL_USERS.get(name.lower(), "").lower() == selected_profile.lower():
                face_names.append(name)
            else:
                face_names.append("Unauthorized")  # Optionally mark as unauthorized

    return frame

def draw_results(frame):
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
    # Scale back up face locations since the frame we detected in was scaled
        top *= cv_scaler
        right *= cv_scaler
        bottom *= cv_scaler
        left *= cv_scaler
                
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)
                
        # Draw a label with a name below the face
        cv2.rectangle(frame, (left -3, top - 35), (right+3, top), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.putText(frame, name, (left + 6, top - 6), font, 0.8, (0, 0, 0), 1)
            
    return frame

def perform_biometrics(method):
    global current_method
    current_method = method
    hide_all_screens()

    if method == "Facial Recognition":
        facial_text.show()

        # --- New Camera Popup Setup ---
        camera_screen = Box(app, layout="vertical")
        instruction_text.show()

        video_display = Label(app.tk)
        video_display.pack()

        stop_recognition = [False]
        cap = picam2
        cap.start()
        time.sleep(2)

        timeout = time.time() + 5  # 5 seconds timeout
        cv_scaler = 4  # Make sure this matches your earlier setting

        def cancel_biometrics():
            stop_recognition[0] = True
            cap.stop()
            video_display.destroy()
            camera_screen.destroy()
            instruction_text.hide()
            facial_text.hide()
            request_auth_method(selected_profile)
            
        PushButton(camera_screen, text="Cancel", width=30, command=cancel_biometrics)

        def update_frame():
            if stop_recognition[0]:
                return

            try:
                frame = cap.capture_array()
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Resize for faster processing
                small_frame = cv2.resize(rgb_frame, (0, 0), fx=(1/cv_scaler), fy=(1/cv_scaler))

                # Face detection
                face_locations = face_recognition.face_locations(small_frame)
                face_encodings = face_recognition.face_encodings(small_frame, face_locations)

                face_names = []

                FACE_CONFIDENCE_THRESHOLD = 0.8  # smaller = stricter match

                for face_encoding in face_encodings:
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    best_distance = face_distances[best_match_index]

                    # Debug print to shell
                    print(f"[DEBUG] Face distance: {best_distance}")

                    if best_distance < FACE_CONFIDENCE_THRESHOLD:
                        name = known_face_names[best_match_index]
                        if FACIAL_USERS.get(name.lower()) == selected_profile:
                            face_names.append(name)
                        else:
                            face_names.append("Unauthorized")
                    else:
                        face_names.append("Unknown")

                # Handle matches
                for name in face_names:
                    if name != "Unauthorized" and name != "Unknown":
                        recognized_name = name
                        stop_recognition[0] = True
                        cap.stop()
                        video_display.destroy()
                        camera_screen.destroy()
                        instruction_text.hide()
                        facial_text.hide()
                        
                        sql = "INSERT INTO login_records (user_id, confidence, status, method) VALUES (%s, %s, %s, %s)"
                        values = (0, 0, "Success", "Facial Recognition")
                        cursor.execute(sql, values)
                        db.commit()
                        
                        info("Success", f"Welcome, {recognized_name.title()}!")
                        switch_panel(selected_profile)
                        return
                    
                    elif name == "Unauthorized":
                        stop_recognition[0] = True
                        cap.stop()
                        video_display.destroy()
                        camera_screen.destroy()
                        instruction_text.hide()
                        facial_text.hide()
                        
                        sql = "INSERT INTO login_records (user_id, confidence, status, method) VALUES (%s, %s, %s, %s)"
                        values = (0, 0, "Failed", "Facial Recognition")
                        cursor.execute(sql, values)
                        db.commit()
                        
                        info("Error", "Unauthorized: Face does not match selected profile.")
                        request_auth_method(selected_profile)
                        return
                    elif name == "Unknown":
                        info("Warning", "Unknown face detected. Rechecking...")

                # Timeout handling
                if time.time() > timeout:
                    stop_recognition[0] = True
                    cap.stop()
                    video_display.destroy()
                    camera_screen.destroy()
                    instruction_text.hide()
                    facial_text.hide()
                    info("Error", "Face not recognized. Try again.")
                    request_auth_method(selected_profile)
                    return

                # Display frame
                img = Image.fromarray(rgb_frame)
                img = img.resize((640, 480))
                imgtk = ImageTk.PhotoImage(image=img)
                video_display.imgtk = imgtk
                video_display.config(image=imgtk)

                app.after(100, update_frame)
            except Exception as e:
                print(f"[ERROR] Facial recognition error: {e}")
                stop_recognition[0] = True
                cap.stop()
                video_display.destroy()
                camera_screen.destroy()
                instruction_text.hide()
                facial_text.hide()
                info("Error", "Unknown user. Please try again.")
                request_auth_method(selected_profile)

        update_frame()


def fingerprint_auth():
    global current_method
    current_method = "Fingerprint"
    hide_all_screens()
    fingerprint_text.show()  # Show the instruction text

    def scan():
        timeout = time.time() + 5  # 5 seconds max
        while time.time() < timeout:
            if get_fingerprint():
                fingerprint_text.hide()
                uid = finger.finger_id
                confidence = finger.confidence

                user_data = FINGERPRINT_USERS.get(str(uid))
                if not user_data:
                    info("Error", "Fingerprint not registered.")
                    request_auth_method(selected_profile)
                    return

                name = user_data["name"]
                role = user_data["role"]
                
                current_method = "Fingerprint"

                sql = "INSERT INTO login_records (user_id, confidence, status, method) VALUES (%s, %s, %s, %s)"
                values = (uid, confidence, "Success", current_method)
                cursor.execute(sql, values)
                db.commit()

                print(f"[DEBUG] Fingerprint ID: {uid}, Name: {name}, Role: {role}, Confidence: {confidence}")

                if confidence >= 110:
                    if role.lower() == selected_profile.lower():
                        info("Success", f"Welcome, {name.title()}!")
                        switch_panel(selected_profile)
                        return
                    else:
                        info("Error", f"Access denied. '{name.title()}' is a {role}, not a {selected_profile}.")
                        break
                else:
                    print(f"[DEBUG] Confidence too low: {confidence}")
                    info("Error", "Fingerprint confidence too low. Try again.")
                    break

        fingerprint_text.hide()
       
        current_method = "Fingerprint"
        sql = "INSERT INTO login_records (user_id, confidence, status, method) VALUES (%s, %s, %s, %s)"
        values = (0, 0, "Failed", current_method)
        cursor.execute(sql, values) 
        db.commit()
        
        if app.tk.winfo_exists():
            info("Error", "Fingerprint not recognized. Try again.")
        request_auth_method(selected_profile)

    app.after(100, scan)

# Create instruction text at top of your GUI setup
instruction_text = Text(app, text="", size=text_size, visible=False)

def enroll_finger(location):
    global instruction_text

    scans_needed = 4
    successful_scans = 0

    for fingerimg in range(1, scans_needed + 1):
        instruction_text.value = f"Place finger on sensor... (Scan {fingerimg}/{scans_needed})"
        app.update()
        time.sleep(2)

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                instruction_text.value = "Image taken. Checking quality..."
                app.update()
                time.sleep(1)
                break
            elif i == adafruit_fingerprint.NOFINGER:
                instruction_text.value = "Waiting for finger..."
                app.update()
            elif i == adafruit_fingerprint.IMAGEFAIL:
                instruction_text.value = "Imaging error. Try again."
                app.update()
                return False
            else:
                instruction_text.value = "Unknown imaging error."
                app.update()
                return False

        instruction_text.value = "Analyzing fingerprint..."
        app.update()
        time.sleep(1)

        buffer_id = 1 if (fingerimg % 2) == 1 else 2  # alternate between buffer 1 and 2
        i = finger.image_2_tz(buffer_id)
        if i == adafruit_fingerprint.OK:
            instruction_text.value = "Good quality fingerprint!"
            successful_scans += 1
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                instruction_text.value = "Fingerprint too messy. Try again slowly."
            elif i == adafruit_fingerprint.FEATUREFAIL:
                instruction_text.value = "Fingerprint features unclear. Press a little harder."
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                instruction_text.value = "Invalid fingerprint. Try adjusting finger position."
            else:
                instruction_text.value = "Unknown error during analysis."
            app.update()
            time.sleep(2)
            return False

        app.update()
        time.sleep(2)

        if fingerimg != scans_needed:
            instruction_text.value = "Remove finger."
            app.update()
            while finger.get_image() != adafruit_fingerprint.NOFINGER:
                pass
            time.sleep(1)

    # After all scans
    instruction_text.value = "Creating fingerprint model..."
    app.update()
    time.sleep(1)

    i = finger.create_model()
    if i != adafruit_fingerprint.OK:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            instruction_text.value = "Scans didn't match. Try again."
        else:
            instruction_text.value = "Model creation error."
        app.update()
        time.sleep(2)
        return False

    instruction_text.value = f"Storing fingerprint at ID #{location}..."
    app.update()
    time.sleep(1)

    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        instruction_text.value = "Fingerprint stored successfully!"
        app.update()
        time.sleep(1)
        return True
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            instruction_text.value = "Bad storage location!"
        elif i == adafruit_fingerprint.FLASHERR:
            instruction_text.value = "Flash storage error!"
        else:
            instruction_text.value = "Unknown storage error."
        app.update()
        time.sleep(2)
        return False

    return True


def add_user_fingerprint():
    hide_all_screens()

    global current_popup
    if current_popup:
        current_popup.destroy()
            

    if finger.read_sysparam() != adafruit_fingerprint.OK:
        error("Error", "Failed to get system parameters")
        return

    if finger.count_templates() != adafruit_fingerprint.OK:
        error("Error", "Failed to count existing fingerprints")
        return

    if current_popup is not None:
        current_popup.destroy()

    current_popup = Box(app, layout="vertical", width=500, height=600, align="top")
    Text(current_popup, text="Enter User Name for Fingerprint:", size=text_size)
    name_box = TextBox(current_popup, width=30)

    def add_letter(ltr): name_box.value += ltr.lower()
    def delete_letter(): name_box.value = name_box.value[:-1]
    def add_space(): name_box.value += " "
    def clear_name(): name_box.value = ""
    def cancel_keyboard():
        global current_popup
        if current_popup:
            current_popup.destroy()
            current_popup = None
        go_back()

    def submit_name():
        global current_popup
        name = name_box.value.strip().lower()
        if not name:
            error("Error", "Name cannot be empty.")
            return
        if any(user.get("name") == name for user in FINGERPRINT_USERS.values()):
            error("Error", f"'{name.title()}' is already registered.")
            return

        used_ids = set(map(int, FINGERPRINT_USERS.keys()))
        for new_id in range(finger.library_size):
            if new_id not in used_ids:
                break
        else:
            error("Error", "No available fingerprint slots.")
            return
        
        current_popup.destroy()
        current_popup = None

        current_popup = Box(app, layout="vertical", width=300, height=200)
        Text(current_popup, text=f"Select role for '{name.title()}':")

        def choose_role(role):
            global current_popup
            current_popup.destroy()
            current_popup = None

            instruction_text.show()
            instruction_text.value = f"Enrolling fingerprint for {name.title()}..."
            app.update()

            if enroll_finger(new_id):
                FINGERPRINT_USERS[str(new_id)] = {"name": name, "role": role}
                save_fingerprint_users()
                info("Success", f"{role} '{name.title()}' enrolled at ID #{new_id}!")
                instruction_text.value = "Enrollment successful!"
                app.update()
                time.sleep(2)
                instruction_text.hide()
                go_back()
            else:
                error("Failure", "Enrollment failed.")
                instruction_text.value = "Enrollment failed."
                app.update()
                time.sleep(2)
                instruction_text.hide()
                go_back()

        PushButton(current_popup, text="Staff", command=lambda: choose_role("Staff"))
        PushButton(current_popup, text="Patient", command=lambda: choose_role("Patient"))
        PushButton(current_popup, text="Cancel", command=cancel_keyboard)

    keyboard = Box(current_popup, layout="vertical", align="top")
    for row_text in ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]:
        row = Box(keyboard, layout="grid")
        for idx, letter in enumerate(row_text):
            PushButton(row, text=letter, width=2, height=1, grid=[idx, 0], command=lambda l=letter: add_letter(l))

    special_row = Box(keyboard, layout="grid")
    PushButton(special_row, text="Space", width=6, height=1, grid=[0, 0], command=add_space)
    PushButton(special_row, text="Delete", width=6, height=1, grid=[1, 0], command=delete_letter)
    PushButton(special_row, text="Clear", width=6, height=1, grid=[2, 0], command=clear_name)
    PushButton(special_row, text="Confirm", width=6, height=1, grid=[3, 0], command=submit_name)
    PushButton(special_row, text="Back", width=6, height=1, grid=[4, 0], command=cancel_keyboard)


def remove_fingerprint_by_name():
    hide_all_screens()

    global current_popup
    if current_popup:
        current_popup.destroy()

    if finger.read_sysparam() != adafruit_fingerprint.OK:
        error("Error", "Failed to read fingerprint system parameters.")
        return

    if current_popup:
        current_popup.destroy()

    current_popup = Box(app, layout="vertical", width=500, height=600, align="top")
    Text(current_popup, text="Enter Name to Delete:", size=text_size)
    name_box = TextBox(current_popup, width=30)

    # Keyboard input helpers
    def add_letter(ltr): name_box.value += ltr.lower()
    def delete_letter(): name_box.value = name_box.value[:-1]
    def add_space(): name_box.value += " "
    def clear_name(): name_box.value = ""

    def cancel_keyboard():
        global current_popup
        if current_popup:
            current_popup.destroy()
            current_popup = None
        go_back()

    def delete_by_name():
        global current_popup
        target_name = name_box.value.strip().lower()

        if not target_name:
            error("Error", "Name cannot be empty.")
            return

        # Find the ID associated with this name
        matching_id = None
        for fid, data in FINGERPRINT_USERS.items():
            if data["name"].lower() == target_name:
                matching_id = int(fid)
                break

        if matching_id is None:
            error("Error", f"No fingerprint found for '{target_name.title()}'.")
            return

        # Attempt to delete from sensor
        instruction_text.show()
        instruction_text.value = f"Deleting fingerprint for '{target_name.title()}' (ID #{matching_id})..."
        app.update()
        time.sleep(1)

        i = finger.delete_model(matching_id)
        if i == adafruit_fingerprint.OK:
            del FINGERPRINT_USERS[str(matching_id)]
            save_fingerprint_users()

            instruction_text.value = "Fingerprint deleted successfully!"
            app.update()
            time.sleep(2)
            instruction_text.hide()
            go_back()
            info("Success", f"'{target_name.title()}' has been removed.")
        else:
            instruction_text.value = "Failed to delete fingerprint."
            app.update()
            time.sleep(2)
            instruction_text.hide()
            error("Error", "Fingerprint deletion failed.")

        current_popup.destroy()
        current_popup = None

    # Onscreen keyboard
    keyboard = Box(current_popup, layout="vertical", align="top")
    for row_text in ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]:
        row = Box(keyboard, layout="grid")
        for idx, letter in enumerate(row_text):
            PushButton(row, text=letter, width=2, height=1, grid=[idx, 0], command=lambda l=letter: add_letter(l))

    special_row = Box(keyboard, layout="grid")
    PushButton(special_row, text="Space", width=6, height=1, grid=[0, 0], command=add_space)
    PushButton(special_row, text="Delete", width=6, height=1, grid=[1, 0], command=delete_letter)
    PushButton(special_row, text="Clear", width=6, height=1, grid=[2, 0], command=clear_name)
    PushButton(special_row, text="Confirm", width=6, height=1, grid=[3, 0], command=delete_by_name)
    PushButton(special_row, text="Back", width=6, height=1, grid=[4, 0], command=cancel_keyboard)



def train_model():
    print("[INFO] Starting to process faces...")
    imagePaths = list(paths.list_images("dataset"))
    knownEncodings = []
    knownNames = []

    for (i, imagePath) in enumerate(imagePaths):
        print(f"[INFO] Processing image {i + 1}/{len(imagePaths)}")
        name = imagePath.split(os.path.sep)[-2]
        
        image = cv2.imread(imagePath)
        if image is None:
            print(f"[WARNING] Could not read {imagePath}")
            continue

        # Resize image to 50% for faster processing
        image = cv2.resize(image, (0, 0), fx=0.8, fy=0.8)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        boxes = face_recognition.face_locations(rgb, model="hog")  # keep 'hog' for speed
        encodings = face_recognition.face_encodings(rgb, boxes)
        
        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(name)

    print("[INFO] Serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    with open("encodings.pickle", "wb") as f:
        f.write(pickle.dumps(data))

    print("[INFO] Training complete. Encodings saved to 'encodings.pickle'")

    
def reload_encodings():
    global known_face_encodings, known_face_names
    with open("encodings.pickle", "rb") as f:
        data = pickle.load(f)
        known_face_encodings = data["encodings"]
        known_face_names = data["names"]


def add_user_facial_recognition():
    hide_all_screens()

    global current_popup
    if current_popup:
        current_popup.destroy()
          

    current_popup = Box(app, layout="vertical", width=600, height=600, align="top")
    Text(current_popup, text="Enter New User Name:", size=text_size)
    name_box = TextBox(current_popup, width=30)

    # --- Local input helpers ---
    def add_letter(ltr):
        name_box.value += ltr.lower()

    def delete_letter():
        name_box.value = name_box.value[:-1]

    def add_space():
        name_box.value += " "

    def clear_name():
        name_box.value = ""

    def cancel_keyboard():
        global current_popup
        if current_popup:
            current_popup.destroy()
            current_popup = None
        go_back()

    def submit_name():
        global current_popup
        name = name_box.value.strip().lower()
        if not name:
            error("Error", "Name cannot be empty.")
            return

        current_popup.destroy()
        app.update()
        time.sleep(0.8)

        # Show role selection popup
        current_popup = Box(app, layout="vertical", width=300, height=200)
        Text(current_popup, text=f"Select role for '{name.title()}':")

        def choose_role(role):
            global current_popup
            current_popup.destroy()
            current_popup = None
            start_camera_capture(name)

        PushButton(current_popup, text="Staff", command=lambda: choose_role("Staff"))
        PushButton(current_popup, text="Patient", command=lambda: choose_role("Patient"))
        PushButton(current_popup, text="Cancel", command=cancel_keyboard)

    # --- Onscreen keyboard ---
    keyboard = Box(current_popup, layout="vertical", align="top")

    # Row 1
    top_row = Box(keyboard, layout="grid")
    for idx, letter in enumerate("QWERTYUIOP"):
        PushButton(top_row, text=letter, width=2, height=2, grid=[idx, 0], command=lambda l=letter: add_letter(l))

    # Row 2
    middle_row = Box(keyboard, layout="grid")
    for idx, letter in enumerate("ASDFGHJKL"):
        PushButton(middle_row, text=letter, width=2, height=2, grid=[idx, 0], command=lambda l=letter: add_letter(l))

    # Row 3
    bottom_row = Box(keyboard, layout="grid")
    for idx, letter in enumerate("ZXCVBNM"):
        PushButton(bottom_row, text=letter, width=2, height=2, grid=[idx, 0], command=lambda l=letter: add_letter(l))

    # Special row
    special_row = Box(keyboard, layout="grid")
    PushButton(special_row, text="Space", width=6, height=1, grid=[0, 0], command=add_space)
    PushButton(special_row, text="Delete", width=6, height=1, grid=[1, 0], command=delete_letter)
    PushButton(special_row, text="Clear", width=6, height=1, grid=[2, 0], command=clear_name)
    PushButton(special_row, text="Confirm", width=6, height=1, grid=[3, 0], command=submit_name)
    PushButton(special_row, text="Back", width=6, height=1, grid=[4, 0], command=cancel_keyboard)

        

def remove_facial_data():
    hide_all_screens()

    global current_popup
    if current_popup:
        current_popup.destroy()

    current_popup = Box(app, layout="vertical", width=500, height=600, align="top")
    Text(current_popup, text="Enter Name to Delete:", size=text_size)
    name_box = TextBox(current_popup, width=30)

    # Keyboard input helpers
    def add_letter(ltr):
        name_box.value += ltr.lower()

    def delete_letter():
        name_box.value = name_box.value[:-1]

    def add_space():
        name_box.value += " "

    def clear_name():
        name_box.value = ""

    def cancel_keyboard():
        global current_popup
        if current_popup:
            current_popup.destroy()
            current_popup = None
        go_back()

    def delete():
        global current_popup
        name = name_box.value.strip().lower()
        if not name:
            error("Error", "Name cannot be empty.")
            return

        user_folder = os.path.join("dataset", name)
        if os.path.exists(user_folder):
            shutil.rmtree(user_folder)
            print(f"[INFO] Deleted folder: {user_folder}")
        else:
            error("Error", f"No folder found for '{name}'")
            return

        try:
            with open("encodings.pickle", "rb") as f:
                data = pickle.load(f)

            encodings = data["encodings"]
            names = data["names"]

            filtered_data = {
                "encodings": [e for e, n in zip(encodings, names) if n.lower() != name],
                "names": [n for n in names if n.lower() != name]
            }

            with open("encodings.pickle", "wb") as f:
                pickle.dump(filtered_data, f)

            if name in FACIAL_USERS:
                del FACIAL_USERS[name]
                save_facial_users()

            reload_encodings()
            info("Success", f"Facial data for '{name}' deleted.")

        except Exception as e:
            error("Error", f"Failed to update encodings: {e}")

        current_popup.destroy()
        current_popup = None
        go_back()

    # Onscreen keyboard
    keyboard = Box(current_popup, layout="vertical", align="top")

    # Row 1
    top_row = Box(keyboard, layout="grid")
    for idx, letter in enumerate("QWERTYUIOP"):
        PushButton(top_row, text=letter, width=2, height=1, grid=[idx, 0], command=lambda l=letter: add_letter(l))

    # Row 2
    middle_row = Box(keyboard, layout="grid")
    for idx, letter in enumerate("ASDFGHJKL"):
        PushButton(middle_row, text=letter, width=2, height=1, grid=[idx + 1, 0], command=lambda l=letter: add_letter(l))

    # Row 3
    bottom_row = Box(keyboard, layout="grid")
    for idx, letter in enumerate("ZXCVBNM"):
        PushButton(bottom_row, text=letter, width=2, height=1, grid=[idx + 2, 0], command=lambda l=letter: add_letter(l))

    # Special keys
    special_row = Box(keyboard, layout="grid")
    PushButton(special_row, text="Space", width=6, height=1, grid=[0, 0], command=add_space)
    PushButton(special_row, text="Delete", width=6, height=1, grid=[1, 0], command=delete_letter)
    PushButton(special_row, text="Clear", width=6, height=1, grid=[2, 0], command=clear_name)
    PushButton(special_row, text="Confirm", width=6, height=1, grid=[3, 0], command=delete)
    PushButton(special_row, text="Back", width=6, height=1, grid=[4, 0], command=cancel_keyboard)

def add_user_pin():
    hide_all_screens()

    global current_popup
    if current_popup:
        current_popup.destroy()
           

    current_popup = Box(app, layout="vertical", width=500, height=600, align="top")
    prompt_label = Text(current_popup, text="Enter Name for PIN:", size=text_size)

    name_box = TextBox(current_popup, width=30)
    pin_box = TextBox(current_popup, width=30, hide_text=True)
    pin_box.visible = False

    # Containers
    keyboard = Box(current_popup, layout="vertical", align="top")
    pin_pad = Box(current_popup, layout="grid", visible=False)

    def cancel_add_pin():
        global current_popup
        if current_popup:
            current_popup.destroy()
            current_popup = None
        go_back()

    # Name input helpers
    def add_letter(ltr): name_box.value += ltr.lower()
    def delete_letter(): name_box.value = name_box.value[:-1]
    def add_space(): name_box.value += " "
    def clear_name(): name_box.value = ""

    # Show PIN entry UI
    def show_pin_pad():
        name = name_box.value.strip().lower()
        if not name:
            error("Error", "Name cannot be empty.")
            return
        if name in PIN_USERS:
            error("Error", f"'{name.title()}' is already registered.")
            return

        prompt_label.value = "Enter PIN Number for New User:"
        name_box.hide()
        keyboard.hide()
        pin_box.show()
        pin_pad.show()

    # PIN input helpers
    def update_pin_entry(digit): pin_box.value += str(digit)
    def delete_pin_digit(): pin_box.value = pin_box.value[:-1]
    def clear_pin(): pin_box.value = ""

    # Submit PIN and choose role
    def submit_pin():
        name = name_box.value.strip().lower()
        pin = pin_box.value.strip()

        if not name or not pin:
            error("Error", "Name and PIN cannot be empty.")
            return

        if not pin.isdigit():
            error("Error", "PIN must contain only numbers.")
            return

        if len(pin) != 4:
            error("Error", "PIN must be exactly 4 digits.")
            return

        if name in PIN_USERS:
            error("Error", f"'{name.title()}' already exists.")
            return

        # Destroy current popup
        global current_popup
        if current_popup:
            current_popup.destroy()
            current_popup = None

        # Role selection
        role_popup = Box(app, layout="vertical", width=300, height=200)
        Text(role_popup, text=f"Select role for '{name.title()}':")

        def choose_role(role):
            role_popup.destroy()
            PIN_USERS[name] = {"pin": pin, "role": role}
            save_pin_users()
            info("Success", f"User '{name.title()}' added with PIN.")
            go_back()

        PushButton(role_popup, text="Staff", width=20, command=lambda: choose_role("Staff"))
        PushButton(role_popup, text="Patient", width=20, command=lambda: choose_role("Patient"))
        def cancel_role_selection():
            role_popup.destroy()
            show_main_menu()  # or go_back(), depending on what screen you want to return to

        PushButton(role_popup, text="Cancel", width=20, command=cancel_role_selection)
    # Build keyboard for name entry
    for row_text in ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]:
        row = Box(keyboard, layout="grid")
        for idx, letter in enumerate(row_text):
            PushButton(row, text=letter, width=2, height=1, grid=[idx, 0], command=lambda l=letter: add_letter(l))

    special_row = Box(keyboard, layout="grid")
    PushButton(special_row, text="Space", width=6, height=1, grid=[0, 0], command=add_space)
    PushButton(special_row, text="Delete", width=6, height=1, grid=[1, 0], command=delete_letter)
    PushButton(special_row, text="Clear", width=6, height=1, grid=[2, 0], command=clear_name)
    PushButton(special_row, text="Next", width=6, height=1, grid=[3, 0], command=show_pin_pad)

    # PIN pad
    for label, row, col in [
        (1, 0, 0), (4, 0, 1), (7, 0, 2),
        (2, 1, 0), (5, 1, 1), (8, 1, 2),
        (3, 2, 0), (6, 2, 1), (9, 2, 2),
        ("⌫", 3, 0), (0, 3, 1), ("✔", 3, 2)
    ]:
        if label == "⌫":
            PushButton(pin_pad, text=label, grid=[row, col], command=delete_pin_digit)
        elif label == "✔":
            PushButton(pin_pad, text=label, grid=[row, col], command=submit_pin)
        else:
            PushButton(pin_pad, text=str(label), grid=[row, col], command=lambda l=label: update_pin_entry(l))

    PushButton(current_popup, text="Cancel", command=cancel_add_pin)

def remove_pin_user():
    hide_all_screens()

    global current_popup
    if current_popup:
        current_popup.destroy()

    current_popup = Box(app, layout="vertical", width=1500, height=600, align="top")
    Text(current_popup, text="Enter Name to Delete PIN:", size=text_size)
    name_box = TextBox(current_popup, width=30)

    # --- Keyboard helpers ---
    def add_letter(ltr): name_box.value += ltr.lower()
    def delete_letter(): name_box.value = name_box.value[:-1]
    def add_space(): name_box.value += " "
    def clear_name(): name_box.value = ""

    def cancel_keyboard():
        global current_popup
        if current_popup:
            current_popup.destroy()
            current_popup = None
        go_back()

    def delete_pin():
        global current_popup
        name = name_box.value.strip().lower()

        if not name:
            error("Error", "Name cannot be empty.")
            return

        if name in PIN_USERS:
            del PIN_USERS[name]
            save_pin_users()
            current_popup.destroy()
            current_popup = None
            info("Success", f"PIN user '{name.title()}' deleted.")
            go_back()
        else:
            error("Error", f"No PIN user found for '{name.title()}'.")

    # --- Keyboard UI ---
    keyboard = Box(current_popup, layout="vertical", align="top")

    for row_text in ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]:
        row = Box(keyboard, layout="grid")
        for idx, letter in enumerate(row_text):
            PushButton(row, text=letter, width=4, height=2, grid=[idx, 0], command=lambda l=letter: add_letter(l))

    special_row = Box(keyboard, layout="grid")
    PushButton(special_row, text="Space", width=6, height=1, grid=[0, 0], command=add_space)
    PushButton(special_row, text="Delete", width=6, height=1, grid=[1, 0], command=delete_letter)
    PushButton(special_row, text="Clear", width=6, height=1, grid=[2, 0], command=clear_name)
    PushButton(special_row, text="Confirm", width=6, height=1, grid=[3, 0], command=delete_pin)
    PushButton(special_row, text="Back", width=6, height=1, grid=[4, 0], command=cancel_keyboard)



def start_camera_capture(name):
    instruction_text.show()
    instruction_text.value = "Camera starting, please wait..."
    app.update()

    camera_screen = Box(app, layout="vertical")

    photo_counter_text = Text(camera_screen, text="Captured 0 photos", size=text_size)

    video_display = Label(app.tk)
    video_display.pack()

    photos_taken = [0]
    captured_images = []
    stop_button_pressed = [False]
    
    def cancel_camera_capture():
        global current_popup
        if current_popup:
            current_popup.destroy()
            current_popup = None
        stop_button_pressed[0] = True
        cap.stop()
        video_display.destroy()
        camera_screen.destroy()
        instruction_text.hide()
        go_back()  # Return to previous menu
        
    def capture_photo():
        if current_frame[0] is not None:
            img = current_frame[0]
            captured_images.append(img)
            photos_taken[0] += 1
            photo_counter_text.value = f"Captured {photos_taken[0]} photos"

    def finish_and_train():
        if photos_taken[0] < 5:
            error("Error", "Please capture at least 5 photos before adding.")    
        else:
            FACIAL_USERS[name] = role
            save_facial_users()
            stop_button_pressed[0] = True
            return

    PushButton(camera_screen, text="Capture Photo", width=30, command=capture_photo)
    PushButton(camera_screen, text="Finish and Add", width=30, command=finish_and_train)
    PushButton(camera_screen, text="Back", width=30, command=cancel_camera_capture) 
    cap = picam2
    cap.start()
    time.sleep(2)

    dataset_folder = "dataset"
    person_folder = os.path.join(dataset_folder, name)
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)

    current_frame = [None]

    def update_frame():
        if stop_button_pressed[0]:
            cap.stop()
            video_display.destroy()
            camera_screen.destroy()
            app.update()

            # Save captured images
            for idx, img in enumerate(captured_images):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{name}_{timestamp}_{idx}.jpg"
                filepath = os.path.join(person_folder, filename)
                cv2.imwrite(filepath, cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

            # Retrain model
            train_model()
            reload_encodings()  

            instruction_text.hide()
            info("Success", f"User '{name}' added successfully with {len(captured_images)} photo(s)!")
            go_back()
            return

        frame = cap.capture_array()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(frame)
        img = img.resize((400, 300))
        current_frame[0] = img

        imgtk = ImageTk.PhotoImage(image=img)
        video_display.imgtk = imgtk
        video_display.config(image=imgtk)

        app.after(30, update_frame)

    instruction_text.value = "Camera Active. Press 'Capture Photo' when ready."
    app.update()

    update_frame()
        
def get_fingerprint():
    """Attempts to scan and match fingerprint once."""
    if finger.get_image() != adafruit_fingerprint.OK:
        return False
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True

def exit_app():
    hide_all_screens()
    start_screen.show()

def show_main_menu():
    hide_all_screens()
    main_menu.show()


# --- Start Screen ---
start_screen = Box(app, layout="auto", width="fill", height="fill")
PushButton(start_screen, text="Welcome to Dr. Pill\n\nTouch to Start", width="fill", height="fill",
           command=lambda: show_main_menu()).text_size = int(text_size * 1.2)

# --- Main Menu ---
datetime_box = Box(app, layout="auto", width="fill")
datetime_text = Text(app, text="", size=int(text_size * 0.8), color="black")
main_menu = Box(app, layout="vertical", visible=False)
Text(main_menu, text="Welcome to Dr. Pill!", size=text_size)
for role in ["Admin", "Staff", "Patient"]:
    PushButton(main_menu, text=role, width=30, height=button_height, command=lambda r=role: request_auth_method(r))
PushButton(main_menu, text="Exit", width=30, command=exit_app)

# --- Auth Method Screen ---
datetime_box = Box(app, layout="auto", width="fill")
datetime_text = Text(app, text="", size=int(text_size * 0.8), color="black")
auth_method_screen = Box(app, layout="vertical", visible=False)
auth_label = Text(auth_method_screen, text="Choose Authentication Method:", size=text_size)
PushButton(auth_method_screen, text="Facial Recognition", width=30, command=lambda: perform_biometrics("Facial Recognition"))
PushButton(auth_method_screen, text="Fingerprint", width=30, command=fingerprint_auth)
PushButton(auth_method_screen, text="PIN", width=30, command=show_password_screen)
PushButton(auth_method_screen, text="Back", width=20, command=go_back)

# --- Password Window ---
datetime_box = Box(app, layout="auto", width="fill")
datetime_text = Text(app, text="", size=int(text_size * 0.8), color="black")
password_window = Box(app, layout="vertical", visible=False)
password_label = Text(password_window, text="Enter password:", size=text_size)
password_entry = TextBox(password_window, hide_text=True, width=30)
error_message = Text(password_window, text="", color="red")
number_pad = Box(password_window, layout="grid")
for label, row, col in [
    (1, 0, 0), (4, 0, 1), (7, 0, 2),
    (2, 1, 0), (5, 1, 1), (8, 1, 2),
    (3, 2, 0), (6, 2, 1), (9, 2, 2),
    ("⌫", 3, 0), (0, 3, 1), ("✔", 3, 2)
]:
    if label == "⌫":
        PushButton(number_pad, text=label, grid=[row, col], command=delete_last_digit)
    elif label == "✔":
        PushButton(number_pad, text=label, grid=[row, col], command=verify_password)
    else:
        PushButton(number_pad, text=str(label), grid=[row, col], command=lambda l=label: update_password_entry(l))

PushButton(password_window, text="Cancel", command=go_back)

# --- Dispense Pill Screen ---
dispense_screen = Box(app, layout="grid", visible=False)

Text(dispense_screen, text="Select Pill # (1–12):", grid=[0, 0])
pill_number_box = TextBox(dispense_screen, width=5, grid=[1, 0])

Text(dispense_screen, text="Quantity:", grid=[0, 1])
pill_count_box = TextBox(dispense_screen, width=5, grid=[1, 1])

# Track which box is selected (pill number or pill count)
selected_box = [pill_number_box]  # Default

def select_pill_number_box():
    selected_box[0] = pill_number_box

def select_pill_count_box():
    selected_box[0] = pill_count_box

# When clicked, switch input to that box
pill_number_box.when_clicked = select_pill_number_box
pill_count_box.when_clicked = select_pill_count_box

# Create a number pad below
number_pad_dispense = Box(dispense_screen, layout="grid", grid=[0, 2], align="left", width="fill")

def update_dispense_entry(number):
    selected_box[0].value += str(number)

def delete_dispense_entry():
    selected_box[0].value = selected_box[0].value[:-1]

def clear_dispense_entry():
    selected_box[0].value = ""

# Buttons for number pad
for label, row, col in [
    (1, 0, 0), (4, 0, 1), (7, 0, 2),
    (2, 1, 0), (5, 1, 1), (8, 1, 2),
    (3, 2, 0), (6, 2, 1), (9, 2, 2),
    ("⌫", 3, 0), (0, 3, 1), ("C", 3, 2)
]:
    if label == "⌫":
        PushButton(number_pad_dispense, text=label, grid=[row, col], command=delete_dispense_entry)
    elif label == "C":
        PushButton(number_pad_dispense, text=label, grid=[row, col], command=clear_dispense_entry)
    else:
        PushButton(number_pad_dispense, text=str(label), grid=[row, col], command=lambda l=label: update_dispense_entry(l))

# Dispense and Back Buttons
PushButton(dispense_screen, text="Dispense", grid=[1, 2], command=lambda: send_dispense_command())
PushButton(dispense_screen, text="Back", grid=[2, 2], command=go_back)


# --- Manage Users Menu ---
manage_users_screen = Box(app, layout="grid", visible=False)

PushButton(manage_users_screen, text="Add User(s)", grid=[0, 0], width=30, command=show_add_user_screen)
PushButton(manage_users_screen, text="Remove User(s)", grid=[0, 1], width=30, command=show_remove_user_screen)
PushButton(manage_users_screen, text="View User(s)", width=30, grid=[0, 2], command=show_view_users_screen)
PushButton(manage_users_screen, text="Back", grid=[0, 3], width=30, command=go_back)

# --- Add User Screen ---
add_user_screen = Box(app, layout="grid", visible=False)
PushButton(add_user_screen, text="Add User Fingerprint", grid=[0, 1],width=30,command=add_user_fingerprint)
PushButton(add_user_screen, text="Add User Facial Recognition", grid=[0, 2], width=30, command=add_user_facial_recognition)
PushButton(add_user_screen, text="Add User PIN", grid=[0, 3], width=30, command=add_user_pin)
PushButton(add_user_screen, text="Back", grid=[0, 4], width=30,command=go_back)

# --- Remove User Screen ---
remove_user_screen = Box(app, layout="vertical", visible=False)

PushButton(remove_user_screen, text="Delete Fingerprint", width=30, command=remove_fingerprint_by_name)
PushButton(remove_user_screen, text="Delete Facial Recognition", width=30, command=remove_facial_data)
PushButton(remove_user_screen, text="Delete PIN User", width=30, command=remove_pin_user)
PushButton(remove_user_screen, text="Back", width=30, command=go_back)

# --- View Users Screen ---
view_user_screen = Box(app, layout="vertical", visible=False)

def show_users():
    global view_user_screen
    view_user_screen.clear()  # Clear old content

    load_fingerprint_users()
    load_facial_users()

    print("[DEBUG] Loading users...")  # This must show

    # Header
    Text(view_user_screen, text="View Registered Users", size=20)

    # Fingerprint Users
    Text(view_user_screen, text="-- Fingerprint Users --")
    if FINGERPRINT_USERS:
        for uid, role in FINGERPRINT_USERS.items():
            Text(view_user_screen, text=f"ID #{uid} - {role}")
    else:
        Text(view_user_screen, text="No fingerprint users")

    # Facial Users
    Text(view_user_screen, text="-- Facial Recognition Users --")
    if FACIAL_USERS:
        for name, role in FACIAL_USERS.items():
            Text(view_user_screen, text=f"{name.title()} - {role}")
    else:
        Text(view_user_screen, text="No facial recognition users")

    # Back button
    PushButton(view_user_screen, text="Back", command=go_back)

def show_view_users_screen():
    hide_all_screens()
    show_users()
    view_user_screen.show()


# --- Profile Panel ---
profile_panel = Box(app, layout="vertical", visible=False)
profile_text = Text(profile_panel, text="Welcome!", size=text_size)

# Admin Menu Options
datetime_box = Box(app, layout="auto", width="fill")
datetime_text = Text(app, text="", size=int(text_size * 0.8), color="black")
admin_options = Box(profile_panel, layout="vertical", visible=False)
PushButton(admin_options, text="Test Motors", width=30,command=lambda: perform_action("TEST_MOTORS"))
PushButton(admin_options, text="Dispense Pills", width=30, command=show_dispense_menu)
PushButton(admin_options, text="Manage Users", width=30, command=show_manage_users_menu)
PushButton(admin_options, text="Log out", width=30, command=logout)


# Staff Menu Options
datetime_box = Box(app, layout="auto", width="fill")
datetime_text = Text(app, text="", size=int(text_size * 0.8), color="black")
staff_options = Box(profile_panel, layout="vertical", visible=False)
PushButton(staff_options, text="Add User", width=30, command=show_add_user_screen)
PushButton(staff_options, text="Log out", width=30, command=logout)

# Patient Menu Options
datetime_box = Box(app, layout="auto", width="fill")
datetime_text = Text(app, text="", size=int(text_size * 0.8), color="black")
patient_options = Box(profile_panel, layout="vertical", visible=False)
PushButton(patient_options, text="Log out", width=30, command=logout)

update_datetime()
app.display()  



