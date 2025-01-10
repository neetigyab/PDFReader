import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect_checkboxes(image, ignored_area=None):
    """Detect checkboxes and determine if they are checked or unchecked, ignoring specified areas."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    checkbox_states = {}
    checkbox_positions = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        if 0.8 <= aspect_ratio <= 1.5 and 10 <= w <= 30 and 10 <= h <= 30:
            # Skip checkboxes in the ignored area
            if ignored_area and (ignored_area[0] <= x <= ignored_area[0] + ignored_area[2] and
                                 ignored_area[1] <= y <= ignored_area[1] + ignored_area[3]):
                continue
            roi = gray[y+2:y+h-2, x+2:x+w-2]
            non_zero = cv2.countNonZero(roi)
            checkbox_states[(x, y)] = "Unchecked" if non_zero > (w * h * 0.45) else "Checked"
            checkbox_positions.append((x, y, w, h))

    return checkbox_states, checkbox_positions

def visualize_checkboxes(image, checkbox_positions, checkbox_states, page_number):
    """Visualize all detected checkboxes on the image."""
    for (x, y, w, h) in checkbox_positions:
        state = checkbox_states.get((x, y), "Unchecked")
        color = (0, 255, 0) if state == "Checked" else (0, 0, 255)
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(f"Checkboxes Detected on Page {page_number}")
    plt.axis("off")
    plt.show()
