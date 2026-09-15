import cv2
import mediapipe as mp
import numpy as np
import math
import serial
import time
import threading
from collections import deque

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ─── KONFIGURASI SERIAL ───────────────────────────────────────
PORT     = 'COM16'   # Sesuaikan dengan port Arduino Anda
BAUDRATE = 115200    

try:
    arduino = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(2)
    print(f"[OK] Terhubung ke Arduino di {PORT}")
except Exception as e:
    arduino = None
    print(f"[WARN] Gagal terhubung: {e}")

# ─── VARIABEL FEEDBACK & GRAFIK ──────────────────────────────
feedback = {
    "sudut": 0.0,
    "rpm":   0.0,
    "pwm":   0
}
target_rpm = 0.0  

# Buffer data untuk grafik (Menyimpan 100 data terakhir)
HISTORY_LEN = 100
rpm_history = deque([0.0] * HISTORY_LEN, maxlen=HISTORY_LEN)
target_history = deque([0.0] * HISTORY_LEN, maxlen=HISTORY_LEN)

def read_arduino_feedback():
    """Membaca data aktual (Sudut, RPM, PWM) dari Arduino secara real-time"""
    while True:
        if arduino and arduino.is_open:
            try:
                line = arduino.readline().decode('utf-8', errors='ignore').strip()
                parts = line.split(",")
                if len(parts) == 3:
                    feedback["sudut"] = float(parts[0])
                    feedback["rpm"]   = float(parts[1])
                    feedback["pwm"]   = int(parts[2])
            except:
                pass
        time.sleep(0.01)

fb_thread = threading.Thread(target=read_arduino_feedback, daemon=True)
fb_thread.start()

# ─── INISIALISASI MEDIAPIPE ───────────────────────────────────
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
tip_ids = [4, 8, 12, 16, 20]

def draw_glow_circle(img, center, color):
    for i in range(10, 0, -2):
        cv2.circle(img, center, i, color, 1)

def count_fingers(lm_list, hand_type):
    fingers = []
    if hand_type == "Right":
        fingers.append(1 if lm_list[4][0] > lm_list[3][0] else 0)
    else:
        fingers.append(1 if lm_list[4][0] < lm_list[3][0] else 0)
    for i in range(1, 5):
        fingers.append(1 if lm_list[tip_ids[i]][1] < lm_list[tip_ids[i]-2][1] else 0)
    return sum(fingers)

