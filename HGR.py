import cv2
import mediapipe as mp

# Initialize Media Pipe hands class.
mpHands = mp.solutions.hands
hands = mpHands.Hands()

# Initialize the webcam.
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam.
    ret, frame = cap.read()
    
    # Flip the frame horizontally for a later selfie-view display.
    frame = cv2.flip(frame, 1)
    
    # Convert the frame to RGB.
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame to detect hand landmarks.
    results = hands.process(rgb)
    
    # Check if hand landmarks are detected.
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the finger tips.
            finger_tips = [hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].y,
                           hand_landmarks.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP].y,
                           hand_landmarks.landmark[mpHands.HandLandmark.RING_FINGER_TIP].y,
                           hand_landmarks.landmark[mpHands.HandLandmark.PINKY_TIP].y]
            
            # Check if the hand is wide open.
            if all(tip > hand_landmarks.landmark[mpHands.HandLandmark.MCP].y for tip in finger_tips):
                cv2.putText(frame, "STOP", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # Check if the hand is closed.
            elif all(tip < hand_landmarks.landmark[mpHands.HandLandmark.MCP].y for tip in finger_tips):
                cv2.putText(frame, "GO", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Display the output.
    cv2.imshow('Hand Gesture Recognition', frame)
    
    # Exit on pressing 'q'.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window.
cap.release()
cv2.destroyAllWindows()