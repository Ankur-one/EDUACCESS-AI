import importlib

st = importlib.import_module("streamlit")


# ============================================================
# BROWSER VOICE DETECTOR
# ============================================================

def show_browser_voice_detector():
    """
    Detect voices available through the browser's
    SpeechSynthesis API.

    The browser determines which voices are available.
    """

    component_html = """
    <div
        id="voice-status"
        style="
            padding: 10px;
            border: 1px solid #cccccc;
            border-radius: 8px;
            margin-top: 5px;
            font-family: Arial, sans-serif;
        "
    >
        🎙️ Detecting available browser voices...
    </div>

    <script>

    function detectVoices() {

        const voices =
            window.speechSynthesis.getVoices();

        const status =
            document.getElementById(
                "voice-status"
            );

        if (!voices || voices.length === 0) {

            status.innerHTML =
                "⚠️ No browser voices detected yet.";

            return;
        }

        status.innerHTML =
            "✅ " +
            voices.length +
            " browser voice(s) detected.";

    }


    // --------------------------------------------------------
    // Initial detection
    // --------------------------------------------------------

    detectVoices();


    // --------------------------------------------------------
    // Chrome / Edge often loads voices asynchronously
    // --------------------------------------------------------

    window.speechSynthesis.addEventListener(
        "voiceschanged",
        detectVoices
    );

    </script>
    """

    st.components.v1.html(
        component_html,
        height=65,
    )


# ============================================================
# VOICE INFORMATION
# ============================================================


def show_voice_information():
    st.markdown(
        "#### 🎙️ Browser Voice Information"
    )

    st.caption(
        "The available voices depend on your browser "
        "and operating system."
    )

    st.info(
        "💡 Chrome and Edge may load voices a few moments "
        "after the Tutor page opens."
    )

