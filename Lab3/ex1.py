from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from chei import *
from array import array
from PIL import Image
import sys
import time
import Levenshtein


computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

img = open("test2.png", "rb")
img2 = open("img.png", "rb")
read_response = computervision_client.read_in_stream(
    image=img,
    #image=img2
    mode="Printed",
    raw=True
)

operation_id = read_response.headers['Operation-Location'].split('/')[-1]
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Print the detected text, line by line
detected_text_lines = []
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            detected_text_lines.append(line.text)

print()

groundTruth = ["Succes in rezolvarea", "tEMELOR la", "LABORAtoaree de", "Inteligenta Artificiala!"]
#groundTruth=["Google Cloud","Platform"]
detected_text = " ".join(detected_text_lines)
ground_truth = " ".join(groundTruth)


cer = Levenshtein.distance(detected_text, ground_truth) / len(ground_truth)
print("Character Error Rate (CER):", cer)

detected_words = detected_text.split()
ground_truth_words = ground_truth.split()
wer = Levenshtein.distance(" ".join(detected_words), " ".join(ground_truth_words)) / len(ground_truth_words)
print("Word Error Rate (WER):", wer)

# compute the performance
no_of_correct_lines = sum(i == j for i, j in zip(detected_text_lines, groundTruth))
print("Number of Correct Lines:", no_of_correct_lines)


detected_text = " ".join(detected_text_lines)
ground_truth_text = " ".join(groundTruth)

similarity_ratio = Levenshtein.ratio(detected_text, ground_truth)
print("Edit Distance Ratio:", similarity_ratio)
distance = Levenshtein.distance(detected_text, ground_truth)
print("Levenshtein Distance:", distance)
