import os
from PIL import Image, ImageFilter
import numpy as np

def remove_gif_background_advanced(input_path, output_path, tolerance=40, edge_feather=2):
    """
    Remove background from a GIF with improved edge handling.

    Args:
        input_path: Path to input GIF
        output_path: Path to output GIF
        tolerance: Color difference tolerance (higher = more aggressive removal)
        edge_feather: Pixels to smooth at edges (reduces pixelation)
    """
    print(f"Loading GIF from: {input_path}")

    gif = Image.open(input_path)
    frames = []
    durations = []
    bg_color = None

    try:
        frame_num = 0
        while True:
            duration = gif.info.get('duration', 100)
            durations.append(duration)

            # Convert to RGBA
            frame = gif.convert('RGBA')
            data = np.array(frame).astype(np.float32)

            # Detect background color from first frame
            if bg_color is None:
                # Sample multiple edge points
                h, w = data.shape[:2]
                edge_samples = []

                # Top and bottom edges
                for x in range(0, w, max(1, w//10)):
                    edge_samples.append(tuple(data[0, x, :3].astype(int)))
                    edge_samples.append(tuple(data[h-1, x, :3].astype(int)))

                # Left and right edges
                for y in range(0, h, max(1, h//10)):
                    edge_samples.append(tuple(data[y, 0, :3].astype(int)))
                    edge_samples.append(tuple(data[y, w-1, :3].astype(int)))

                # Find most common color
                from collections import Counter
                bg_color = Counter(edge_samples).most_common(1)[0][0]
                print(f"Detected background color: RGB{bg_color}")
                print(f"Using tolerance: {tolerance}, edge feather: {edge_feather}")

            # Calculate color distance from background
            r, g, b = bg_color
            color_dist = np.sqrt(
                (data[:, :, 0] - r)**2 +
                (data[:, :, 1] - g)**2 +
                (data[:, :, 2] - b)**2
            )

            # Create alpha channel based on distance
            # Pixels closer to bg_color become more transparent
            alpha = np.clip(color_dist / tolerance * 255, 0, 255).astype(np.uint8)

            # Apply feathering to smooth edges
            if edge_feather > 0:
                alpha_img = Image.fromarray(alpha, 'L')
                alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(edge_feather))
                alpha = np.array(alpha_img)

            # Set alpha channel
            data[:, :, 3] = alpha

            # Convert back to image
            frame_transparent = Image.fromarray(data.astype(np.uint8), 'RGBA')
            frames.append(frame_transparent)

            frame_num += 1
            if frame_num % 50 == 0:
                print(f"Processed {frame_num} frames...")

            gif.seek(gif.tell() + 1)

    except EOFError:
        pass

    print(f"Total frames processed: {len(frames)}")
    print(f"Saving to: {output_path}")

    # Save with transparency
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=False
    )

    print("Done!")
    print(f"\nFile saved: {output_path}")

    # Show file size
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"File size: {size_mb:.2f} MB")

if __name__ == "__main__":
    input_file = r"D:\AIArm\NexusLogo1.gif"
    output_file = r"D:\AIArm\NexusLogo1_transparent_v2.gif"

    # Try with higher tolerance and more edge smoothing
    remove_gif_background_advanced(input_file, output_file, tolerance=50, edge_feather=3)
