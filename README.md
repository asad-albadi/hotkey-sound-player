# Hotkey Sound Player

Hotkey Sound Player is a simple application that allows you to play sound files using custom hotkey combinations. It provides an easy-to-use graphical interface to set up and manage your hotkey-sound pairs.

## Features

- Select and play sound files using custom hotkey combinations
- Add, remove, and manage hotkey-sound pairs
- Start and stop the hotkey listener
- Save and load configuration from a JSON file
- Supports multiple audio formats: MP3, OGG, WAV, OGA

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/hotkey-sound-player.git
    cd hotkey-sound-player
    ```

2. Create a virtual environment and activate it:

    ```sh
    python3.12 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

    ```sh
    python hotkey_sound_player.py
    ```

2. Use the graphical interface to add sound-hotkey pairs, start the listener, and enjoy playing sounds with your hotkeys.

## Packaging

To create a standalone executable, use `pyinstaller`:

```sh
pyinstaller --onefile --windowed hotkey_sound_player.py
```

This will generate a single executable file in the dist directory.
