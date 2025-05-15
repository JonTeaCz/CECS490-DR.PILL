# Dr. Pill

**Automatic Pill Dispenser for Improved Medication Management**

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Team](#team)
- [Roles & Responsibilities](#roles--responsibilities)
- [Project Objectives](#project-objectives)
- [System Architecture](#system-architecture)
- [Demonstrations](#demonstrations)
- [Cost Breakdown](#cost-breakdown)
- [Schedule](#schedule)
- [Challenges & Solutions](#challenges--solutions)
- [Stretch Goals & Future Work](#stretch-goals--future-work)
- [Ethical Considerations](#ethical-considerations)
- [Intellectual Property](#intellectual-property)
- [References](#references)
- [Contact](#contact)

---

## Overview

**Dr. Pill** is an automatic pill dispenser designed to revolutionize medication management for patients, caregivers, and healthcare professionals. The device automates pill dispensing, enhances adherence, and reduces human error through features like biometric security, real-time reminders, and comprehensive tracking. Dr. Pill is especially beneficial for the elderly and those with complex medication regimens, aiming to simplify the process and improve patient outcomes.

---

## Features

- **Automatic Pill Dispensing:** Motorized drop pivot system and conveyor belt for accurate, timely delivery.
- **Multi-Mode Operation:** Refill (continuous) and On-Demand (scheduled) dispensing.
- **Multiple Storage Compartments:** Supports up to 8 different medications.
- **User Interface:** 7" touchscreen display for easy operation.
- **Biometric Security:** Facial recognition, fingerprint scanner, and number pad for secure access.
- **Dosage Tracking & Logging:** Dispense history, object recognition for verification, and MySQL database integration.
- **Reminders & Alerts:** Missed dose, low supply, and refill notifications.
- **Customizable Schedules:** Supports multiple user roles (admin, staff, patient).
- **Secure Data Storage:** Patient data is protected and access-controlled.

---

## Team

| Name                  | Email                                      |
|-----------------------|--------------------------------------------|
| Jonathan Cerniaz      | jonathan.cerniaz@gmail.com                 |
| Jehmel Espiritu       | Jehmel.Espiritu01@student.csulb.edu        |
| Jeremy Espiritu       | Jeremy.Espiritu01@student.csulb.edu        |
| Joseph Guzman         | joseph.guzman@student.csulb.edu            |
| Afzal Hakim           | Afzal.Hakim01@student.csulb.edu            |
| Lee Roger Ordinario   | LeeRoger.Ordinario@student.csulb.edu       |

---

## Roles & Responsibilities

- **Jonathan Cerniaz:** Circuitry, team management, touchscreen, enclosure, power, conveyor, storage, facial and fingerprint recognition.
- **Joseph Guzman:** Enclosure, GitHub, 3D design/build, motor testing, dispensing, board communication, conveyor.
- **Jehmel Espiritu:** User interface implementation, display menu programming.
- **Jeremy Espiritu:** Pill tracking/dispensing, screen display, dispense history.
- **Afzal Hakim:** Facial recognition, number pad, fingerprint scanner, log tracking/storage.
- **Lee Roger Ordinario:** Dispense/storage design, soldering, object recognition.

---

## Project Objectives

- Improve medication adherence and accuracy.
- Enhance patient safety and independence.
- Reduce medication errors and caregiver workload.
- Provide secure, user-friendly, and customizable medication management.
- Integrate advanced biometric security and remote monitoring.

---

## System Architecture

**Main Components:**
- Raspberry Pi 5 (CPU)
- STM32 Microcontroller
- Stepper and Servo Motors
- 7" Touchscreen LCD
- Biometric sensors (fingerprint, facial recognition)
- Pixy2 Object Recognition
- MySQL database
- Secure enclosure

**Subsystems:**
- **Pill Dispenser:** Motorized dispensing, multi-compartment storage, conveyor delivery.
- **User Interface:** Touchscreen for controls, logs, and feedback.
- **Authentication:** Biometric and keypad access, secure logging.

**Technical Highlights:**
- Dispensing accuracy: 99.9%
- UI response time: <500 ms
- Authentication speed: Facial <3s, Fingerprint <1s, Keypad <5s
- Storage for 8 medications
- 24-hour battery backup (stretch goal)
- IP54-rated enclosure

---

## Demonstrations

- **Demo 1:** Pill dispensing and storage (motorized mechanism)
- **Demo 2:** Touchscreen UI and number pad application
- **Demo 3:** Authentication system with MySQL logging
- **Final Demo:** Fully integrated system with all features and roles

---

## Cost Breakdown

| Category      | Estimate      |
|---------------|--------------|
| Labor         | $225,000      |
| Parts         | ~$490         |
| **Total**     | **$225,490**  |

**Major Parts:**
- Raspberry Pi 5: $80
- 7" Touchscreen: $36
- Pill Compartments: $24
- Power Supply: $27
- Camera Module: $30
- Fingerprint Scanner: $75
- Misc. (sensors, microSD, etc.): $200

---

## Schedule

| Phase                  | Start       | End         | Key Activities                              |
|------------------------|------------|-------------|---------------------------------------------|
| Research & Planning    | Aug 2024   | Oct 2024    | Prototype, storage mechanism                |
| Hardware Development   | Oct 2024   | Mar 2025    | UI, security, motors, assembly              |
| Software Development   | Oct 2024   | Mar 2025    | UI, security, tracking                      |
| Integration & Testing  | Feb 2025   | May 2025    | System integration, comprehensive testing   |
| Project Completion     | May 2025   | May 2025    | Final demo, expo preparation                |

---

## Challenges & Solutions

- **Precise Dispensing:** Implemented XY grid/conveyor, upgraded motors, improved mounts, explored vibration mechanisms.
- **Space Management:** Stackable components, optimized layouts.
- **Power Management:** Universal supply, step-down converters, backup battery, sleep modes.
- **3D Printing Issues:** Used stronger materials, reinforced structures.
- **Communication Bugs:** Troubleshooted MySQL and biometric device integration.
- **Temperature Regulation:** Improved ventilation, monitored heat.

---

## Stretch Goals & Future Work

- Remote access for authorized personnel
- Mobile app for medication tracking and reminders
- Modular/portable design with battery backup
- Enhanced object recognition
- Commercialization and regulatory compliance

---

## Ethical Considerations

- **Patient Education:** Ensuring users understand device operation.
- **Data Privacy:** Secure storage and access controls for medical data.
- **Maintaining Human Interaction:** Device should support, not replace, patient-provider relationships.
- **Device Reliability:** Multiple fail-safes for accuracy and safety.

---

## Intellectual Property

- **Unique Features:** Modern design, advanced automation, comprehensive security.
- **Similar Devices:** Live Fine, Hero, MedReady.
- **Patentable Ideas:** Under consideration.

---

## References

See [Documentation.md](Documentation/Documentation.md) and [Final Report (PDF)](Progress/Progress_Reports/CECS490B_Final_Report_Group.pdf) for full bibliography and technical appendices.

---

## Contact

For questions or collaboration, please contact any team member listed in the [Team](#team) section.
