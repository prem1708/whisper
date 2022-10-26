import streamlit as st

from utils import *

def main():
    # Streamlit config
    st.set_page_config(
        page_title="YouTube Video Transcription with Whisper",
        layout="centered",
    )

    # Title
    st.markdown("# YouTube Video Transcription with Whisper 🤫")

    # Intro text
    st.markdown(
        """
        This Streamlit app lets you transcribe YouTube videos using 
        [Whisper](https://github.com/openai/whisper), 
        a general-purpose speech recognition model developed by 
        [OpenAI](https://openai.com/).
        """
    )

    # Load Whisper model
    with st.spinner("Loading Whisper model..."):
        model =  load_whisper_model()


    # Title: Input data
    st.markdown("## Input data")

    # Input option
    input_option = st.selectbox("Input option:", options=["Choose an option...", "Sample URLs", "Custom URL"])

    # Sample URLs
    if input_option == "Sample URLs":
        sample_option = st.selectbox("Sample:", options=["Choose a sample..."] + list(SAMPLES.keys()))
        url = sample_to_url(sample_option)

    # Custom URL
    elif input_option == "Custom URL":
        url = st.text_input('YouTube URL:')

    else:
        url = None


    if url:
        # Check if the input url is a valid YouTube url
        right_url = valid_url(url)

        if right_url:
            if get_video_duration_from_youtube_url(url) <= MAX_VIDEO_LENGTH: 
                # Display YouTube video
                _,col2,_ =st.columns([0.35, 1, 0.35])
                col2.video(url)

                # Transcribe checkbox
                transcribe_cb = st.checkbox("Transcribe")

                if transcribe_cb:
                    st.info(
                        """
                        If the transcription process takes just a few seconds, this means that the output was cached.
                        You can try again with another sample or a custom YouTube URL!
                        """
                    )

                    st.markdown("## Output")
                    
                    # Transcribe
                    with st.spinner("Transcribing audio..."):
                        result = None
                        try:
                            result = transcribe_youtube_video(model, url)
                        except RuntimeError:
                            result = None
                            st.warning(
                                """
                                Oops! Someone else is using the model right now to transcribe another video. 
                                Please try again in a few seconds.
                                """
                            )

                    if result:
                        # Print detected language
                        st.success("Detected language: {}".format(result['language']))
                        
                        # Select output file extension and get data
                        file_extension = st.selectbox("File extension:", options=["TXT (.txt)", "SubRip (.srt)"])
                        if file_extension == "TXT (.txt)":
                            file_extension = "txt"
                            data = result['text'].strip()
                        elif file_extension == "SubRip (.srt)":
                            file_extension = "srt"
                            data = result['srt']

                        # Print output
                        data = st.text_area("Text:", value=data, height=350)

                        # Download data
                        st.download_button("Download", data=data, file_name="captions.{}".format(file_extension))
            else:
                st.warning("Sorry, the video has to be shorter than or equal to eight minutes.")
        else:
            st.warning("Invalid YouTube URL.")


if __name__ == "__main__":
    main()
