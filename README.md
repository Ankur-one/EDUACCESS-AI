\# EduAccess-AI



\## AI-Powered Inclusive Learning Platform for Students with Disabilities



EduAccess-AI is an accessibility-focused AI learning platform designed to help students with different disabilities learn through personalized, interactive, and multimodal educational support.



The platform combines Artificial Intelligence, Text-to-Speech, Speech-to-Text, multilingual support, Retrieval-Augmented Generation (RAG), accessibility preferences, and personalized tutoring into one application.



\---



\## Features



\### 1. User Authentication



\- User registration

\- Secure password hashing

\- Login and logout

\- Session management

\- User-specific learning preferences



\### 2. AI Tutor



EduAccess-AI provides an interactive AI tutor that can:



\- Answer educational questions

\- Explain difficult concepts

\- Provide simple explanations

\- Explain topics step by step

\- Repeat important concepts

\- Provide personalized learning assistance



\### 3. Accessibility Support



The platform provides accessibility options including:



\- Simple explanations

\- Step-by-step learning

\- Repetition support

\- Visual explanation support

\- Large text support

\- High contrast mode

\- Dyslexia-friendly mode



\### 4. Text-to-Speech



The application supports browser-based Text-to-Speech.



Users can configure:



\- Voice

\- Speech rate

\- Volume

\- Pitch

\- Autoplay

\- Text-to-Speech enable/disable



TTS preferences can be stored for the user.



\### 5. Speech-to-Text



Students can interact with the tutor using voice input.



Speech-to-Text allows users to:



\- Record a question

\- Convert speech into text

\- Send the converted question to the AI tutor



\### 6. Multilingual Learning



The platform supports multilingual learning and can provide educational assistance in different languages.



\### 7. Conversation History



Tutor conversations are stored in the database.



Each conversation can contain:



\- User

\- Session ID

\- Question

\- AI answer

\- Creation timestamp



This allows users to maintain their learning history.



\### 8. RAG Support



The project includes Retrieval-Augmented Generation functionality for improving AI responses using relevant educational information.



\### 9. Database



The project uses SQLAlchemy for database management.



The database stores:



\- User accounts

\- Accessibility preferences

\- TTS preferences

\- Tutor conversations



\### 10. Modular Architecture



The application is divided into independent modules for better maintainability.



\---



\# Project Architecture



```text

EduAccess-AI/

│

├── app/

│   │

│   ├── accessibility/

│   │   └── Accessibility functionality

│   │

│   ├── ai/

│   │   ├── tutor.py

│   │   ├── prompts.py

│   │   └── AI tutor functionality

│   │

│   ├── audio/

│   │   ├── tts.py

│   │   └── stt.py

│   │

│   ├── auth/

│   │   ├── authentication

│   │   ├── password management

│   │   └── session management

│   │

│   ├── communication/

│   │

│   ├── config/

│   │

│   ├── database/

│   │   ├── database.py

│   │   ├── models.py

│   │   └── crud.py

│   │

│   ├── learning/

│   │

│   ├── multilingual/

│   │

│   ├── rag/

│   │

│   ├── speech/

│   │

│   ├── ui/

│   │   ├── tutor.py

│   │   ├── tutor\_history.py

│   │   ├── tutor\_preferences.py

│   │   └── tutor\_accessibility.py

│   │

│   ├── vision/

│   │

│   └── main.py

│

├── requirements.txt

├── README.md

├── .gitignore

└── ...

