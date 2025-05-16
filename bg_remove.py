import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import time


def extract_largest_object_mask(image):
    _, thresh = cv2.threshold(image, 30, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=2)
    thresh = cv2.erode(thresh, kernel, iterations=1)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return np.zeros_like(image)
    largest_contour = max(contours, key=cv2.contourArea)
    mask = np.zeros_like(image)
    cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
    return mask


def apply_background_removal(image, mask, threshold_value=10):
    _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    # Create a result image with white background (255)
    result = np.ones_like(image) * 255
    # Copy the original image pixels where the mask is white (255)
    result[mask == 255] = image[mask == 255]
    return result


def crop_to_content(image):
    _, thresh = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)
    coords = cv2.findNonZero(thresh)
    if coords is None:
        return image
    x, y, w, h = cv2.boundingRect(coords)
    return image[y : y + h, x : x + w]


# --- Main Processing Pipeline ---


def process_dataset(input_folder, visualize=False):
    processed_images = []
    image_files = sorted(
        [
            f
            for f in os.listdir(input_folder)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
    )
    print(f"Found {len(image_files)} images to process.")
    for idx, image_name in enumerate(image_files):
        image_path = os.path.join(input_folder, image_name)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print(f"Failed to load {image_name}, skipping...")
            continue

        # Step 1: Extract foreground mask
        foreground_mask = extract_largest_object_mask(image)

        # Step 2: Apply background removal with white background
        image_fg = apply_background_removal(image, foreground_mask)

        # Step 3: Crop result
        result_image = crop_to_content(image_fg)
        processed_images.append(result_image)

        # Visualize first 5 with original, mask, and background removed
        if visualize and idx < 5:
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 3, 1)
            plt.imshow(image, cmap="gray")
            plt.title("Original")

            plt.subplot(1, 3, 2)
            plt.imshow(foreground_mask, cmap="gray")
            plt.title("Foreground Mask")

            plt.subplot(1, 3, 3)
            plt.imshow(image_fg, cmap="gray")
            plt.title("Background Removed")
            plt.tight_layout()
            plt.savefig(f"visualization_{idx}.png")

        if (idx + 1) % 100 == 0:
            print(f"Processed {idx + 1}/{len(image_files)} images...")

    print(f"Processing complete. Total processed images: {len(processed_images)}")
    return processed_images


# --- Plotting Function for Resulted Images ---


def plot_processed_images(processed_images, num_images=5):
    num_images = min(num_images, len(processed_images))
    plt.figure(figsize=(15, 5))
    for i in range(num_images):
        plt.subplot(1, num_images, i + 1)
        plt.imshow(processed_images[i], cmap="gray")
        plt.title(f"Processed Image {i + 1}")
        plt.axis("off")
    plt.tight_layout()
    plt.savefig("processed_images_plot.png")


if __name__ == "__main__":
    input_folder = "/kaggle/input/gan-heart-teacher-model-dataset"
    output_folder = "/kaggle/working/processed_heart_teacher_images"
    os.makedirs(output_folder, exist_ok=True)

    start_time = time.time()
    processed_images = process_dataset(input_folder, visualize=True)
    duration = time.time() - start_time
    print(f"Processing completed in {duration:.2f} seconds.")

    print("Plotting processed images...")
    plot_processed_images(processed_images, num_images=5)

    print("Saving images...")
    for idx, img in enumerate(processed_images):
        cv2.imwrite(os.path.join(output_folder, f"processed_{idx}.png"), img)
    print(f"Saved {len(processed_images)} images to {output_folder}")
