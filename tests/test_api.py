import os
import google.generativeai as genai
import json

import cv2
import numpy as np


def parse_detection(response_text):
    czysty_tekst = response_text.replace('```json', '').replace('```', '').strip()

    try:
        dane = json.loads(czysty_tekst)
    except json.JSONDecodeError as error:
        raise ValueError("Odpowiedź modelu nie jest poprawnym formatem JSON.") from error

    if isinstance(dane, list):
        if not dane or not isinstance(dane[0], dict):
            raise ValueError("Odpowiedź modelu musi zawierać obiekt detekcji.")
        dane = dane[0]

    if not isinstance(dane, dict):
        raise ValueError("Odpowiedź modelu musi być obiektem JSON.")

    return dane

def test_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Ustaw zmienną środowiskową GEMINI_API_KEY przed uruchomieniem testu.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-3.5-flash-lite')
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "test_image.jpg")

    # odczyt pliku jako bajty
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # obiekt strukturalny zrozumiały dla Gemini API
    image_blob = {
        "mime_type": "image/jpeg",
        "data": image_bytes
    }

    prompt = (
        "Zidentyfikuj główny obiekt na tym zdjęciu. "
        "Zwróć odpowiedź w formacie JSON. "
        "Format musi wyglądać dokładnie tak: {\"obiekt\": \"nazwa\", \"bounding_box\": [ymin, xmin, ymax, xmax]}"
    )
    
    response = model.generate_content([prompt, image_blob])
    print(response.text)

    dane = parse_detection(response.text)

    stream = np.fromfile(image_path, dtype=np.uint8)
    img_cv = cv2.imdecode(stream, cv2.IMREAD_COLOR)

    
    height, width, _ = img_cv.shape
    # skalowanie znormalizowanych współrzędnych Gemini (0-1000) do faktycznych pikseli zdjęcia
    box = dane.get('bounding_box')
    ymin = int((box[0] / 1000) * height)
    xmin = int((box[1] / 1000) * width)
    ymax = int((box[2] / 1000) * height)
    xmax = int((box[3] / 1000) * width)

    # ramka
    cv2.rectangle(img_cv, (xmin, ymin), (xmax, ymax), (0, 255, 0), 1)

    cv2.imshow(f"Znaleziono: {dane.get('obiekt')}", img_cv)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # print("Dostępne modele generujące:")
    # for m in genai.list_models():
    #     if 'generateContent' in m.supported_generation_methods:
    #         print(m.name)
    test_gemini()