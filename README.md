
# HomeAI - Your Personal AI Assistant

Welcome to HomeAI, your next-generation home AI assistant that leverages some of the most advanced technologies available to create a truly interactive and responsive home environment. HomeAI integrates OpenAI's GPT-4-turbo for smart decision-making and content generation, ElevenLabs for high-quality text-to-speech, OpenAI Whisper for accurate speech-to-text, and Pico Labs' Porcupine for efficient wake word detection, making it an all-in-one solution for your smart home needs.

## Getting Started

### Cloning the Repository

To get started with HomeAI, you'll first need to clone the repository to your local machine. You can do this by opening a terminal and running the following command:

\```bash
git clone git@github.com:teknetik/homeAI.git
\```

This command clones the repository, allowing you to work on it locally.

### Setting Up Environment Variables

HomeAI requires several API keys to function correctly. These keys are stored in an environment file (.env) for security. Follow these steps to set up your environment file:

1. In the terminal, navigate to the root directory of your cloned repository.
2. Copy the `.env_example` file to a new file named `.env`:

\```bash
cp .env_example .env
\```

3. Open the `.env` file in your preferred text editor.
4. Fill in the placeholders with your API keys for OpenAI, ElevenLabs, Pico, and any other services required by HomeAI.

**Note:** The `.env` file is crucial for the operation of HomeAI as it contains sensitive information. Never share or commit this file to public repositories.

### Application Overview

HomeAI is designed to be your personal assistant, providing various services such as:

- **Generating Text & Answers:** Using OpenAI's GPT-4-turbo, HomeAI can generate text, provide answers to questions, and decide on actions to take in different scenarios.
- **Text to Speech:** Leveraging ElevenLabs' technology, HomeAI can convert text into natural-sounding speech, making the interaction with your home feel more personal and engaging.
- **Speech to Text:** With OpenAI Whisper, HomeAI can accurately transcribe spoken words into text, allowing for seamless voice commands and queries.
- **Wake Word Detection:** Pico Labs' Porcupine is utilized for efficient wake word detection, ensuring that HomeAI is always ready to respond to your commands.

## Conclusion

HomeAI is at the forefront of home assistant technology, integrating powerful tools to make your life easier and your home smarter. If you have any questions or need further assistance, please open an issue in this repository.

Thank you for choosing HomeAI as your home's AI assistant.

## Setting Up Pipenv on Ubuntu

`Pipenv` is a dependency manager for Python projects. If you're using Ubuntu, you can follow these steps to install and use `Pipenv` with HomeAI.

### Installation

1. **Update your package list** to ensure you can download the latest versions of the software:

\```bash
sudo apt update
\```

2. **Install Pipenv** using `apt`. Pipenv allows you to create a virtual environment for the project and manage its dependencies:

\```bash
sudo apt install pipenv
\```

### Usage

After installing Pipenv, you can set up your project's environment and install its dependencies.

1. **Navigate to your project directory** where the `Pipfile` and `Pipfile.lock` are located.

\```bash
cd path/to/homeAI
\```

2. **Install project dependencies** by running:

\```bash
pipenv install
\```

This command reads the `Pipfile` and installs the necessary packages inside a new virtual environment specifically for HomeAI.

3. **Activate the virtual environment** to use it. This step ensures that you are using the correct versions of the tools and libraries required by HomeAI:

\```bash
pipenv shell
\```

4. **Run HomeAI** within the virtual environment. Any Python command or script should now be run within this environment to ensure consistency and avoid conflicts with other projects.

### Exiting the Virtual Environment

When you're done working with HomeAI, you can exit the virtual environment by typing:

\```bash
exit
\```

This command will return you to your system's global Python environment, where you can work on other projects or perform general tasks.


## Change Log

### Version 0.0.0.1

- Initial release of HomeAI.
- Integrated OpenAI's GPT-4-turbo for text generation and decision-making.
- Utilized ElevenLabs for high-quality text-to-speech conversion.
- Incorporated OpenAI Whisper for accurate speech-to-text transcription.
- Integrated Pico Labs' Porcupine for efficient wake word detection.

### Version 0.0.0.2

- Added support for Groq LPU Inference Engine for faster AI processing.
- Enhanced wake word detection accuracy using Pico Labs' Porcupine.
- Improved text generation - Stella now creates shorter spoken responses, while asyncronously generating longer text responses.
- Implemented Picovoice "Koala noise suppression for better speech-to-text accuracy.