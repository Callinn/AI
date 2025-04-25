import tempfile

import cv2
import numpy as np
import time
import Levenshtein
from spellchecker import SpellChecker
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from chei import *

spell_checker = SpellChecker()

# === Configurări ===
image_path = "test2.png"
apply_denoise = True
apply_binarization = False
apply_contrast = False

# === Funcții pentru preprocesare ===
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = gray

    if apply_denoise:
        result = cv2.fastNlMeansDenoising(result, None, 30, 7, 21)

    if apply_binarization:
        result = cv2.adaptiveThreshold(result, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    if apply_contrast:
        alpha = 1.5  # contrast
        beta = 0     # luminozitate
        result = cv2.convertScaleAbs(result, alpha=alpha, beta=beta)

    return result

# === OCR cu Azure ===
def run_azure(image_path):
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    with open(image_path, "rb") as image_stream:
        read_response = computervision_client.read_in_stream(image=image_stream, mode="Printed", raw=True)

    operation_id = read_response.headers['Operation-Location'].split('/')[-1]
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    lines = []
    boxes = []
    if read_result.status == OperationStatusCodes.succeeded:
        for result in read_result.analyze_result.read_results:
            for line in result.lines:
                lines.append(line.text)
                bbox = line.bounding_box
                x_min = min(bbox[0::2])
                y_min = min(bbox[1::2])
                x_max = max(bbox[0::2])
                y_max = max(bbox[1::2])
                boxes.append((x_min, y_min, x_max, y_max))
    return " ".join(lines), boxes

# === Evaluare CER & WER ===
def evaluate_ocr(output_text, ground_truth):
    gt_text = " ".join(ground_truth)
    cer = Levenshtein.distance(output_text.strip(), gt_text) / len(gt_text)
    wer = Levenshtein.distance(" ".join(output_text.strip().split()), " ".join(gt_text.split())) / len(gt_text.split())
    return cer, wer

# === Corectare ortografică ===
def correct_text(text):
    corrected = []
    for word in text.split():
        suggestion = spell_checker.correction(word)
        if suggestion is None:
            corrected.append(word)
        else:
            corrected.append(suggestion)
    return " ".join(corrected)
# === Afișare box-uri ===
def draw_boxes(image, boxes, save_path="output_boxes.png"):
    for box in boxes:
        x_min, y_min, x_max, y_max = map(int, box)
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
    cv2.imwrite(save_path, image)
    print(f"[i] Imaginea cu box-urile a fost salvată la: {save_path}")

# === Main ===
if __name__ == "__main__":
    # Ground truth
    ground_truth = ["Succes in rezolvarea", "tEMELOR la", "LABORAtoaree de", "Inteligenta Artificiala!"]

    image = cv2.imread(image_path)
    processed_image = preprocess_image(image)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_image_path = temp_file.name
        cv2.imwrite(temp_image_path, processed_image)

    # OCR Azure
    azure_text, boxes = run_azure(temp_image_path)
    azure_cer, azure_wer = evaluate_ocr(azure_text, ground_truth)

    print("\n--- Azure OCR ---")
    print("Text:", azure_text.strip())
    print(f"CER: {azure_cer:.4f} | Accuracy: {(1 - azure_cer) * 100:.2f}%")
    print(f"WER: {azure_wer:.4f} | Accuracy: {(1 - azure_wer) * 100:.2f}%")

    # Corectare ortografică Azure
    corrected_azure = correct_text(azure_text)
    print("\nText Azure corectat:", corrected_azure)

    # Desenare bounding box-uri
    draw_boxes(image.copy(), boxes)
