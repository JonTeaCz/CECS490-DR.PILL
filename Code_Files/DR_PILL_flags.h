// CECS 490A: Senior Project - Dr. Pill Dispenser
// File Name: DR_PILL_flags.h
// Created: 10/15/2024 8:14:44 PM
// Authors: Jonathan Cerniaz, Jehmel Espiritu, Jeremy Espiritu, Joseph Guzman, Afzal Hakim, Lee Roger Ordinario 
// Description: Header file that contains all the flags that will need to be initialized at the start of the program.

#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>

// ==================== General Flags ====================


// ==================== Customer Flags ====================
bool CUSTOMER_FLAG = false;              // Flag for customer authentication
bool CUSTOMER_AUTHENTICATED = false;     // Flag for if the customer is authenticated
bool CUSTOMER_AUTHENTICATE_FLAG = false; // Flag for if the customer is ready to authenticate
bool CUSTOMER_AUTHENTICATE_SUCCESS = false; // Flag for successful customer authentication
bool CUSTOMER_AUTHENTICATE_ERROR = false;   // Flag for error in customer authentication
bool CUSTOMER_AUTHENTICATE_COMPLETE = false; // Flag for completion of customer authentication
bool CUSTOMER_AUTHENTICATE_EXIT = false;    // Flag for customer exit from authentication
bool CUSTOMER_AUTHENTICATE_RETRY = false;   // Flag for customer retry of authentication
bool CUSTOMER_AUTHENTICATE_SUCCESSFUL = false; // Flag for successful customer authentication
bool CUSTOMER_AUTHENTICATE_FAILED = false;  // Flag for failed customer authentication

// ==================== Staff Flags ====================
bool STAFF_FLAG = false;                // Flag for staff authentication
bool STAFF_AUTHENTICATED = false;       // Flag for if the staff is authenticated
bool STAFF_AUTHENTICATE_FLAG = false;   // Flag for if the staff is ready to authenticate
bool STAFF_AUTHENTICATE_SUCCESS = false; // Flag for successful staff authentication
bool STAFF_AUTHENTICATE_ERROR = false;   // Flag for error in staff authentication
bool STAFF_AUTHENTICATE_COMPLETE = false; // Flag for completion of staff authentication
bool STAFF_AUTHENTICATE_EXIT = false;    // Flag for staff exit from authentication
bool STAFF_AUTHENTICATE_RETRY = false;   // Flag for staff retry of authentication
bool STAFF_AUTHENTICATE_SUCCESSFUL = false; // Flag for successful staff authentication
bool STAFF_AUTHENTICATE_FAILED = false;  // Flag for failed staff authentication

bool STAFF_FINGERPRINT_FLAG = false;    // Flag for staff fingerprint verification
bool STAFF_FACIAL_RECOGNITION_FLAG = false; // Flag for staff facial recognition verification
bool STAFF_PINPAD_FLAG = false;         // Flag for staff pin pad verification
bool STAFF_PINPAD_SUCCESS = false;      // Flag for successful staff pin pad verification
bool STAFF_FINGERPRINT_SUCCESS = false; // Flag for successful staff fingerprint verification
bool STAFF_FACIAL_RECOGNITION_SUCCESS = false; // Flag for successful staff facial recognition verification

bool STAFF_DISPENSE_FLAG = false;       // Flag for staff ready to dispense
bool STAFF_DISPENSE_COMPLETE = false;   // Flag for complete staff dispensing
bool STAFF_DISPENSE_ERROR = false;      // Flag for staff dispensing error
bool STAFF_DISPENSE_SUCCESS = false;    // Flag for successful staff dispensing
bool STAFF_EXIT_FLAG = false;           // Flag for staff exit
bool STAFF_ERROR_FLAG = false;          // Flag for general staff error


// ==================== System Flags ====================
bool FINGERPRINT_FLAG = false;          // Flag for fingerprint verification
bool FACIAL_RECOGNITION_FLAG = false;   // Flag for facial recognition verification
bool PINPAD_FLAG = false;               // Flag for pin pad verification
bool PINPAD_SUCCESS = false;            // Flag for successful pin pad verification
bool FINGERPRINT_SUCCESS = false;       // Flag for successful fingerprint verification
bool FACIAL_RECOGNITION_SUCCESS = false; // Flag for successful facial recognition verification

bool DISPENSE_FLAG = false;             // Flag for customer ready to dispense
bool DISPENSE_COMPLETE = false;         // Flag for complete dispensing
bool DISPENSE_ERROR = false;            // Flag for dispensing error
bool DISPENSE_SUCCESS = false;          // Flag for successful dispensing
bool EXIT_FLAG = false;                 // Flag for customer exit
bool ERROR_FLAG = false;                // Flag for general error