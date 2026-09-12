<h2>📌 Deskripsi Project</h2>

<p>
Project ini merupakan sistem kendali kecepatan motor DC berbasis
<b>PID (Proportional-Integral-Derivative)</b> dengan <b>webcam sebagai input
setpoint melalui deteksi jumlah jari</b>. Sistem menggunakan Arduino Uno
sebagai kontroler real-time, sedangkan PC/laptop digunakan untuk menjalankan
deteksi tangan, GUI, dan monitoring data.
</p>

<p>
Sistem tidak menggunakan Internet of Things (IoT). Komunikasi antara Arduino
dan PC dilakukan menggunakan <b>USB Serial</b> dengan baud rate
<b>115200 bps</b>.
</p>

<p><b>Alur utama sistem:</b></p>

<p align="center">
  <b>
    🎥 Webcam → ✋ Deteksi Tangan → 🔢 Jumlah Jari → 🎯 Setpoint RPM
    → 🟦 Arduino → 🧠 PID → ⚡ PWM → L298N → ⚙️ Motor DC
  </b>
</p>

<p>
Data dari sensor kemudian dikirim kembali ke PC untuk monitoring secara
real-time.
</p>

<hr>

<h2>🎯 Tujuan</h2>

<ol>
  <li>
    Merancang sistem kendali kecepatan motor DC menggunakan Arduino Uno,
    L298N, motor DC, AS5600, ACS712, dan voltage divider.
  </li>
  <li>
    Menggunakan webcam dan MediaPipe Hands + OpenCV untuk mengubah jumlah
    jari menjadi setpoint RPM.
  </li>
  <li>
    Mengimplementasikan kontroler PID secara diskrit pada Arduino Uno.
  </li>
  <li>
    Menampilkan kecepatan motor dan data sistem secara real-time melalui
    GUI berbasis Python.
  </li>
  <li>
    Menganalisis respons sistem terhadap beberapa nilai setpoint serta
    kestabilan pembacaan sensor dan kontrol PID.
  </li>
</ol>

<hr>

<h2>✨ Fitur Utama</h2>

<table>
  <tr>
    <td>🎥</td>
    <td><b>Deteksi Gesture</b></td>
    <td>Mendeteksi jumlah jari menggunakan webcam.</td>
  </tr>
  <tr>
    <td>✋</td>
    <td><b>Input Setpoint</b></td>
    <td>Jumlah jari digunakan untuk menentukan target RPM.</td>
  </tr>
  <tr>
    <td>⚙️</td>
    <td><b>Kontrol PID</b></td>
    <td>Mengatur kecepatan motor DC secara otomatis.</td>
  </tr>
  <tr>
    <td>🔄</td>
    <td><b>Sensor AS5600</b></td>
    <td>Mengukur posisi sudut dan kecepatan motor.</td>
  </tr>
  <tr>
    <td>📊</td>
    <td><b>Monitoring Real-Time</b></td>
    <td>Menampilkan data sistem pada PC.</td>
  </tr>
  <tr>
    <td>🖥️</td>
    <td><b>GUI Python</b></td>
    <td>Menampilkan informasi dan grafik sistem.</td>
  </tr>
  <tr>
    <td>📟</td>
    <td><b>LCD 16×2</b></td>
    <td>Menampilkan sudut, RPM, dan PWM.</td>
  </tr>
  <tr>
    <td>🔌</td>
    <td><b>USB Serial</b></td>
    <td>Komunikasi Arduino dengan PC pada 115200 bps.</td>
  </tr>
  <tr>
    <td>🛡️</td>
    <td><b>Anti-Windup</b></td>
    <td>Membatasi akumulasi integral PID.</td>
  </tr>
  <tr>
    <td>🛑</td>
    <td><b>Safety Stop</b></td>
    <td>Motor dihentikan ketika setpoint = 0 RPM.</td>
  </tr>
  <tr>
    <td>📉</td>
    <td><b>Low-Pass Filter</b></td>
    <td>Menstabilkan pembacaan RPM.</td>
  </tr>
</table>

<hr>

<h2>🧩 Hardware</h2>

