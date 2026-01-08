import json
import boto3
import cv2
import mediapipe as mp
import numpy as np
import tempfile

s3 = boto3.client("s3")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5
)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles



def lambda_handler(event, context):
    try:
        # Get S3 info
        print("EVENT RECEIVED:")
        record = event["Records"][0]
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        # Download image to temp file
        with tempfile.NamedTemporaryFile() as tmp:
            s3.download_file(bucket, key, tmp.name)
            image = cv2.imread(tmp.name)

        annotated_image = image.copy()

        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Run MediaPipe
        results = hands.process(image_rgb)

        detected = results.multi_hand_landmarks is not None
        landmarks = []

        if detected:
            for hand in results.multi_hand_landmarks:
                landmarks.append([
                    {"x": lm.x, "y": lm.y, "z": lm.z}
                    for lm in hand.landmark
                ])

        output = {
            "image": key,
            "hand_detected": detected,
            "num_hands": len(landmarks),
            "landmarks": landmarks
        }


        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
              	annotated_image,
              	hand_landmarks,
              	mp_hands.HAND_CONNECTIONS,
              	mp_drawing_styles.get_default_hand_landmarks_style(),
              	mp_drawing_styles.get_default_hand_connections_style()
            	 )



        result_key = key.replace("uploads/", "results/")

        with tempfile.NamedTemporaryFile(suffix=".jpg") as out:
            cv2.imwrite(out.name, annotated_image)
            s3.upload_file(out.name, bucket, result_key)





        print(json.dumps(output))
        return output

    except Exception as e:
        print(str(e))
        raise
