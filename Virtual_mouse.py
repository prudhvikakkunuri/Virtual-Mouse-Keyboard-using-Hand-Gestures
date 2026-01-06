import cv2
import mediapipe as mp
import pyautogui
import math
import time
SCREEN_W, SCREEN_H = 1380, 800
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, SCREEN_W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, SCREEN_H)

pyautogui.FAILSAFE = False
screen_w, screen_h = pyautogui.size()


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils


keys = [
    ["Q","W","E","R","T","Y","U","I","O","P"],
    ["A","S","D","F","G","H","J","K","L",","],
    ["Z","X","C","V","B","N","M",";","___","<<<"]
]

key_w, key_h = 90, 105
keyboard_x = 50
keyboard_y = 280

typed_text = ""
clicked = False
last_press_time = 0
prev_iy = 0   


window_name = "Virtual Mouse + Keyboard + Input Box"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, SCREEN_W, SCREEN_H)


def draw_input_box(img, text):
    cv2.rectangle(img, (50, 40), (SCREEN_W - 50, 120), (0, 255, 0),cv2.FILLED)
    cv2.putText(img, text[-60:], (60, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0), 2)

def draw_keyboard(img):
    for i, row in enumerate(keys):
        for j, key in enumerate(row):
            x = keyboard_x + j * key_w
            y = keyboard_y + i * key_h
            cv2.rectangle(img, (x, y), (x + key_w, y + key_h),(255, 0, 0),cv2.FILLED)
            cv2.putText(img, key, (x + 10, y + 45),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)

def handle_key_press(key):
    global typed_text
    if key == "___":
        typed_text += " "
        pyautogui.press("space")
    elif key == "<<<":
        typed_text = typed_text[:-1]
        pyautogui.press("backspace")
    else:
        typed_text += key
        pyautogui.press(key.lower())

def check_key_press(ix, iy):
    global last_press_time
    for i, row in enumerate(keys):
        for j, key in enumerate(row):
            x = keyboard_x + j * key_w
            y = keyboard_y + i * key_h
            if x < ix < x + key_w and y < iy < y + key_h:
                if time.time() - last_press_time > 0.5:
                    handle_key_press(key)
                    last_press_time = time.time()


while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (SCREEN_W, SCREEN_H))
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    draw_input_box(frame, typed_text)
    draw_keyboard(frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            ix = int(hand_landmarks.landmark[8].x * w)
            iy = int(hand_landmarks.landmark[8].y * h)
            tx = int(hand_landmarks.landmark[4].x * w)
            ty = int(hand_landmarks.landmark[4].y * h)


            mx = screen_w / w * ix
            my = screen_h / h * iy
            pyautogui.moveTo(mx, my)

            distance = math.hypot(ix - tx, iy - ty)

            if distance < 30:
                if not clicked:
                    pyautogui.click()
                    clicked = True
            else:
                clicked = False


            if prev_iy != 0:
                if iy - prev_iy > 25:   # tap threshold
                    check_key_press(ix, iy)

            prev_iy = iy,

            cv2.circle(frame, (ix, iy), 8, (0,255,0), -1)

    cv2.imshow(window_name, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
