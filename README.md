# AI Driven Work From Home Assistant

A Python-based assistant tool designed to enhance remote working experiences by tracking distractions, correcting posture, and suppressing background noise.

## 💡 Features

- **Posture Recognition System** 📏  
  Uses MediaPipe and OpenCV to monitor user's sitting posture via webcam and notify if slouching.

- **Distraction Tracking System** 👁️  
  Tracks eye movement to determine screen focus and sends alerts after prolonged distraction.

- **Background Noise Suppression System** 🔊  
  Processes audio recordings to suppress unwanted background sounds using Librosa.

## 🛠️ Built With

- Python 3
- OpenCV
- MediaPipe
- Librosa
- SoundFile
- ctypes
- time

## 📂 Project Structure

- `posture_monitor/`: Code for posture recognition
- `distraction_tracker/`: Code for distraction detection
- `noise_suppressor/`: Code for background audio cleaning
- `evaluation/`: Performance comparison data and graphs

## 📊 Evaluation Highlights

- Up to **92.89% distraction tracking accuracy**
- **Low latency (0.0263 sec/frame)** and **low memory usage**
- Significantly better performance under heavy CPU load compared to open-source alternatives

## 📈 Future Enhancements

- Dashboard GUI
- Mobile App Support
- Gamification & Break Reminders
- Multilingual Audio Feedback

## 📜 License

This project is open-sourced under the MIT License.

## 🎓 Academic Info

Dissertation submitted for M.Eng in Computer Science at Leeds Beckett University  
**Author**: Yatharth Mehta  
**Submission Date**: 6 May 2025  
**Module**: COMP737 – Masters Final Project
