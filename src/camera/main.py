import cv2

cap = cv2.VideoCapture(0)
width, height = 640, 500

def obj_data(img):
    image_input = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (width, height))
    obj_data(frame)

    cv2.imshow("FRAME", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
