#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status,
# if an undefined variable is used, or if a piped command fails.
set -euo pipefail

# --- ARGUMENT VALIDATION ---
# Check if exactly two arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Error: Missing required arguments." >&2
    echo "Usage: $0 <target_directory> <output_m3u_file>" >&2
    exit 1
fi

# Assign positional parameters to descriptive variables
TARGET_DIR="$1"
OUTPUT_M3U="$2"
MAX_DURATION="$3"  # Maximum duration in seconds (e.g. 5 minutes = 300 seconds)

# --- CONFIGURATION ---
FFPROBE_PATH="ffprobe" # Change to full path if ffprobe is not in your system PATH

# --- INITIALIZATION ---
# Verify the target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist." >&2
    exit 1
fi

# Reinitialize the M3U file with the required EXTM3U header
echo "#EXTM3U" > "$OUTPUT_M3U"
echo "M3U file reinitialized: $OUTPUT_M3U"
echo "Scanning '$TARGET_DIR' for videos shorter than 5 minutes..."

# --- MAIN PROCESS ---
# Use 'find' with case-insensitive OR logic to match extensions.
find "$TARGET_DIR" -type f \( -iname "*.mkv" -o -iname "*.webm" -o -iname "*.mp4" \) -print0 | while IFS= read -r -d '' fullName; do

    # Fetch the duration using your specified command structure
    duration_str=$("${FFPROBE_PATH}" -i "${fullName}" -show_format -v quiet | grep duration | sed 's/duration=//')

    # Ensure ffprobe returned a valid, non-empty value
    if [ -n "$duration_str" ]; then
        # Use 'bc' to perform floating-point comparison
        if (( $(echo "$duration_str < $MAX_DURATION" | bc -l) )); then
            # Round the duration to the nearest whole integer for the M3U #EXTINF tag
            duration_round=$(printf "%.0f" "$duration_str")
            basename_file=$(basename "$fullName")

            # Append metadata and file path to the playlist
            echo "#EXTINF:${duration_round},${basename_file}" >> "$OUTPUT_M3U"
            echo "${fullName}" >> "$OUTPUT_M3U"

            echo "Added (${duration_round}s): ${basename_file}"
        fi
    else
        echo "Warning: Could not read duration for ${fullName}" >&2
    fi

done

echo "Done! The playlist has been successfully generated."
