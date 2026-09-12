#include <Arduino.h>
#include <Wire.h>
#include <AS5600.h>
#include <LiquidCrystal_I2C.h>

#define L298N_ENB_PIN 3
#define L298N_IN3_PIN 5
#define L298N_IN4_PIN 6

LiquidCrystal_I2C lcd(0x27, 16, 2);
AS5600 as5600;

unsigned long waktuLama = 0;
float sudutLama = 0.0;
float rpm = 0.0;
float sudutOffset = 0.0;

// ==========================================
// VARIABEL PID (Tuning Menengah & Stabil)
// ==========================================

float Kp = 3.30;      // Dorongan proporsional
float Ki = 0.5;       // Dorongan integral
float Kd = 0.002;     // Rem turunan untuk meredam guncangan

float setpoint_rpm = 0.0;

float error = 0.0;
float last_error = 0.0;

float integral = 0.0;
float derivative = 0.0;

int output_pwm = 0;


void setup() {

  pinMode(L298N_ENB_PIN, OUTPUT);
  pinMode(L298N_IN3_PIN, OUTPUT);
  pinMode(L298N_IN4_PIN, OUTPUT);

  Serial.begin(115200);

  Wire.begin();
  as5600.begin();

  if (!as5600.isConnected()) {
    while (1);
  }

  // Auto-Tare 0 Derajat saat mesin dinyalakan
  sudutOffset = as5600.readAngle() * (360.0 / 4096.0);

  waktuLama = millis();
  sudutLama = 0.0;

  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print(" SISTEM MONITOR ");

  lcd.setCursor(0, 1);
  lcd.print(" PID BERJALAN ");

  delay(2000);

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Sudut:");

  lcd.setCursor(0, 1);
  lcd.print("RPM:");

  lcd.setCursor(9, 1);
  lcd.print("PWM:");
}


void loop() {

  // ===================================================
  // 1. TERIMA TARGET RPM DARI PYTHON
  // ===================================================

  if (Serial.available() > 0) {

    float rpm_masuk = Serial.parseFloat();

    // Keamanan rentang target RPM
    // Sesuai kode pada laporan
    if (rpm_masuk >= 0 && rpm_masuk <= 10000) {
      setpoint_rpm = rpm_masuk;
    }

    // Bersihkan sisa buffer karakter yang masuk
    while (Serial.available() > 0) {
      Serial.read();
    }
  }


  // ===================================================
  // 2. BACA SENSOR & HITUNG RPM
  // ===================================================

  uint16_t rawAngle = as5600.readAngle();

  float sudutSekarang =
    (rawAngle * (360.0 / 4096.0)) - sudutOffset;

  if (sudutSekarang < 0.0) {
    sudutSekarang += 360.0;
  }

  unsigned long waktuSekarang = millis();

  long selisihWaktu =
    waktuSekarang - waktuLama;

  // Update perhitungan setiap 100 ms (0.1 detik)
  if (selisihWaktu >= 100) {

    float selisihSudut =
      sudutSekarang - sudutLama;


    // Koreksi jika melewati batas lingkaran
    if (selisihSudut > 180.0) {
      selisihSudut -= 360.0;
    }
    else if (selisihSudut < -180.0) {
      selisihSudut += 360.0;
    }


    // Hitung RPM Mentah
    // Menggunakan fabs agar tidak membulat jadi 0
    float putaran =
      fabs(selisihSudut) / 360.0;

    float menit =
      (float)selisihWaktu / 60000.0;

    float rpm_mentah =
      putaran / menit;


    // =================================================
    // LOW-PASS FILTER
    // Menstabilkan angka RPM
    // =================================================

    // Mengambil 40% data baru
    // dan mempertahankan 60% data lama
    rpm =
      (0.4 * rpm_mentah) +
      (0.6 * rpm);


    // =================================================
    // 3. KALKULASI PID & ANTI-WINDUP
    // =================================================

    float dt =
      (float)selisihWaktu / 1000.0;

    error =
      setpoint_rpm - rpm;


    // Anti-Windup:
    // Batasi memori integral agar PWM
    // tidak nyangkut lama di 255
    integral += error * dt;

    if (integral > 255.0) {
      integral = 255.0;
    }
    else if (integral < -255.0) {
      integral = -255.0;
    }


    derivative =
      (error - last_error) / dt;


    float hasil_pid =
      (Kp * error) +
      (Ki * integral) +
      (Kd * derivative);


    output_pwm =
      (int)hasil_pid;


    // Batasi tegangan akhir ke modul L298N
    if (output_pwm > 255) {
      output_pwm = 255;
    }
    else if (output_pwm < 0) {
      output_pwm = 0;
    }


    // =================================================
    // SAFETY FEATURE
    // Matikan paksa jika target adalah 0
    // =================================================

    if (setpoint_rpm == 0.0) {

      output_pwm = 0;
      integral = 0.0;

      // Reset tampilan RPM ke 0 saat berhenti
      rpm = 0.0;
    }


    last_error = error;

    sudutLama = sudutSekarang;
    waktuLama = waktuSekarang;


    // =================================================
    // 4. KIRIM DATA KE PYTHON
    // =================================================

    Serial.print(sudutSekarang, 1);
    Serial.print(",");

    Serial.print(rpm, 1);
    Serial.print(",");

    Serial.println(output_pwm);
  }


  // ===================================================
  // 5. JALANKAN MOTOR L298N
  // ===================================================

  analogWrite(
    L298N_ENB_PIN,
    output_pwm
  );

  digitalWrite(
    L298N_IN3_PIN,
    LOW
  );

  digitalWrite(
    L298N_IN4_PIN,
    HIGH
  );


  // ===================================================
  // 6. UPDATE TAMPILAN LCD
  // ===================================================

  lcd.setCursor(6, 0);
  lcd.print(" ");

  lcd.setCursor(6, 0);
  lcd.print(sudutSekarang, 1);
  lcd.print((char)223);


  lcd.setCursor(4, 1);
  lcd.print(" ");

  lcd.setCursor(4, 1);
  lcd.print((int)rpm);


  lcd.setCursor(13, 1);
  lcd.print(" ");

  lcd.setCursor(13, 1);
  lcd.print(output_pwm);


  delay(1);
}
