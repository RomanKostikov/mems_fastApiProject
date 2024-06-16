import os
import csv
import argparse
import requests
import glob
import sys
import asyncio


def main():
    parser = argparse.ArgumentParser(
        description="Upload images to fastAPI-img-store and generate CSV with image path's and uploaded image id.")
    parser.add_argument("--image_dir", type=str, required=True,
                        help="Path to the directory with images.")
    parser.add_argument("--csv_name", type=str,
                        default="uploaded_images.csv", help="Name of the CSV file.")
    parser.add_argument("--csv_delimiter", type=str,
                        default=";", help="Delimiter for the CSV file.")
    parser.add_argument("--api_url", type=str,
                        default="http://127.0.0.1:8000/images/", help="Server API URL.")
    parser.add_argument("--request_timeout", type=int,
                        default=30, help="Timeout for API requests in seconds.")
    parser.add_argument("--max_concurrent_uploads", type=int,
                        default=5, help="Maximum number of concurrent uploads.")

    try:
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print("Error parsing arguments:", e)
        sys.exit(1)

    asyncio.run(process_images(args.image_dir, args.csv_name, args.csv_delimiter,
                args.api_url, args.request_timeout, args.max_concurrent_uploads))


async def process_images(image_dir, csv_name, csv_delimiter, api_url, request_timeout, max_concurrent_uploads):
    if not os.path.exists(image_dir):
        print(f"Error: '{image_dir}' directory not found.")
        return

    images = glob.glob(os.path.join(image_dir, "*"))

    semaphore = asyncio.Semaphore(max_concurrent_uploads)

    tasks = []
    for image_path in images:
        task = asyncio.create_task(upload_image(
            image_path=image_path, api_url=api_url, request_timeout=request_timeout, semaphore=semaphore))
        tasks.append(task)

    results = await asyncio.gather(*tasks)

    if results:
        with open(csv_name, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=csv_delimiter)
            csv_writer.writerow(["path_to_file", "id_from_server"])
            for result in results:
                if result:
                    path, image_id = result
                    csv_writer.writerow([path, image_id])


async def upload_image(image_path, api_url: str, request_timeout: int, semaphore: asyncio.Semaphore):
    async with semaphore:
        with open(image_path, 'rb') as f:
            files = {"file": ('image.jpeg', f, 'multipart/form-data')}
            try:
                response = await asyncio.to_thread(requests.post, api_url, files=files, timeout=request_timeout)

                if response.status_code == 201:
                    data = response.json()
                    image_id = data.get("ID")
                    print(f"Uploaded '{image_path}' with ID: {image_id}")
                    return image_path, image_id
                else:
                    print(
                        f"Failed to upload '{image_path}'. Status code: {response.status_code}")
            except requests.exceptions.Timeout:
                print(f"Request for '{image_path}' timed out.")
            except requests.exceptions.RequestException as e:
                print(f"Error occurred while uploading '{image_path}': {e}")


if __name__ == "__main__":
    main()