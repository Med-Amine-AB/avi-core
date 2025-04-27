![Avi Care Logo](mobile/avi_care/assets/logo%20png.png)

# Avi Care: AI-Powered Personal Health Companion

## Project Overview

### Problem
In Morocco, wearable devices collect valuable health data (e.g., heart rate, sleep patterns, SpO2) but fail to provide actionable insights. This gap leaves users, especially in rural areas, without real-time health advice or emergency support.

### Solution
**Avi Care** is an AI-powered personal health companion that bridges this gap by:
- Collecting health data from existing wearable devices.
- Analyzing the data using AI to detect dehydration, stress, injuries, and more.
- Providing real-time actionable advice (e.g., "Hydrate now" or "Rest for potential sprain").
- Generating emergency health reports via QR codes for doctors.

Avi Care empowers users with timely health insights and improves access to healthcare, especially in underserved communities.

---

## Key Features

1. **Hydration Monitoring**  
   Detects dehydration risks and advises users to hydrate.

2. **Stress Detection**  
   Monitors stress levels and provides relaxation tips.

3. **Sleep Quality Analysis**  
   Tracks sleep patterns and offers suggestions for better rest.

4. **Early Injury Detection**  
   Identifies potential injuries based on movement and health data.

5. **Emergency Health Reports**  
   Generates QR-coded reports for doctors, enabling faster emergency response.

6. **No New Hardware Required**  
   Works seamlessly with existing wearable devices.

---

## Tech Stack

- **Backend**: Flask, Firebase  
- **Mobile App**: Flutter  
- **AI Models**: Custom models for:
  - Injury detection
  - Stress detection
  - Sleep quality analysis
  - Cardiovascular health monitoring

---

## Installation and Usage

### Prerequisites
- Python 3.8+
- Flutter SDK
- Firebase account for backend setup
- All devices (mobile, backend server, and wearable simulator) must be connected to the **same network** for local testing.

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/avi-care.git
   cd avi-care/backend
   ```

### Testing the App

1. **Install the Mobile App**  
   - Navigate to the `mobile` directory:
     ```bash
     cd avi-care/mobile
     ```
   - Install dependencies:
     ```bash
     flutter pub get
     ```
   - Run the app:
     ```bash
     flutter run
     ```

2. **Run the Flask Backend**  
   - Navigate to the [backend](http://_vscodecontentref_/0) directory:
     ```bash
     cd avi-care/backend
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Start the Flask server:
     ```bash
     python app.py
     ```

3. **Run the Control Script**  
   - Navigate to the control script directory:
     ```bash
     cd avi-care/control
     ```
   - Run the control script:
     ```bash
     python control.py
     ```

4. **Run the Wearable Simulator**  
   - Navigate to the wearable simulator directory:
     ```bash
     cd avi-care/wearable_simulator
     ```
   - Start the simulator:
     ```bash
     python simulator.py
     ```

5. **Ensure Network Connection**  
   - Verify that all devices (mobile app, backend server, and wearable simulator) are connected to the **same local network** for proper communication.

---

## Hackathon Alignment

### Reproducibility
- Open-source code with clear setup instructions ensures easy replication.

### Technical Implementation
- Combines AI, mobile development, and cloud technologies for a robust solution.

### Innovation
- AI-driven health insights from existing wearables—no new hardware required.

### Ethics
- Prioritizes user privacy and data security with Firebase.

### Impact
- Improves healthcare accessibility for rural communities in Morocco.

### Pitch Quality
- Watch our 2-minute video pitch here (link to be added).

---

## Demo

- **Video Pitch**:  

---

## Objectives

- **70%+ users** receive daily actionable health advice.
- **30% reduction** in untreated conditions like dehydration.
- **Faster emergency response** via QR-coded health reports.

---

## Contact

For questions or contributions, please contact:  
**Team Avi Care**  
Email: [mohamedamineaboudrar@gmail.com](mailto:your-email@example.com)  
GitHub: [https://github.com/Med-Amine-AB](https://github.com/your-repo/avi-care)