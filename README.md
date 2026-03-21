# HandSense Remote: AI-Powered Gesture Media Control
HandSense Remote is a high-performance, privacy-first computer vision application that allows users to control macOS media playback through real-time hand gestures. Built specifically to leverage the M4 Pro Neural Engine, this project demonstrates the bridge between Local AI, Computer Vision, and System-Level OS integration.

## Overview
Most media controllers rely on hardware or cloud-based voice assistants. HandSense moves the intelligence to the edge. By utilizing local landmark detection models, it interprets hand positions as system commands (Volume, Play/Pause, Skip) with sub-30ms latency.

### Why Local AI?
- Latency: Real-time gesture control requires immediate feedback that cloud APIs (like Gemini/GPT-4o) cannot provide due to network round-trips.
- Privacy: Camera data is processed entirely in volatile memory and never leaves the device.
- Efficiency: Optimized for Apple Silicon Unified Memory, significantly reducing CPU overhead compared to standard x86 implementations.

## Features
[ ] Real-time Landmark Tracking: 21-point hand coordinate mapping at 30+ FPS.

[ ] Dynamic Gesture Mapping: - Pinch: Volume Control (Vertical movement).

    Open Palm: Play / Pause.

    Swipe: Track Navigation.

[ ] System-Level Integration: Direct communication with macOS via AppleScript and PyObjC.

[ ] Modular Architecture: Clean separation between the AI Inference Engine and the OS Controller.

## Tech Stack
Language: Python 3.11
Inference Engine: MediaPipe (optimized for ARM64)
Computer Vision: OpenCV
Hardware Acceleration: CoreML / Metal (via MediaPipe/TensorFlow-Metal)
OS Bridge: AppleScript / PyObjC (Native macOS API)