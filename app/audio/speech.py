import importlib


try:
    sr = importlib.import_module("speech_recognition")
except ImportError:
    sr = None
try:
    pyttsx3 = importlib.import_module("pyttsx3")
except ImportError:
    pyttsx3 = None


# ============================================================
# SPEECH RECOGNIZER
# ============================================================

recognizer = sr.Recognizer() if sr is not None else None


# ============================================================
# TEXT TO SPEECH ENGINE
# ============================================================

tts_engine = pyttsx3.init() if pyttsx3 is not None else None


# ============================================================
# SPEECH TO TEXT
# ============================================================

def speech_to_text():

    """
    Listen to the student's microphone and
    convert speech into text.
    """

    if recognizer is None:
        return ""

    try:

        with sr.Microphone() as source:

            print("Listening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1,
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=15,
            )

        text = recognizer.recognize_google(
            audio
        )

        return text

    except sr.WaitTimeoutError:

        return ""

    except sr.UnknownValueError:

        return ""

    except sr.RequestError:

        return ""

    except Exception:

        return ""


# ============================================================
# TEXT TO SPEECH
# ============================================================

def text_to_speech(
    text: str,
):

    """
    Convert text into spoken audio.
    """

    if not text or tts_engine is None:

        return False

    try:

        tts_engine.say(
            text
        )

        tts_engine.runAndWait()

        return True

    except Exception:

        return False