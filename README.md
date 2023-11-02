# Python YouTube Downloader

A Python script for downloading YouTube videos using the [pytube](https://pytube.io/en/latest/) library.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Download videos in various formats and qualities from YouTube.
- Support for downloading entire playlists and channels.
- Simple command-line interface for easy interaction.
- Automatic updates to ensure compatibility with the latest YouTube changes.

## Requirements

- Python 3.6+
- Python Installation Package-managment [pip](https://pypi.org/project/pip/).
- (Optional) ffmpeg for 1080p+ video downloading.

You can install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

## Installation

1. Clone this repository:

```bash
git clone https://github.com/BadPingHere/Youtube-DL
```

2. Navigate to the project directory:

```bash
cd Youtube-DL
```

3. Install the required packages as mentioned in the Requirements section.

4. You are ready to use the YouTube downloader!

## Usage

You can use the YouTube downloader by running the either the `download_cli.py` or `download_gui.py` script, depending on the interface you perfer. If you choose a CLI, you have the options between a verbose, more detailed and longer version, or a one-liner, quick version. If you choose the verbose CLI, just run the script. If you choose the quick CLI, here are some common usage examples:

```bash
python download_cli.py --url https://www.youtube.com/watch?v=dQw4w9WgXcQ --video -- --thumbnail --captions --audio --resolution 720p
```

For more options and information, use the `--help` flag:

```bash
python download_cli.py --help
```

## Contributing

Contributions are welcome! If you want to contribute to this project, please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature or bug fix:

```bash
git checkout -b feature/your-feature
```

3. Make your changes and commit them with descriptive commit messages.

4. Push your changes to your fork:

```bash
git push origin feature/your-feature
```

5. Create a pull request to the main repository.

Please ensure that your code follows the project's coding style and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
