// CECS 490A: Senior Project - Dr. Pill Dispenser
// File Name: Authenticator.c 
// Created: 10/05/2024 1:27:06 PM
// Authors: Jonathan Cerniaz, Jehmel Espiritu, Jeremy Espiritu, Joseph Guzman, Afzal Hakim, Lee Roger Ordinario 
// Description: This file is used to authenticate the user. It will check if the user an authorized user or a customer.

#include "Authenticator.h"
#include <stdio.h>
#include <string.h>

// Function prototypes
void verifyFingerprint();
void verifyFacialRecognition();
void verifyPinPad();
void authenticateUser();
void authenticateStaff();
void authenticateCustomer();

void authenticateUser() {
    int userType;
    printf("Select user type:\n");
    printf("1. Staff\n");
    printf("2. Customer\n");
    printf("Enter choice: ");
    scanf("%d", &userType);

    switch (userType) {
        case 1:
            authenticateStaff();
            break;
        case 2:
            authenticateCustomer();
            break;
        default:
            printf("Invalid choice.\n");
            break;
    }
}
void authenticateStaff() {
    int choice;
    printf("Select verification method:\n");
    printf("1. Fingerprint\n");
    printf("2. Facial Recognition\n");
    printf("3. Pin Pad\n");
    printf("Enter choice: ");
    scanf("%d", &choice);

    switch (choice) {
        case 1:
            verifyFingerprint();
            break;
        case 2:
            verifyFacialRecognition();
            break;
        case 3:
            verifyPinPad();
            break;
        default:
            printf("Invalid choice.\n");
            break;
    }
}

void authenticateCustomer() {
    int choice;
    printf("Select verification method:\n");
    printf("1. Fingerprint\n");
    printf("2. Facial Recognition\n");
    printf("3. Pin Pad\n");
    printf("Enter choice: ");
    scanf("%d", &choice);

    switch (choice) {
        case 1:
            verifyFingerprint();
            break;
        case 2:
            verifyFacialRecognition();
            break;
        case 3:
            verifyPinPad();
            break;
        default:
            printf("Invalid choice.\n");
            break;
    }
}

void verifyFingerprint() {
    // Placeholder for fingerprint verification logic
    printf("Verifying fingerprint...\n");
    // Simulate verification success
}

void verifyFacialRecognition() {
    // Placeholder for facial recognition verification logic
    printf("Verifying facial recognition...\n");
    // Simulate verification success
}

void verifyPinPad() {
    // Placeholder for pin pad verification logic
    printf("Verifying pin pad...\n");
    // Simulate verification success
}
