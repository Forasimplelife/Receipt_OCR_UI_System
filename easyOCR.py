import os
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import easyocr

# Initialize EasyOCR reader
reader = easyocr.Reader(['en', 'ch_sim'], gpu=False)  # Specify languages

# Set file paths
label_dir = "runs/detect/exp17/labels"  # Path to detection result TXT files
image_dir = "data/corrected_images"  # Path to original images
output_csv_base = "ocr_results_easyocr.csv"  # Base name for CSV output

# Auto-generate unique CSV filename
def generate_csv_filename(base_name):
    if not os.path.exists(base_name):
        return base_name
    base, ext = os.path.splitext(base_name)
    counter = 1
    while os.path.exists(f"{base}{counter}{ext}"):
        counter += 1
    return f"{base}{counter}{ext}"

# Initialize results storage
results = {}
images_with_labels = []

# Process each label file
for label_file in os.listdir(label_dir):
    if label_file.endswith(".txt"):
        image_name = label_file.replace(".txt", ".jpg")  # Assume images are in JPG format
        image_path = os.path.join(image_dir, image_name)
        label_path = os.path.join(label_dir, label_file)

        if not os.path.exists(image_path):
            print(f"Image file {image_path} not found, skipping.")
            continue

        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to read image {image_path}, skipping.")
            continue

        # Read label file
        with open(label_path, "r") as f:
            lines = f.readlines()

        # Process each detection box
        for line in lines:
            components = line.strip().split()
            class_id = int(components[0])
            x_center, y_center, width, height = map(float, components[1:5])

            # Map relative coordinates to the original image size
            h_original, w_original = image.shape[:2]
            x1 = int((x_center - width / 2) * w_original)
            y1 = int((y_center - height / 2) * h_original)
            x2 = int((x_center + width / 2) * w_original)
            y2 = int((y_center + height / 2) * h_original)

            # Special adjustment for class_1
            if class_id == 1:
                amount_width_ratio = 0.4  # Keep only the right 40% of the box
                x1 = int(x1 + (x2 - x1) * (1 - amount_width_ratio))

            # Crop the detected area
            cropped_image = image[y1:y2, x1:x2]

            # OCR recognition using EasyOCR
            try:
                ocr_result = reader.readtext(cropped_image)
                text = " ".join([res[1] for res in ocr_result]).strip()
            except Exception as e:
                text = f"OCR failed: {e}"

            # Initialize entry for this image in results
            if image_name not in results:
                results[image_name] = {}

            # Save the OCR result under the corresponding class
            results[image_name][f"class_{class_id}"] = text

            # Draw bounding box on the image
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                image,
                f"class_{class_id}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 0),
                1,
                cv2.LINE_AA,
            )

        # Add the annotated image to the list
        images_with_labels.append((image, image_name))

# # Display images with detection boxes
# if len(images_with_labels) == 1:
#     # If only one image, display it
#     image, name = images_with_labels[0]
#     plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#     plt.title(f"Image: {name}")
#     plt.axis("off")
#     plt.show()
# else:
#     # If multiple images, calculate the required number of rows
#     num_images = len(images_with_labels)
#     num_cols = 3  # Fixed number of columns
#     num_rows = (num_images + num_cols - 1) // num_cols  # Calculate rows dynamically

#     fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
#     axes = axes.flatten()

#     # Loop through images and plot
#     for idx, (img, name) in enumerate(images_with_labels):
#         axes[idx].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#         axes[idx].set_title(f"Image: {name}")
#         axes[idx].axis("off")

#     # Hide empty axes if there are fewer images than grid slots
#     for idx in range(num_images, len(axes)):
#         axes[idx].axis("off")

#     plt.tight_layout()
#     plt.show()

# Convert results to DataFrame
df = pd.DataFrame.from_dict(results, orient="index").reset_index()
df.rename(columns={"index": "image_name"}, inplace=True)

# Ensure all classes are represented in the CSV
all_classes = ['class_0', 'class_1', 'class_2']
for class_col in all_classes:
    if class_col not in df.columns:
        df[class_col] = ""  # Add empty column for missing classes

# Generate a unique CSV filename
output_csv = generate_csv_filename(output_csv_base)

# Save results to CSV with UTF-8 BOM encoding
df.to_csv(output_csv, index=False, encoding="utf-8-sig")
print(f"OCR results saved to {output_csv}")