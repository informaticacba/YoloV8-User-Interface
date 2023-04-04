import subprocess
import re

def execute_yolo_command(command, output_queue):
    output_queue.put(command)
    print(command)
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in iter(process.stdout.readline, b''):
            line = line.decode("utf-8").strip()
            output_queue.put(line)

        process.stdout.close()
        process.wait()
        output_queue.put(None)
    except Exception as e:
        output_queue.put(f'Error: {e}')
        output_queue.put(None)

def update_progress(window, line):
    match = re.search(r'\((\d+)/(\d+)\)', line)
    if match:
        current_frame, total_frames = int(match.group(1)), int(match.group(2))
        progress = int(current_frame / total_frames * 100)
        window['progress'].update(progress)
        if 'progress_percentage' in window.AllKeysDict:  # Check if the element exists before updating
            window['progress_percentage'].update(f'{progress}%')  # Update the percentage text element