from pyzbar.pyzbar import decode
import cv2
import io
import csv
import numpy

i = 0
k = 0
imagetrue = cv2.imread("true.jpg")
imagefalse = cv2.imread("false.jpg")
data_list = list()
entrance = numpy.zeros(1500, dtype=int)

try:
    backup = open(r"backup.csv", "r", encoding='utf-8')

    csv_reader = csv.reader(backup, delimiter=',')
    for line in list(csv_reader)[0]:
        entrance[k] = line
        k = k + 1
except:
    pass

# print(entrance)
# newbackup = io.open(r"backup.csv", "w",encoding='utf-8')
data_base = input("(khaharan or baradaran)")
if data_base == "k":
    pathfile = r"khaharan.csv"
elif data_base == "b":
    pathfile = r"baradaran.csv"
file = io.open(pathfile, "r", encoding='utf-8')
for line in file:
    splitLine = line.split(",")
    data_list.insert(i, splitLine)
    i = i + 1
# print(list(item[3] for item in data_list))
id = list(item[3] for item in data_list)
id = list(map(int, id))
print(data_list)
cap = cv2.VideoCapture(0)


def scan_qr_code(frame):
    result = decode(frame)

    if len(result) > 0:
        qr_code_data = result[0].data.decode("utf-8")
        return int(qr_code_data)


while True:
    j = 0
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Frame', frame)

    qr_code_data = scan_qr_code(frame)

    if qr_code_data is not None:
        # پیدا کردن ایندکس عنصر
        for j in range(0, i):
            if id[j] == qr_code_data:
                print(data_list[j][0], "\nتاریخ تولد:", data_list[j][5])
                if entrance[j] == 1:
                    frame = imagefalse
                    cv2.imshow('Frame', frame)
                    cv2.waitKey(2000)
                elif entrance[j] == 0:
                    frame = imagetrue
                    cv2.imshow("Frame", frame)
                    cv2.waitKey(2000)
                    entrance[j] = 1
                    # if 1 <= j <= len(line):
                    with open("backup.csv", 'w') as file:
                        csv_writer = csv.writer(file)

                        # نوشتن داده‌ها روی فایل
                        csv_writer.writerows([list(entrance)])

                break
        print("محتوای QR کد:", qr_code_data)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

with open("output.csv", 'w', encoding='utf-8') as file:
    k = 0
    for data in data_list:
        csv_writer = csv.writer(file)

        # نوشتن داده‌ها روی فایل
        csv_writer.writerow([data[0], entrance[k]])
        k = k + 1

print("done")