<table>
  <thead>
    <tr>
      <th>No.</th>
      <th>Komponen</th>
      <th>Spesifikasi</th>
      <th>Jumlah</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>Arduino Uno R3</td>
      <td>+ Kabel USB</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Driver Motor L298N</td>
      <td>Dual H-Bridge</td>
      <td>1</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Motor DC</td>
      <td>12 V, 180–190 RPM</td>
      <td>1</td>
    </tr>
    <tr>
      <td>4</td>
      <td>AS5600</td>
      <td>Magnetic Rotary Position Sensor</td>
      <td>1</td>
    </tr>
    <tr>
      <td>5</td>
      <td>Baterai</td>
      <td>9 V</td>
      <td>1</td>
    </tr>
    <tr>
      <td>6</td>
      <td>Webcam</td>
      <td>Minimal 720p</td>
      <td>1</td>
    </tr>
    <tr>
      <td>7</td>
      <td>Adaptor</td>
      <td>12 V 2 A</td>
      <td>1</td>
    </tr>
    <tr>
      <td>8</td>
      <td>PC/Laptop</td>
      <td>RAM minimal 4 GB</td>
      <td>1</td>
    </tr>
    <tr>
      <td>9</td>
      <td>Box</td>
      <td>Wadah sistem</td>
      <td>1</td>
    </tr>
    <tr>
      <td>10</td>
      <td>LCD</td>
      <td>16×2</td>
      <td>1</td>
    </tr>
    <tr>
      <td>11</td>
      <td>Saklar</td>
      <td>ON/OFF 3 pin</td>
      <td>2</td>
    </tr>
    <tr>
      <td>12</td>
      <td>Spacer</td>
      <td>2,5 cm</td>
      <td>1</td>
    </tr>
    <tr>
      <td>13</td>
      <td>ACS712</td>
      <td>Sensor arus</td>
      <td>1</td>
    </tr>
    <tr>
      <td>14</td>
      <td>Voltage Divider</td>
      <td>R1 = 10 kΩ, R2 = 4,7 kΩ</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

<hr>

<h2>💻 Software</h2>

<h3>Arduino</h3>

<ul>
  <li>Arduino IDE</li>
  <li>Arduino/C++</li>
  <li><code>Wire</code></li>
  <li><code>AS5600</code></li>
  <li><code>LiquidCrystal_I2C</code></li>
</ul>

<h3>PC / Laptop</h3>

<ul>
  <li>Python</li>
  <li>OpenCV</li>
  <li>MediaPipe Hands</li>
  <li>GUI Python</li>
  <li>PySerial</li>
</ul>

<hr>

<h2>✋ Mapping Gesture ke Setpoint</h2>

<p>
Jumlah jari yang terdeteksi oleh webcam digunakan sebagai target
kecepatan motor.
</p>

<table align="center">
  <thead>
    <tr>
      <th>Gesture</th>
      <th>Jumlah Jari</th>
      <th>Setpoint</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>☝️</td>
      <td>1 jari</td>
      <td><b>35 RPM</b></td>
    </tr>
    <tr>
      <td>✌️</td>
      <td>2 jari</td>
      <td><b>50 RPM</b></td>
    </tr>
    <tr>
      <td>🤟</td>
      <td>3 jari</td>
      <td><b>60 RPM</b></td>
    </tr>
    <tr>
      <td>🖐️</td>
      <td>4 jari</td>
      <td><b>70 RPM</b></td>
    </tr>
    <tr>
      <td>🖐️</td>
      <td>5 jari</td>
      <td><b>80 RPM</b></td>
    </tr>
  </tbody>
</table>

<p align="center">
  <i>
    Pengguna tidak perlu memasukkan nilai RPM secara manual untuk memilih
    target kecepatan.
  </i>
</p>

<hr>

<h2>⚙️ Prinsip Kerja Sistem</h2>

<b>🎥 Input Gesture</b>

<br>

<p>
Webcam menangkap gambar tangan pengguna. Python menggunakan
<b>MediaPipe Hands</b> dan <b>OpenCV</b> untuk mendeteksi landmark tangan
dan menentukan jumlah jari yang terdeteksi.
</p>


<br>

<b>🎯 Penentuan Setpoint</b>

<br>

<p>
Jumlah jari dikonversi menjadi nilai setpoint RPM:
</p>

<pre>
1 jari → 35 RPM
2 jari → 50 RPM
3 jari → 60 RPM
4 jari → 70 RPM
5 jari → 80 RPM
</pre>

<p>
Setpoint kemudian dikirim dari PC ke Arduino melalui komunikasi serial.
</p>



<h2>🔌 Komunikasi Serial</h2>

