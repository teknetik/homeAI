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