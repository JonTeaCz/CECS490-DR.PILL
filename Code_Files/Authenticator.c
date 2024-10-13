// CECS 490A: Senior Project - Dr. Pill Dispenser
// File Name: Authenticator.c 
// Created: 10/05/2024 1:27:06 PM
// Authors: Jonathan Cerniaz, Jehmel Espiritu, Jeremy Espiritu, Joseph Guzman, Afzal Hakim, Lee Roger Ordinario 
// Description: This file is used to authenticate the user. It will check if the user an authorized user or a customer.

#include "Authenticator.h"

#include <stdio.h>
#include <string.h>

// Function prototypes
int verifyFingerprint();
int verifyFacialRecognition();
int verifyPinPad();
int authenticateUser();
int authenticateCustomer();

int authenticateUser() {
    int choice;
    printf("Select verification method:\n");
    printf("1. Fingerprint\n");
    printf("2. Facial Recognition\n");
    printf("3. Pin Pad\n");
    printf("Enter choice: ");
    scanf("%d", &choice);

    switch (choice) {
        case 1:
            return verifyFingerprint();
        case 2:
            return verifyFacialRecognition();
        case 3:
            return verifyPinPad();
        default:
            printf("Invalid choice.\n");
            return 0;
    }
}

int authenticateCustomer() {
    int choice;
    printf("Select verification method:\n");
    printf("1. Fingerprint\n");
    printf("2. Facial Recognition\n");
    printf("3. Pin Pad\n");
    printf("Enter choice: ");
    scanf("%d", &choice);

    switch (choice) {
        case 1:
            return verifyFingerprint();
        case 2:
            return verifyFacialRecognition();
        case 3:
            return verifyPinPad();
        default:
            printf("Invalid choice.\n");
            return 0;
    }
}

int verifyFingerprint() {
    // Placeholder for fingerprint verification logic
    printf("Verifying fingerprint...\n");
    // Simulate verification success
    return 1;
}

int verifyFacialRecognition() {
    // Placeholder for facial recognition verification logic
    printf("Verifying facial recognition...\n");
    // Simulate verification success
    return 1;
}

int verifyPinPad() {
    // Placeholder for pin pad verification logic
    printf("Verifying pin pad...\n");
    // Simulate verification success
    return 1;
}