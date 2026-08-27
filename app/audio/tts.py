import importlib


# ============================================================
# STREAMLIT
# ============================================================

st = importlib.import_module("streamlit")


# ============================================================
# TEXT TO SPEECH
# ============================================================

def show_text_to_speech(
    text: str,
    language: str = "en-IN",
    autoplay: bool = False,
    selected_voice: str = "",
    speech_rate: float = 0.9,
    volume: float = 1.0,
    pitch: float = 1.0,
):
    """
    Browser-based Text-to-Speech.

    The browser's SpeechSynthesis API is used to detect
    and use voices available on the student's device.
    """

    if not text:
        return


    # ========================================================
    # ESCAPE TEXT
    # ========================================================

    escaped_text = (
        str(text)
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
    )


    # ========================================================
    # ESCAPE LANGUAGE
    # ========================================================

    escaped_language = (
        str(language)
        .replace("\\", "\\\\")
        .replace("'", "\\'")
    )


    # ========================================================
    # ESCAPE SELECTED VOICE
    # ========================================================

    escaped_voice = (
        str(selected_voice)
        .replace("\\", "\\\\")
        .replace("'", "\\'")
    )


    # ========================================================
    # AUTOPLAY
    # ========================================================

    autoplay_code = ""

    if autoplay:

        autoplay_code = """
        setTimeout(
            function() {
                speakText();
            },
            700
        );
        """


    # ========================================================
    # HTML COMPONENT
    # ========================================================

    component_html = """

    <div style="
        padding: 15px;
        border: 1px solid #cccccc;
        border-radius: 10px;
        margin-top: 12px;
        font-family: Arial, sans-serif;
    ">

        <strong>
            🔊 Read AI Answer
        </strong>

        <br><br>


        <!-- ================================================= -->
        <!-- VOICE SELECTOR -->
        <!-- ================================================= -->

        <label for="voiceSelect">
            🎙️ Available Voices
        </label>

        <br>

        <select
            id="voiceSelect"
            style="
                width: 100%;
                padding: 8px;
                margin-top: 6px;
                margin-bottom: 12px;
            "
        >

            <option value="">
                Loading voices...
            </option>

        </select>


        <!-- ================================================= -->
        <!-- PLAY BUTTON -->
        <!-- ================================================= -->

        <button
            onclick="speakText()"
            style="
                padding: 8px 16px;
                margin-right: 8px;
                cursor: pointer;
            "
        >
            ▶️ Play
        </button>


        <!-- ================================================= -->
        <!-- STOP BUTTON -->
        <!-- ================================================= -->

        <button
            onclick="stopSpeech()"
            style="
                padding: 8px 16px;
                cursor: pointer;
            "
        >
            ⏹️ Stop
        </button>


        <br><br>


        <!-- ================================================= -->
        <!-- STATUS -->
        <!-- ================================================= -->

        <small id="voiceStatus">
            Detecting available voices...
        </small>

    </div>


    <script>

    // ========================================================
    // TUTOR DATA
    // ========================================================

    const tutorText =
        `{escaped_text}`;

    const tutorLanguage =
        `{escaped_language}`;

    const previousVoice =
        `{escaped_voice}`;

    const tutorRate =
        {speech_rate};

    const tutorVolume =
        {volume};

    const tutorPitch =
        {pitch};


    // ========================================================
    // ELEMENTS
    // ========================================================

    const voiceSelect =
        document.getElementById(
            "voiceSelect"
        );


    const voiceStatus =
        document.getElementById(
            "voiceStatus"
        );


    // ========================================================
    // GET LANGUAGE PREFIX
    // ========================================================

    function getLanguagePrefix(language) {

        return language
            .split("-")[0]
            .toLowerCase();

    }


    const languagePrefix =
        getLanguagePrefix(
            tutorLanguage
        );


    // ========================================================
    // LOAD AVAILABLE VOICES
    // ========================================================

    function loadVoices() {

        const voices =
            window.speechSynthesis
                .getVoices();


        // ----------------------------------------------------
        // CLEAR SELECTOR
        // ----------------------------------------------------

        voiceSelect.innerHTML = "";


        // ----------------------------------------------------
        // DEFAULT VOICE
        // ----------------------------------------------------

        const defaultOption =
            document.createElement(
                "option"
            );


        defaultOption.value = "";


        defaultOption.textContent =
            "🔊 Default voice";


        voiceSelect.appendChild(
            defaultOption
        );


        // ----------------------------------------------------
        // SORT VOICES
        // ----------------------------------------------------

        const sortedVoices =
            voices.slice().sort(
                function(a, b) {

                    const aLanguage =
                        a.lang
                            .toLowerCase()
                            .startsWith(
                                languagePrefix
                            );

                    const bLanguage =
                        b.lang
                            .toLowerCase()
                            .startsWith(
                                languagePrefix
                            );


                    if (
                        aLanguage &&
                        !bLanguage
                    ) {

                        return -1;

                    }


                    if (
                        !aLanguage &&
                        bLanguage
                    ) {

                        return 1;

                    }


                    return a.name.localeCompare(
                        b.name
                    );

                }
            );


        // ----------------------------------------------------
        // ADD VOICES
        // ----------------------------------------------------

        sortedVoices.forEach(
            function(voice) {

                const option =
                    document.createElement(
                        "option"
                    );


                option.value =
                    voice.name;


                let label =
                    voice.name;


                if (voice.lang) {

                    label +=
                        " (" +
                        voice.lang +
                        ")";

                }


                // ------------------------------------------------
                // LANGUAGE MATCH
                // ------------------------------------------------

                if (
                    voice.lang
                        .toLowerCase()
                        .startsWith(
                            languagePrefix
                        )
                ) {

                    label +=
                        " ✓";

                }


                option.textContent =
                    label;


                // ------------------------------------------------
                // RESTORE PREVIOUS VOICE
                // ------------------------------------------------

                if (
                    previousVoice &&
                    voice.name ===
                    previousVoice
                ) {

                    option.selected =
                        true;

                }


                voiceSelect.appendChild(
                    option
                );

            }
        );


        // ----------------------------------------------------
        // STATUS
        // ----------------------------------------------------

        if (voices.length === 0) {

            voiceStatus.textContent =
                "No browser voices were detected.";

            return;

        }


        const matchingVoices =
            voices.filter(
                function(voice) {

                    return voice.lang
                        .toLowerCase()
                        .startsWith(
                            languagePrefix
                        );

                }
            );


        if (
            matchingVoices.length > 0
        ) {

            voiceStatus.textContent =
                voices.length +
                " voice(s) available. " +
                matchingVoices.length +
                " match the active language.";

        }
        else {

            voiceStatus.textContent =
                voices.length +
                " voice(s) available. " +
                "No exact language match was found.";

        }

    }


    // ========================================================
    // INITIAL LOAD
    // ========================================================

    loadVoices();


    // ========================================================
    // VOICES CHANGED
    // ========================================================

    if (
        "onvoiceschanged"
        in window.speechSynthesis
    ) {

        window.speechSynthesis
            .onvoiceschanged =
            loadVoices;

    }


    // ========================================================
    // SPEAK
    // ========================================================

    function speakText() {

        // ----------------------------------------------------
        // STOP CURRENT SPEECH
        // ----------------------------------------------------

        window.speechSynthesis.cancel();


        // ----------------------------------------------------
        // CREATE UTTERANCE
        // ----------------------------------------------------

        const utterance =
            new SpeechSynthesisUtterance(
                tutorText
            );


        // ----------------------------------------------------
        // LANGUAGE
        // ----------------------------------------------------

        utterance.lang =
            tutorLanguage;


        // ----------------------------------------------------
        // RATE
        // ----------------------------------------------------

        utterance.rate =
            tutorRate;


        // ----------------------------------------------------
        // VOLUME
        // ----------------------------------------------------

        utterance.volume =
            tutorVolume;


        // ----------------------------------------------------
        // PITCH
        // ----------------------------------------------------

        utterance.pitch =
            tutorPitch;


        // ----------------------------------------------------
        // FIND SELECTED VOICE
        // ----------------------------------------------------

        const voices =
            window.speechSynthesis
                .getVoices();


        const selectedVoice =
            voices.find(
                function(voice) {

                    return (
                        voice.name ===
                        voiceSelect.value
                    );

                }
            );


        // ----------------------------------------------------
        // APPLY SELECTED VOICE
        // ----------------------------------------------------

        if (selectedVoice) {

            utterance.voice =
                selectedVoice;

            utterance.lang =
                selectedVoice.lang;

        }


        // ----------------------------------------------------
        // SPEECH EVENTS
        // ----------------------------------------------------

        utterance.onstart =
            function() {

                voiceStatus.textContent =
                    "🔊 Speaking...";

            };


        utterance.onend =
            function() {

                voiceStatus.textContent =
                    "✅ Speech finished.";

            };


        utterance.onerror =
            function() {

                voiceStatus.textContent =
                    "⚠️ Unable to play this voice.";

            };


        // ----------------------------------------------------
        // SPEAK
        // ----------------------------------------------------

        window.speechSynthesis.speak(
            utterance
        );

    }


    // ========================================================
    // STOP SPEECH
    // ========================================================

    function stopSpeech() {

        window.speechSynthesis.cancel();


        voiceStatus.textContent =
            "⏹️ Speech stopped.";

    }


    // ========================================================
    // AUTOPLAY
    // ========================================================

    {autoplay_code}

    </script>

    """

    component_html = (
        component_html
        .replace("{escaped_text}", escaped_text)
        .replace("{escaped_language}", escaped_language)
        .replace("{escaped_voice}", escaped_voice)
        .replace("{speech_rate}", str(speech_rate))
        .replace("{volume}", str(volume))
        .replace("{pitch}", str(pitch))
        .replace("{autoplay_code}", autoplay_code)
    )


    # ========================================================
    # DISPLAY COMPONENT
    # ========================================================

    st.components.v1.html(

        component_html,

        height=250,

    )