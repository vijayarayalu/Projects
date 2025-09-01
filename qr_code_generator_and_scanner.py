import cv2
import qrcode
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


# QR Code Generator 
def generate_qr(data, filename="qrcode.png"):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"[INFO] QR Code saved as {filename}")


#  QR Code Scanner (Image)
def scan_qr_from_image(image_path):
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    if data:
        print(f"[DECODED] {data}")
    else:
        print("[INFO] No QR code found in the image.")


# QR Code Scanner (Webcam) 
def scan_qr_from_webcam():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    print("[INFO] Starting webcam... Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            print(f"[DECODED] {data}")
            if bbox is not None:
                pts = bbox.astype(int).reshape(-1, 2)
                for i in range(len(pts)):
                    cv2.line(frame, tuple(pts[i]), tuple(pts[(i + 1) % len(pts)]), (0, 255, 0), 2)
                cv2.putText(frame, data, (pts[0][0], pts[0][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# Tkinter GUI 
def gui_app():
    def generate_qr_gui():
        data = entry.get()
        if not data:
            messagebox.showwarning("Warning", "Enter some data to generate QR")
            return
        generate_qr(data, "qrcode_gui.png")
        img = Image.open("qrcode_gui.png")
        img = img.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        qr_label.config(image=img_tk)
        qr_label.image = img_tk

    def scan_image_gui():
        filepath = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
        )
        if filepath:
            scan_qr_from_image(filepath)

    root = tk.Tk()
    root.title("QR Code Generator & Scanner")

    tk.Label(root, text="Enter Data for QR Code:").pack(pady=5)
    entry = tk.Entry(root, width=40)
    entry.pack(pady=5)

    tk.Button(root, text="Generate QR", command=generate_qr_gui).pack(pady=5)
    tk.Button(root, text="Scan from Image", command=scan_image_gui).pack(pady=5)
    tk.Button(root, text="Scan from Webcam", command=scan_qr_from_webcam).pack(pady=5)

    qr_label = tk.Label(root)
    qr_label.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    print("Choose an option:")
    print("1. Generate QR Code")
    print("2. Scan QR from Image")
    print("3. Scan QR from Webcam")
    print("4. Launch GUI")

    choice = input("Enter choice (1-4): ")

    if choice == "1":
        data = input("Enter data (text/URL/etc.): ")
        generate_qr(data)
    elif choice == "2":
        path = input("Enter image path: ")
        scan_qr_from_image(path)
    elif choice == "3":
        scan_qr_from_webcam()
    elif choice == "4":
        gui_app()
    else:
        print("Invalid choice!")

