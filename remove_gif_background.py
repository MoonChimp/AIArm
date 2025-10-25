import os
from PIL import Image
import numpy as np

def remove_gif_background(input_path, output_path):
    """
    Remove background from a GIF file.
    Assumes the background is a solid color (usually the most common color in first frame).
    """
    print(f"Loading GIF from: {input_path}")

    # Open the GIF
    gif = Image.open(input_path)

    # Get GIF properties
    frames = []
    durations = []

    try:
        while True:
            # Get frame duration
            duration = gif.info.get('duration', 100)
            durations.append(duration)

            # Convert frame to RGBA
            frame = gif.convert('RGBA')
            data = np.array(frame)

            # For first frame, detect background color (most common color)
            if len(frames) == 0:
                # Get the color at corners (usually background)
                corners = [
                    tuple(data[0, 0, :3]),
                    tuple(data[0, -1, :3]),
                    tuple(data[-1, 0, :3]),
                    tuple(data[-1, -1, :3])
                ]
                # Use most common corner color as background
                bg_color = max(set(corners), key=corners.count)
                print(f"Detected background color: {bg_color}")

                # Define color tolerance
                tolerance = 30

            # Create mask for background color
            r, g, b = bg_color
            mask = (
                (np.abs(data[:, :, 0] - r) <= tolerance) &
                (np.abs(data[:, :, 1] - g) <= tolerance) &
                (np.abs(data[:, :, 2] - b) <= tolerance)
            )

            # Set alpha channel to 0 for background pixels
            data[mask, 3] = 0

            # Convert back to image
            frame_transparent = Image.fromarray(data, 'RGBA')
            frames.append(frame_transparent)

            print(f"Processed frame {len(frames)}")

            # Move to next frame
            gif.seek(gif.tell() + 1)

    except EOFError:
        pass  # End of GIF

    print(f"Total frames processed: {len(frames)}")

    # Save as new GIF with transparency
    print(f"Saving to: {output_path}")
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        transparency=0,
        disposal=2,
        optimize=False
    )

    print("Done!")

if __name__ == "__main__":
    input_file = r"D:\AIArm\NexusLogo1.gif"
    output_file = r"D:\AIArm\NexusLogo1_transparent.gif"

    remove_gif_background(input_file, output_file)
