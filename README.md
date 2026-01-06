# 🖱️⌨️ Virtual Mouse & Keyboard using Hand Gestures

A real-time **gesture-controlled Virtual Mouse and On-Screen Keyboard** built using **OpenCV, MediaPipe, and PyAutoGUI**.  
This project enables hands-free cursor control and typing using hand landmark detection through a webcam.

---

## 🚀 Features

- 🖐️ **Hand Gesture Mouse Control**
  - Move cursor using index finger
  - Left-click using thumb + index finger pinch

- ⌨️ **Virtual On-Screen Keyboard**
  - Fully visible keyboard rendered on screen
  - Tap / punch gesture to type keys
  - Supports **SPACE** and **BACKSPACE**

- 📝 **Live Input Text Box**
  - Displays typed text in real time
  - Text is also sent to active system applications (Notepad, Browser, etc.)

- 🖥️ **Windowed UI with Controls**
  - Resizable window
  - Minimize / Maximize / Close buttons available
  - No fullscreen lock issues

---

## 🛠️ Tech Stack

- **Python**
- **OpenCV** – video capture & UI rendering
- **MediaPipe Hands** – hand landmark detection
- **PyAutoGUI** – system mouse & keyboard control

---

## 📦 Installation

Install the required dependencies:

```bash
pip install opencv-python mediapipe pyautogui
