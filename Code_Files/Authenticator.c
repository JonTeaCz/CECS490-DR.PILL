// CECS 490A: Senior Project - Dr. Pill Dispenser
// File Name: Authenticator.c 
// Created: 10/05/2024 1:27:06 PM
// Authors: Jonathan Cerniaz, Jehmel Espiritu, Jeremy Espiritu, Joseph Guzman, Afzal Hakim, Lee Roger Ordinario 
// Description: This file is used to authenticate the user. It will check if the user an authorized user or a customer.

#include "Authenticator.h"
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

// Function prototypes
void verifyFingerprint();
void verifyFacialRecognition();
void verifyPinPad();
void authenticateUser();
void authenticateStaff();
void authenticateCustomer();

// Initalize the user struct
User users[MAX_USERS];
int userCount = 0;

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

void loadUsers() {
    FILE *file = fopen("names_and_ids.txt", "r");
    if (file == NULL) {
        printf("Error opening file.\n");
        return;
    }

    while (fscanf(file, "%[^,], %[^,], %[^,], %s\n", users[userCount].firstName, users[userCount].lastName, users[userCount].pin, users[userCount].role) == 4) {
        userCount++;
        if (userCount >= MAX_USERS) break;
    }

    fclose(file);
}

void verifyPinPad() {
    if (userCount == 0) {
        loadUsers();
    }

    char inputPin[6];
    printf("Enter your 5-digit PIN: ");
    scanf("%5s", inputPin);

    bool authenticated = false;
    for (int i = 0; i < userCount; i++) {
        if (strcmp(inputPin, users[i].pin) == 0) {
            printf("Authentication successful. Welcome, %s %s!\n", users[i].firstName, users[i].lastName);
            if (strcmp(users[i].role, "staff") == 0) {
                printf("You are logged in as staff.\n");
                authenticateStaff();
            } else {
                printf("You are logged in as a customer.\n");
                authenticateCustomer();
            }
            authenticated = true;
            break;
        }
    }

    if (!authenticated) {
        printf("Authentication failed. Invalid PIN.\n");
    }
}
