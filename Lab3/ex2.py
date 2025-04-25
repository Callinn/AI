from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import time
from chei import *
# Setează cheile și endpointul
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Încarcă imaginea
img = open("test2.png", "rb")
img2 = open("img.png", "rb")
read_response = computervision_client.read_in_stream(
    image=img,
    #image=img2,
    mode="Printed",
    raw=True
)

# Așteaptă până când procesul de recunoaștere a textului se finalizează
operation_id = read_response.headers['Operation-Location'].split('/')[-1]
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Extrage bounding box-urile detectate
detected_boxes = []
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            bbox = line.bounding_box  # Lista cu 8 coordonate (x, y)
            x_min = min(bbox[0], bbox[2], bbox[4], bbox[6])
            y_min = min(bbox[1], bbox[3], bbox[5], bbox[7])
            x_max = max(bbox[0], bbox[2], bbox[4], bbox[6])
            y_max = max(bbox[1], bbox[3], bbox[5], bbox[7])

            detected_boxes.append((x_min, y_min, x_max, y_max))

# Exemplu de ground truth pentru bounding box-uri
# Aceste valori ar trebui să fie furnizate manual sau extrase dintr-o sursă externă
ground_truth_boxes = [
    (76, 295, 1337, 459),
    (128, 579, 1045, 724),
    (78, 918, 1005, 1027),
    (100, 1127, 1455, 1367)
]

# Funcție pentru calcularea IoU (Intersection over Union)
def iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou

# Calcularea scorurilor IoU pentru fiecare pereche de bounding boxes
iou_scores = [iou(det, gt) for det, gt in zip(detected_boxes, ground_truth_boxes)]
print("IoU scores:", iou_scores)

mean_iou = sum(iou_scores) / len(iou_scores)
print("Mean IoU:", mean_iou)

# Funcții pentru calcularea Precision, Recall și F1-score
def calculate_precision_recall(detected_boxes, ground_truth_boxes, iou_threshold=0.5):
    tp = 0  # True Positives (bounding boxes corect detectate)
    fp = 0  # False Positives (bounding boxes greșite)
    fn = 0  # False Negatives (bounding boxes care trebuiau detectate dar lipsesc)

    matched_gt = set()

    for det in detected_boxes:
        matched = False
        for i, gt in enumerate(ground_truth_boxes):
            if i not in matched_gt and iou(det, gt) >= iou_threshold:
                tp += 1
                matched_gt.add(i)
                matched = True
                break
        if not matched:
            fp += 1

    fn = len(ground_truth_boxes) - len(matched_gt)

    #Din toate boxurile detectate, câte au fost corecte? IoU >= 0.5
    precision = tp / (tp + fp) if tp + fp > 0 else 0
    #Din toate boxurile corecte (ground truth), câte au fost găsite?
    recall = tp / (tp + fn) if tp + fn > 0 else 0
    #O medie armonică între precision și recall.
    f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

    return precision, recall, f1_score

# Calcularea Precision, Recall și F1-score
precision, recall, f1_score = calculate_precision_recall(detected_boxes, ground_truth_boxes)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1_score)
