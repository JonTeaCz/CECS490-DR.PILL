---

# Dr. Pill Documentation

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Team Members & Roles](#team-members--roles)
3. [Team Communication & Progress Tracking](#team-communication--progress-tracking)
4. [Project Objectives](#project-objectives)
5. [System Features](#system-features)
6. [System Design Overview](#system-design-overview)
7. [Subsystems](#subsystems)
8. [Technical Specifications](#technical-specifications)
9. [Verification & Testing](#verification--testing)
10. [Demonstrations](#demonstrations)
11. [Cost Breakdown](#cost-breakdown)
12. [Schedule & Timeline](#schedule--timeline)
13. [Challenges & Solutions](#challenges--solutions)
14. [Stretch Goals & Future Work](#stretch-goals--future-work)
15. [Ethical & Privacy Concerns](#ethical--privacy-concerns)
16. [Intellectual Property](#intellectual-property)
17. [References](#references)
18. [Contact](#contact)

---

## Executive Summary

Dr. Pill is an automatic pill dispenser designed to improve medication management for patients, caregivers, and healthcare professionals. The device automates pill dispensing, enhances adherence, and reduces human error through features like biometric security, real-time reminders, and comprehensive tracking. Dr. Pill is especially beneficial for the elderly and those with complex medication regimens, aiming to simplify the process and improve patient outcomes.

---

## Team Members & Roles

| Name                  | Responsibilities                                                                                  | Contact                                      |
|-----------------------|--------------------------------------------------------------------------------------------------|----------------------------------------------|
| Jonathan Cerniaz      | Circuitry, Team Management, Touchscreen Display, Enclosure & Framework, Power Supply, Conveyor Belt, Storage Design | Jonathan.Cerniaz01@student.csulb.edu         |
| Joseph Guzman         | Enclosure & Framework, GitHub Manager, 3D Design and Build, Motor Testing, Dispensing Mechanism, Board Communication, Conveyor Belt | joseph.guzman@student.csulb.edu              |
| Jehmel Espiritu       | User Interface Implementation, Display Menu Programming                                           | Jehmel.Espiritu01@student.csulb.edu          |
| Jeremy Espiritu       | Pill Tracking & Dispensing, Screen Display, Dispense History                                     | Jeremy.Espiritu01@student.csulb.edu          |
| Afzal Hakim           | Facial Recognition, Number Pad, Fingerprint Scanner, Log Tracking Management & Storage           | Afzal.Hakim01@student.csulb.edu              |
| Lee Roger Ordinario   | Dispense & Storage Design, Soldering, Object Recognition                                         | LeeRoger.Ordinario@student.csulb.edu         |

---

## Team Communication & Progress Tracking

- **Weekly Recap Meetings:** Fridays at 3 PM via Microsoft Teams
- **Daily Check-ins:** In classes and via Teams
- **Monthly Meetups:** Off-campus for team building
- **Tools:**  
  - Microsoft Teams (meetings, task tracking)  
  - GitHub (version control)  
  - Google Docs (progress reports)  
  - Microsoft Office Suite (reports, presentations, tracking)  
  - Shapr3D & SolidWorks (3D design)

---

## Project Objectives

- Improve medication adherence and accuracy
- Enhance patient safety and independence
- Reduce medication errors and caregiver workload
- Provide secure, user-friendly, and customizable medication management
- Integrate advanced security (biometrics) and remote monitoring

---

## System Features

- **Automatic Pill Dispensing:** Motorized drop pivot system, conveyor belt
- **Multiple Modes:** Refill (continuous) and On-Demand (scheduled)
- **Multi-compartment Storage:** Up to 8 types of medication
- **User Interface:** 7" touchscreen display
- **Security:** Facial recognition, fingerprint scanner, number pad
- **Tracking:** Dispense history logging, object recognition for verification
- **Connectivity:** MySQL database, remote access (stretch goal)
- **Alerts:** Missed dose, low supply, refill reminders
- **Customizability:** Schedules, user roles (admin, staff, patient)
- **Data Security:** Secure storage and access controls

---

## System Design Overview

- **Block Diagrams:**  
  - Authentication flow for staff and patients  
  - Storage, retrieval, and logging processes  
- **Main Components:**  
  - Raspberry Pi 5 (CPU)  
  - STM32 Microcontroller  
  - Stepper and Servo Motors  
  - 7" Touchscreen  
  - Biometric sensors (fingerprint, facial recognition)  
  - MySQL database  
  - Secure enclosure

---

## Subsystems

1. **Pill Dispenser:**  
   - Motorized dispensing, multi-compartment storage, conveyor delivery

2. **User Interface:**  
   - Touchscreen for controls, logs, and feedback

3. **Authentication:**  
   - Biometric and keypad access, secure logging

---

## Technical Specifications

| Specification           | Value/Description                   |
|-------------------------|-------------------------------------|
| Dispensing Accuracy     | 99.9%                               |
| UI Response Time        | <500 ms                             |
| Pill Dispensing Time    | <2 seconds after authentication     |
| Authentication Speed    | Facial: <3s, Fingerprint: <1s, Keypad: <5s |
| Storage Capacity        | 8 medications                       |
| Battery Backup          | 24 hours (stretch goal)             |
| CPU                     | Raspberry Pi 5, ARM Cortex-A72, 1.5 GHz, 64-bit, 2-8GB RAM |
| Connectivity            | Wi-Fi, Bluetooth, I2C, SPI, UART, USB, Ethernet |
| Noise Level             | <40 dB                              |
| Enclosure               | IP54-rated, shock and vibration resistant |

---

## Verification & Testing

- **Tolerance Analysis:** Test across full operational ranges
- **Component Testing:** Motors, CPU, sensors, UI
- **Integration Testing:** System-wide simulations
- **Real-World Scenarios:** Timed dispensing, user authentication, error handling
- **Performance Metrics:** Response time, throughput, error rate, UI feedback
- **Worst-Case Testing:** Simulated jams, delayed responses, stress conditions

---

## Demonstrations

- **Demo 1:** Pill dispensing and storage (motorized mechanism)
- **Demo 2:** Touchscreen UI and number pad application
- **Demo 3:** Authentication system with MySQL logging
- **Final Demo:** Fully integrated system with all features and roles

---

## Cost Breakdown

### Labor Cost

| Team Member        | Calculation                 | Total      |
|--------------------|----------------------------|------------|
| Jonathan Cerniaz   | $50 × 2.5 × 300            | $37,500    |
| Jehmel Espiritu    | $50 × 2.5 × 300            | $37,500    |
| Jeremy Espiritu    | $50 × 2.5 × 300            | $37,500    |
| Joseph Guzman      | $50 × 2.5 × 300            | $37,500    |
| Afzal Hakim        | $50 × 2.5 × 300            | $37,500    |
| Lee Roger Ordinario| $50 × 2.5 × 300            | $37,500    |
| **Total Labor Cost** |                            | **$225,000**|

### Parts Cost (Estimate)

| Component                  | Estimated Cost | Source         |
|----------------------------|---------------|----------------|
| Raspberry Pi 5             | $80           | CanaKit        |
| 7" Touch Screen Display    | $35.99        | Amazon         |
| Wood                       | ~$20          | Home Depot     |
| Pill Compartments          | $23.99        | 3D Printing/Amazon |
| Power Supply               | $26.99        | Amazon         |
| Camera Module              | ~$30          | Amazon         |
| Fingerprint Scanner        | ~$75          | Amazon, DigiKey|
| Sensors, MicroSD, Motor Driver, STM32, Misc. | ~$200         | Amazon, DigiKey, ElectroMaker |
| **Total Parts**            | **~$489.84**  |                |

**Grand Total:** ~$225,489.84

---

## Schedule & Timeline

| Phase                  | Start Date   | End Date     | Key Activities                                 |
|------------------------|--------------|--------------|------------------------------------------------|
| Research & Planning    | Aug 26, 2024 | Oct 7, 2024  | Prototype design, storage mechanism            |
| Hardware Development   | Oct 1, 2024  | Mar 1, 2025  | UI, security, motors, assembly                 |
| Software Development   | Oct 7, 2024  | Mar 1, 2025  | UI, security, tracking system                  |
| Integration & Testing  | Feb 1, 2025  | May 9, 2025  | System integration, comprehensive testing      |
| Project Completion     | May 9, 2025  | May 9, 2025  | Final demo, expo preparation                   |

---

## Challenges & Solutions

- **Precise Dispensing:** Implemented XY grid and conveyor, upgraded motors, improved mounts, explored vibration mechanisms.
- **Space Management:** Stackable components, optimized layouts.
- **Power Management:** Universal supply, step-down converters, backup battery, sleep modes.
- **3D Printing Issues:** Used stronger materials, reinforced structures.
- **Communication Bugs:** Troubleshooted MySQL and biometric device integration.
- **Temperature Regulation:** Improved ventilation, monitored heat.

---

## Stretch Goals & Future Work

- **Remote Access:** For authorized personnel
- **Mobile App:** Medication tracking, reminders, prescription renewal, drug interaction checker
- **Modular Design:** Portability, battery backup
- **Object Recognition:** Enhanced dispensing accuracy
- **Commercialization:** Explore regulatory, manufacturing, and market strategies

---

## Ethical & Privacy Concerns

- **Patient Education:** Ensure users understand device operation
- **Data Privacy:** Secure storage and access controls for medical data
- **Maintaining Human Interaction:** Avoid replacing physician-patient relationships
- **Device Reliability:** Implement fail-safes for accuracy and safety

---

## Intellectual Property

- **Unique Features:** Modern design, advanced automation, comprehensive security
- **Similar Devices:** Live Fine, Hero, MedReady
- **Patentable Ideas:** Under consideration

---

## References

See final report for full bibliography.

---

## Contact

- Jonathan Cerniaz: [Jonathan.Cerniaz01@student.csulb.edu](mailto:Jonathan.Cerniaz01@student.csulb.edu)
- Jehmel Espiritu: [Jehmel.Espiritu01@student.csulb.edu](mailto:Jehmel.Espiritu01@student.csulb.edu)
- Jeremy Espiritu: [Jeremy.Espiritu01@student.csulb.edu](mailto:Jeremy.Espiritu01@student.csulb.edu)
- Joseph Guzman: [joseph.guzman@student.csulb.edu](mailto:joseph.guzman@student.csulb.edu)
- Afzal Hakim: [Afzal.Hakim01@student.csulb.edu](mailto:Afzal.Hakim01@student.csulb.edu)
- Lee Roger Ordinario: [LeeRoger.Ordinario@student.csulb.edu](mailto:LeeRoger.Ordinario@student.csulb.edu)

---
