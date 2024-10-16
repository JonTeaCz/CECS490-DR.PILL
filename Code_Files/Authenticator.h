// CECS 490A: Senior Project - Dr. Pill Dispenser
// File Name: Authenticator.h
// Created: 10/05/2024 1:27:58 PM
// Authors: Jonathan Cerniaz, Jehmel Espiritu, Jeremy Espiritu, Joseph Guzman, Afzal Hakim, Lee Roger Ordinario 
// Description: Header file for the Authenticator class

#ifndef AUTHENTICATOR_H
#define AUTHENTICATOR_H

// Define Variables
#define MAX_USERS 100
#define MAX_NAME_LENGTH 50
#define MAX_ROLE_LENGTH 10

// Struct for the first, last name of the user, and pin number  
typedef struct {
    char firstName[MAX_NAME_LENGTH];
    char lastName[MAX_NAME_LENGTH];
    char pin[6];
    char role[MAX_ROLE_LENGTH];
} User;

void loadUsers();
void verifyFingerprint(void);
void verifyFacialRecognition(void);
void verifyPinPad(void);
void authenticateUser(void);
void authenticateStaff(void);
void authenticateCustomer(void);

#endif