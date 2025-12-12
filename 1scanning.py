import cv2 #bawaan opencv untuk vision
import os #os untuk simulasi data file and folder dari python
import numpy as np #mengubah gambar jadi angka bawaan numpy
from PIL import Image #memanipulasi gambar bawaan dari pillow

# --- KONFIGURASI ---
DATASET_FOLDER = 'dataset' #folder menyimpan data gambar
TRAINER_FILE = 'trainer.yml' #folder menyimpan data gambar yang dilatih
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml" #bawaan dari file xml mendeteksi keberadaan wajah

# Buat folder dataset otomatis kalau belum ada
if not os.path.exists(DATASET_FOLDER):
    os.makedirs(DATASET_FOLDER)

# Inisialisasi Detektor & Pengenal
face_detector = cv2.CascadeClassifier(CASCADE_PATH) #deteksi bahwa itu manusia
recognizer = cv2.face.LBPHFaceRecognizer_create() #mendeteksi wajah menggunakan lbph

def ambil_foto_wajah():
    print("\n[PROSES 1] PENGAMBILAN DATA WAJAH")
    cam = cv2.VideoCapture(0)
    user_id = input('Masukkan ID User (Angka, contoh: 1): ')
    print("Lihat ke kamera... Tunggu sampai 30 foto terambil.")
    
    count = 0
    while True:
        ret, img = cam.read() #kalo kamera tidak kebuka, break
        if not ret: break
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #mengubah gambar ke warna gray
        faces = face_detector.detectMultiScale(gray, 1.3, 5) #scala detect wajah

        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2) #kotak wajah
            count += 1
            # Simpan foto
            nama_file = f"{DATASET_FOLDER}/User.{user_id}.{count}.jpg" #memformat data
            cv2.imwrite(nama_file, gray[y:y+h,x:x+w])
            print(f"Ambil foto ke-{count}")

        cv2.imshow('Daftar Wajah Baru', img)
        
        # Stop jika sudah 30 foto atau tekan ESC
        k = cv2.waitKey(100) & 0xff
        if k == 27 or count >= 30:
            break
            
    cam.release()
    cv2.destroyAllWindows()
    
    print("Pengambilan foto selesai! Lanjut ke training...")
    latih_wajah() # Langsung otomatis training setelah foto

def latih_wajah():
    print("\n[PROSES 2] MELATIH KECERDASAN (TRAINING)")
    
    path = DATASET_FOLDER #memakili proses dataset
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)] #mengurutkan file
    faceSamples=[] #menampung data visual
    ids = [] #memberikan keterangan id

    if len(imagePaths) == 0:
        print("Error: Folder dataset kosong! Ambil foto dulu.")
        return

    for imagePath in imagePaths:
        # Skip jika bukan file gambar (misal file .gitkeep atau folder)
        if os.path.split(imagePath)[-1][0] == '.': continue

        try:
            PIL_img = Image.open(imagePath).convert('L') # Convert ke grayscale
            img_numpy = np.array(PIL_img,'uint8')
            
            # Ambil ID dari nama file (User.1.jpg)
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            
            faces = face_detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
        except Exception as e:
            pass # Skip file yang error/bukan format benar

    recognizer.train(faceSamples, np.array(ids))
    recognizer.write(TRAINER_FILE) # Simpan hasil belajar
    print(f"Training Selesai! {len(np.unique(ids))} wajah telah dipelajari.")
    print("Sekarang kamu bisa jalankan mode Security.")

def jalankan_security():
    print("\n[PROSES 3] MODAL KEAMANAN AKTIF")
    
    if not os.path.exists(TRAINER_FILE):
        print("Error: Data 'trainer.yml' belum ada. Pilih menu 1 dulu!")
        return

    recognizer.read(TRAINER_FILE) # Baca data otak
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Daftar Nama (ID 0 kosong, ID 1 = Owner)
    names = ['None', 'OWNER (DAFFA)', 'USER 2', 'USER 3'] 
    
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    print("Tekan 'ESC' untuk berhenti.")
    
    while True:
        ret, img = cam.read()
        if not ret: break

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(int(minW), int(minH)))

        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

            # Confidence < 50 artinya sangat cocok (0 = identik)
            # Confidence > 50 artinya agak beda
            if (confidence < 60): 
                try:
                    name = names[id]
                except:
                    name = f"User {id}"
                confidence_text = f"{round(100 - confidence)}%"
                color = (0, 255, 0)
            else:
                name = "STRANGER"
                confidence_text = f"{round(100 - confidence)}%"
                color = (0, 0, 255)
            
            cv2.putText(img, str(name), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence_text), (x+5,y+h-5), font, 1, color, 1)
        
        cv2.imshow('Sistem Keamanan',img) 
        if cv2.waitKey(10) & 0xff == 27: break

    cam.release()
    cv2.destroyAllWindows()

# --- MENU UTAMA ---
if __name__ == "__main__":
    while True:
        print("\n=== MENU SECURITY DAFFA ===")
        print("1. Daftar Wajah Baru (Ambil Foto & Training)")
        print("2. Mulai Kamera Keamanan")
        print("3. Keluar")
        
        pilihan = input("Pilih menu (1/2/3): ")
        
        if pilihan == '1':
            ambil_foto_wajah()
        elif pilihan == '2':
            jalankan_security()
        elif pilihan == '3':
            print("Sampai jumpa!")
            break
        else:
            print("Pilihan tidak ada.")