# Mind Wellness Whisperer 🧘‍♀️

Welcome to the Mind Wellness Whisperer project! This is a Streamlit-based chatbot designed to support mental wellness by providing empathetic and supportive conversations. It utilizes the Ollama language model to offer a variety of interaction modes tailored to different user needs.

## Features

- **Empathetic Conversations**: The chatbot provides supportive and empathetic responses to user inputs.
- **Text-to-Speech**: Converts responses to speech, enhancing the user experience.
- **Memory Management**: Stores chat history for continuity in conversations.
- **Tailored Interactions**: Offers specific interaction modes for venting, learning new things, relationship advice, and future planning.
- **Offline Capability**: Operates without internet access.

## Installation

### Prerequisites

- Docker
- Python 3.8 or above
- Git

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/mind-wellness-whisperer.git
    cd mind-wellness-whisperer
    ```

2. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Build and run the Docker container for model download**:
    - Ensure Docker is installed and running on your machine.
    - Use the following command to build the Docker image:
        ```bash
        docker build -t mind-wellness-whisperer .
        ```
    - Run the Docker container:
        ```bash
        docker run -p 8501:8501 mind-wellness-whisperer
        ```

## Usage

1. **Run the Streamlit application**:
    ```bash
    streamlit run app.py
    ```

2. **Interact with the chatbot**:
   - Open your browser and navigate to the local Streamlit URL provided in the terminal.
   - Use the sidebar to start a new chat, mute/unmute audio, load previous chats, or clear chat history.
   - Choose from the predefined buttons for venting, learning new things, relationship advice, or future planning.
   - Input your queries and receive supportive responses from the chatbot.

## Project Structure

- **app.py**: The main application file containing the Streamlit interface and chatbot logic.
- **requirements.txt**: The list of dependencies required to run the project.
- **Dockerfile**: Configuration file to create a Docker image for the project.
- **lottie_files**: A directory for storing Lottie animation files.

## Customization

You can customize the chatbot's behavior and responses by modifying the system messages and interaction modes in `app.py`.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or new features.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

This project uses:
- [Streamlit](https://streamlit.io/)
- [Ollama Language Model](https://ollama.ai/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)
- [Lottie Animations](https://lottiefiles.com/)
- [Docker](https://www.docker.com/)

---

Feel free to reach out if you have any questions or need further assistance. Enjoy using the Mind Wellness Whisperer!
