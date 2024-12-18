// CECS 490A: Senior Project - Dr. Pill Dispenser
// File Name: DR_PILL.c 
// Created: 10/05/2024 1:36:46 PM
// Authors: Jonathan Cerniaz, Jehmel Espiritu, Jeremy Espiritu, Joseph Guzman, Afzal Hakim, Lee Roger Ordinario 
// Description: This file is the main file for the Dr. Pill Dispenser project. This file will be used to run the program.


#include "Authenticator.h"
#include "Interface.h"
#include "LCD_Screen.h"
#include "motors.h"
#include "DR_PILL_flags.h"
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>

// Intialize variables at the start of the program

int main(void) {
    // Initialize hardware components
    initLCD();
    initMotors();
    initAuthenticator();
    initInterface();

    // Main loop
    while (1) {
        // Authenticator.c
        if (()) {
            // Interface.c and LCD_Screen.c
            displayInterface();
            
            // Motors.c
            int pillCount = getPillCountFromUser();
            dispensePills();
        } else {
            // Authenticator.c and LCD_Screen.c
            displayAuthError();
        }
    }

    return ("Exiting program...");
}