def draw_feedback_panel(frame, h, w):
    panel_x, panel_y = w - 260, h - 130
    overlay = frame.copy()
    cv2.rectangle(overlay, (panel_x-10, panel_y-10), (w-10, h-10), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    cv2.rectangle(frame, (panel_x-10, panel_y-10), (w-10, h-10), (0, 255, 255), 1)

    font, small = cv2.FONT_HERSHEY_SIMPLEX, 0.55
    cv2.putText(frame, "── MOTOR STATUS ──",  (panel_x, panel_y+10), font, small, (0, 255, 255), 1)
    cv2.putText(frame, f"Sudut : {feedback['sudut']:.1f} deg", (panel_x, panel_y+30), font, small, (200,200,200), 1)
    cv2.putText(frame, f"Target: {target_rpm:.1f} RPM",        (panel_x, panel_y+50), font, small, (0,255,100), 1)
    cv2.putText(frame, f"Actual: {feedback['rpm']:.1f} RPM",   (panel_x, panel_y+70), font, small, (255,255,255), 1)
    cv2.putText(frame, f"PWM   : {feedback['pwm']}",           (panel_x, panel_y+90), font, small, (0,200,255), 1)

    # Progress bar diskalakan ke Max 200 RPM
    bar_len = int((feedback['rpm'] / 200.0) * 230)
    if bar_len > 230: bar_len = 230
    elif bar_len < 0: bar_len = 0
    
    cv2.rectangle(frame, (panel_x, panel_y+100), (panel_x+230, panel_y+110), (60,60,60), -1)
    cv2.rectangle(frame, (panel_x, panel_y+100), (panel_x+bar_len, panel_y+110), (0,255,100), -1)

def draw_finger_mapping(frame):
    h, w = frame.shape[:2]
    mapping = ["0: STOP (0 RPM)", "1: 40 RPM", "2: 70 RPM", "3: 100 RPM", "4: 150 RPM", "5: 200 RPM"]
    overlay = frame.copy()
    cv2.rectangle(overlay, (5, h-145), (185, h-5), (0,0,0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
    cv2.rectangle(frame, (5, h-145), (185, h-5), (100,100,100), 1)
    cv2.putText(frame, "TARGET RPM (PID):", (12, h-128), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200,200,0), 1)
    for i, m in enumerate(mapping):
        cv2.putText(frame, m, (12, h-110+i*18), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (200,200,200), 1)

def draw_rpm_graph(frame, h, w):
    """Menggambar grafik garis untuk Target RPM vs Actual RPM"""
    g_w, g_h = 300, 120  # Lebar dan Tinggi grafik
    g_x, g_y = w - g_w - 20, 20  # Posisi (Kanan Atas)

    # Latar belakang grafik semi-transparan
    overlay = frame.copy()
    cv2.rectangle(overlay, (g_x, g_y), (g_x + g_w, g_y + g_h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
    cv2.rectangle(frame, (g_x, g_y), (g_x + g_w, g_y + g_h), (150, 150, 150), 1)

    # Label Legenda
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "GRAFIK RPM (0 - 500)", (g_x + 5, g_y + 15), font, 0.4, (255, 255, 255), 1)
    cv2.putText(frame, "- Target", (g_x + 150, g_y + 15), font, 0.4, (0, 255, 100), 1)
    cv2.putText(frame, "- Actual", (g_x + 220, g_y + 15), font, 0.4, (255, 255, 255), 1)

    # Batas maksimal Y-axis diatur ke 200 RPM
    max_rpm_scale = 500.0 

    # Menggambar garis grafik
    for i in range(1, HISTORY_LEN):
        # Hitung koordinat X (waktu)
        x1 = g_x + int((i - 1) / (HISTORY_LEN - 1) * g_w)
        x2 = g_x + int(i / (HISTORY_LEN - 1) * g_w)

        # Hitung koordinat Y untuk TARGET RPM (Warna Hijau)
        ty1 = g_y + g_h - int(min(max(target_history[i-1], 0), max_rpm_scale) / max_rpm_scale * g_h)
        ty2 = g_y + g_h - int(min(max(target_history[i], 0), max_rpm_scale) / max_rpm_scale * g_h)
        cv2.line(frame, (x1, ty1), (x2, ty2), (0, 255, 100), 2)

        # Hitung koordinat Y untuk ACTUAL RPM (Warna Putih)
        ry1 = g_y + g_h - int(min(max(rpm_history[i-1], 0), max_rpm_scale) / max_rpm_scale * g_h)
        ry2 = g_y + g_h - int(min(max(rpm_history[i], 0), max_rpm_scale) / max_rpm_scale * g_h)
        cv2.line(frame, (x1, ry1), (x2, ry2), (255, 255, 255), 2)

prev_wrist, lock_threshold, prev_fingers = None, 200, -1

while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb      = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result   = detector.detect(mp_image)

    total_fingers = 0

    if result.hand_landmarks:
        best_hand_idx = 0
        if prev_wrist is not None:
            min_dist = float('inf')
            for i, hand_landmarks in enumerate(result.hand_landmarks):
                wx, wy = int(hand_landmarks[0].x * w), int(hand_landmarks[0].y * h)
                dist = math.hypot(wx - prev_wrist[0], wy - prev_wrist[1])
                if dist < min_dist:
                    min_dist, best_hand_idx = dist, i
            if min_dist > lock_threshold: best_hand_idx = 0

        locked_landmarks = result.hand_landmarks[best_hand_idx]
        hand_type = result.handedness[best_hand_idx][0].category_name
        lm_list = [(int(lm.x * w), int(lm.y * h)) for lm in locked_landmarks]
        prev_wrist, total_fingers = lm_list[0], count_fingers(lm_list, hand_type)

        for point in lm_list: draw_glow_circle(frame, point, (0, 255, 255))
        
        connections = [(0,1),(1,2),(2,3),(3,4),(0,5),(5,6),(6,7),(7,8),(0,9),(9,10),(10,11),(11,12),(0,13),(13,14),(14,15),(15,16),(0,17),(17,18),(18,19),(19,20)]
        for c in connections: cv2.line(frame, lm_list[c[0]], lm_list[c[1]], (255, 0, 255), 2)
        cv2.putText(frame, f"{hand_type} (LOCKED)", (lm_list[0][0]-20, lm_list[0][1]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
        
        # ── TENTUKAN TARGET RPM BERDASARKAN JARI ──
        if total_fingers == 0: target_rpm = 0.0
        elif total_fingers == 1: target_rpm = 110.0
        elif total_fingers == 2: target_rpm = 140.0
        elif total_fingers == 3: target_rpm = 160.0
        elif total_fingers == 4: target_rpm = 180.0
        elif total_fingers == 5: target_rpm = 200.0

        if total_fingers != prev_fingers:
            if arduino is not None:
                arduino.write(f"{target_rpm}\n".encode('utf-8'))
            prev_fingers = total_fingers
    else:
        prev_wrist = None

    # Update Data ke Buffer Grafik setiap frame
    rpm_history.append(feedback['rpm'])
    target_history.append(target_rpm)

    teks_jari = f"Jari: {total_fingers}" if result.hand_landmarks else "Tangan: Out of Frame"
    cv2.putText(frame, teks_jari, (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    # Menggambar semua elemen GUI
    draw_feedback_panel(frame, h, w)
    draw_finger_mapping(frame)
    draw_rpm_graph(frame, h, w) 
    
    cv2.imshow("Gesture Motor Control", frame)
    
    if cv2.waitKey(1) & 0xFF == 27: break

if arduino is not None:
    arduino.write(b"0\n")
    arduino.close()
cap.release()
cv2.destroyAllWindows()
