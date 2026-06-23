import streamlit as st
import tempfile
import matplotlib.pyplot as plt
import pandas as pd
import os

from matcher import identify_song
from visualization import get_visualization_data


st.set_page_config(
    page_title="Audio Fingerprinting",
    layout="wide"
)

st.markdown("""
<style>

.stApp{
    background-color:#11355E;
    color:pink;
}
/* Sidebar */
[data-testid="stSidebar"]{
    background-color:#101826;
}

/* Sidebar text */
[data-testid="stSidebar"] *{
    color:white;
}


.main-title{
    font-size:48px;
    font-weight:700;
    color:white;
}

.sub-title{
    color:#00E5FF;
    font-size:18px;
}

.result-card{
    background:linear-gradient(
        135deg,
        #113D4F,
        #112733
    );

    padding:30px;
    border-radius:20px;
    border:1px solid #00E5FF;
}
.stMetric {
    background-color: #101826;
    padding: 15px;
    border-radius: 15px;
    border: 1px solid rgba(0,229,255,0.25);
}

[data-testid="stMetricLabel"] {
    color: #00E5FF !important;
    font-size: 16px !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 32px !important;
    font-weight: bold !important;
}

.metric-card{
    background:#D42A7E;
    padding:15px;
    border-radius:15px;
    text-align:center;
    border:1px solid rgba(0,229,255,0.25);
}

</style>
""",
unsafe_allow_html=True)

st.markdown("""
<div class='main-title'>
🎵 Audio Fingerprinting
</div>

<div class='sub-title'>
Shazam-style Song Recognition using Peak Hashing
</div>
""",
unsafe_allow_html=True)

mode = st.sidebar.radio(
    "Mode",
    [
        "Single Clip",
        "Batch Mode"
    ]
)
if mode == "Single Clip":

    left,right = st.columns([3,1])
    with left:
        uploaded_file = st.file_uploader(
        "Upload Query Audio",
        type=["wav","mp3"]
    )
    with right:
        st.metric(
        "Database",
        "50 Songs"
    )
        st.metric(
        "Matcher",
        "Peak Hash"
    )

    identify = st.button(
        "🔍 Identify Song"
        )
    if uploaded_file is not None and identify:
        

        temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

        temp_file.write(
            uploaded_file.getvalue()
            )
        temp_file.close()

        temp_path = temp_file.name
        import os

        song, score, offsets, candidates = identify_song(
            temp_path
            )
        confidence = min(
            100,
            score/25
            )

        col1,col2,col3 = st.columns(3)
        col1.metric(
            "Match Score",
            score
            )
        col2.metric(
            "Confidence",
            f"{confidence:.1f}%"
            )
        col3.metric(
            "Offset Votes",
            len(offsets)
            )
        

        st.markdown(
            f"""
            <div class="result-card">
            <h4 style="color:#00E5FF;">
            MATCH FOUND
            </h4>
            <h1 style="color:white;">
            {song}
            </h1>
            <h3 style="color:#00E5FF;">
            Score : {score}
            </h3>
            </div>
            """,
            unsafe_allow_html=True
            )
        st.subheader(
            "Candidate Scores"
            )
        candidate_df = pd.DataFrame(
            candidates,
            columns=[
                "Song",
                "Score"
                ]
            )
        if len(candidates) > 1:
            winner = candidates[0][1]
            runner = candidates[1][1]
            ratio = winner / max(
                runner,
                1
                )
            st.metric(
                "Winner vs Runner-up",
                f"{ratio:.1f}x"
                )
        st.bar_chart(
            candidate_df.set_index(
                "Song"
                )
            )
        S_peak, freq_idx, time_idx = (
            get_visualization_data(
                temp_path
            )
        )
        st.subheader(
            "Match Statistics"
            )
        c1,c2,c3 = st.columns(3)
        c1.metric(
            "Query Peaks",
            len(freq_idx)
            )
        c2.metric(
            "Offset Votes",
            len(offsets)
            )
        c3.metric(
            "Top Score",
            score
            )        
        tab1, tab2, tab3 = st.tabs([
            "Spectrogram",
            "Constellation",
            "Alignment"
            ])
        with tab1:
            fig, ax = plt.subplots()
            ax.imshow(
            S_peak,
            aspect="auto",
            origin="lower"
        )
            ax.set_xlabel("Time")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)    
        with tab2:
            fig2, ax2 = plt.subplots()
            ax2.scatter(
            time_idx,
            freq_idx,
            s=5
        )
            ax2.set_xlabel(
            "Time Bin"
        )
            ax2.set_ylabel(
            "Frequency Bin"
        )
            st.pyplot(fig2) 
        
        with tab3:
            fig3, ax3 = plt.subplots()
            ax3.hist(
                offsets,
                bins=150
                )
            ax3.set_title(
                "Offset Alignment Peak"
                )
            ax3.set_xlabel(
            "Offset"
            )
            ax3.set_ylabel(
            "Count"
        )
            st.pyplot(fig3)
                   
        
if mode == "Batch Mode":

    uploaded_files = st.file_uploader(
        "Upload Query Clips",
        accept_multiple_files=True,
        type=["wav", "mp3"]
    )
    identify = st.button(
        "🔍 Identify Song"
        )

    if uploaded_files:

        results = []

        for file in uploaded_files:

            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".wav"
            )

            temp_file.write(
                file.read()
            )

            temp_path = temp_file.name

            song, score, offsets, candidates = identify_song(
                temp_path
                )

            prediction = os.path.splitext(
                song
            )[0]
            total_score = sum(
                s for _, s in candidates
                )
            confidence = (
                score /
                max(total_score,1)
                ) * 100
            if len(candidates) > 1:
                winner = candidates[0][1]
                runner = candidates[1][1]
                ratio = round(
                    winner / max(runner,1),
                    2
                    )
            else:
                ratio = "N/A"
            results.append(
                [
                    file.name,
                    prediction,
                    score,
                    round(confidence,2),
                    len(offsets),
                    ratio
                    ]
                )

        df = pd.DataFrame(
            results,
            columns=[
                "Filename",
                "Prediction",
                "Score",
                "Confidence %",
                "Offset Votes",
                "Winner Ratio"
            ]
        )

        st.dataframe(df)

        csv_data = df.to_csv(
            index=False
        )

        st.download_button(
            "Download results.csv",
            csv_data,
            file_name="results.csv",
            mime="text/csv"
        )        