<p>Arduino menggunakan:</p>

<pre>
Serial.begin(115200);
</pre>

<p>
PC mengirim target RPM ke Arduino, sedangkan Arduino mengirim kembali:
</p>

<pre>
Sudut, RPM, PWM
</pre>

<p>
Data dikirim setelah proses pembacaan sensor dan perhitungan PID.
</p>

<hr>

<h2>📟 Tampilan LCD</h2>

<p>LCD 16×2 digunakan untuk menampilkan:</p>

<pre>
Sudut: xxx.x°
RPM: xx   PWM: xxx
</pre>

<p>Saat sistem mulai, LCD menampilkan:</p>

<pre>
 SISTEM MONITOR
 PID BERJALAN
</pre>

<hr>

<h2>🧪 Prosedur Pengujian</h2>

<ol>
  <li>1. Hubungkan Arduino Uno ke PC/laptop menggunakan kabel USB.</li>
  <li>2. Pastikan display/LCD menyala.</li>
  <li>3. Nyalakan switch untuk mengaktifkan driver motor.</li>
  <li>4. Upload program Arduino melalui Arduino IDE.</li>
  <li>5. Jalankan aplikasi Python/GUI melalui VS Code.</li>
  <li>6. Pastikan webcam dapat mendeteksi tangan.</li>
  <li>7. Tampilkan jumlah jari untuk menentukan target RPM.</li>
  <li>8. Amati motor dan perubahan RPM.</li>
li>
</ol>

<hr>

<hr>

<h2>🚀 Cara Menjalankan Project</h2>

<h3>1. Arduino</h3>

<ol>
  <li>Buka folder <code>arduino</code>.</li>
  <li>Buka file program <code>.ino</code> menggunakan Arduino IDE.</li>
  <li>Pastikan library yang diperlukan sudah terpasang.</li>
  <li>Hubungkan Arduino Uno ke PC.</li>
  <li>Upload program ke Arduino.</li>
</ol>

<h3>2. Python</h3>

<p>Install library yang diperlukan:</p>

<pre>
pip install opencv-python mediapipe pyserial
</pre>

<p>Kemudian jalankan:</p>

<pre>
python python/main.py
</pre>

<p>
Sesuaikan COM Port Arduino pada program Python sebelum menjalankan sistem.
</p>

<hr>


<h2>👥 Anggota Kelompok</h2>

<table>
  <thead>
    <tr>
      <th>Nama</th>
      <th>NRP</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Rafie Islamay Murdiato</td>
      <td>2123600036</td>
    </tr>
    <tr>
      <td>Sabrina Keisha Maharani</td>
      <td>2124600043</td>
    </tr>
    <tr>
      <td>Muchammad Ridho Andika</td>
      <td>2124600051</td>
    </tr>
    <tr>
      <td>M. Reihan Maulana</td>
      <td>2124600058</td>
    </tr>
  </tbody>
</table>

<p>
<b>Dosen Pengampu:</b> Ir. Kemalasari, M.T
</p>

<p>
<b>Program Studi:</b> Teknik Elektronika<br>
<b>Institusi:</b> Politeknik Elektronika Negeri Surabaya<br>
<b>Tahun:</b> 2026
</p>

<hr>

<h2>📚 Referensi</h2>

<ul>
  <li>Ogata, K. (2010). <i>Modern Control Engineering</i> (5th ed.). Prentice Hall.</li>
  <li><i>Hand Gesture-Based Servo Motor Control Using Edge Computing</i> (2024). ResearchGate.</li>
  <li><i>Applications of DC Motor Controllers in Robotics</i>. The Control Company.</li>
  <li><i>Gesture Recognition using Camera and MediaPipe on Raspberry Pi</i>. ZBotic.</li>
  <li><i>Kontrol Proporsional Integral Derivatif (PID) pada Kecepatan Sudut Motor DC</i> (2021). ELKOMIKA.</li>
  <li><i>Mengenal PID Controller dalam Sistem Kontrol Otomatis Industri</i> (2025). KMTech.</li>
  <li><i>Implementasi Kendali PID pada Kecepatan Motor DC</i> (2024).</li>
  <li><i>Rancang Bangun Sistem Kendali Kecepatan Motor DC</i> (2020).</li>
</ul>

<hr>

<p align="center">
  <b>⚙️ PID Motor Control + Computer Vision 🤖</b>
</p>
