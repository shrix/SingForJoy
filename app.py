import os
import singforjoy
import streamlit as st
# from streamlit_player import st_player

st.set_page_config(page_title="SingForJoy", page_icon="💎", layout="wide")

# Hide the menu.
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""

# Set the style to hide the default view.
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.session_state[
    "style_css"
] = """
    audio::-webkit-media-controls-panel,
    audio::-webkit-media-controls-enclosure {
        background-color:#202A44;
    }
    audio::-webkit-media-controls-time-remaining-display,
    audio::-webkit-media-controls-current-time-display {
        color: white;
        text-shadow: none; 
    }
    audio::-webkit-media-controls-play-button{
        background-image: url("data:image/png;base64,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");
    }
    audio::-webkit-media-controls-timeline {
        background-color: #314478;
        border-radius: 25px;
        margin-left: 10px;
        margin-right: 10px;
    }
    """

st.markdown(
    "<style>" + st.session_state["style_css"] + "</style>", unsafe_allow_html=True
)

def callback_function(state, key):
    st.session_state[state] = st.session_state[key]

if 'user_operation' not in st.session_state:
    st.session_state.user_operation = None

# Array positions of Songs in singforjoy
song_id     = 0
singer_name = 1
song_name   = 2
image_url   = 3
audio_url   = 4
video_url   = 5
song_genre  = 6

# Write stats into a file called "data" in the folder "stats" for persistency.
# The values are stored in a dictionary with keys and their respective values.
# The usage keys are:
#     "visits"
#     "audio_played"
#     "video_played"
# The play keys are ranging depending on the number of users:
#     "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", ... , "n"
#     where n is the number of users.
# Each user has a dictionary with keys and their respective values.
# The keys are:
#   "played"
#   "liked"
# The values are:
#   Incremental integers depending on number of times users played or liked a song.
#   The values are incremented by 1 each time the user plays or likes their song.

# total_songs = 0           # TODO: Total songs present.
# total_logins = 0          # TODO: Detect logins to increment this value.
# total_played = 0          # TODO: Aggregate the number of times all songs are played.
# most_played = 0           # TODO: Analyze song_played to find this.
# song_played = 0           # TODO: Detect when a specific song is played to increment this value.
# song_liked = 0            # TODO: Add a button to like a song, and detect this event to increment value.
# most_liked = 0            # TODO: Analyze song_liked to find this.

# TODO: list of pendings ...
# Zoom on current video being played, with a button to go back to the list of songs.
# Create a static frame on top to display info about the audio being played.

if 'user_name' not in st.session_state:
    col = st.columns([1, 3, 1])
    with col[1]:
        st.subheader("Your name :")
    with col[1]:
        st.text_input("Enter your name", label_visibility="collapsed", key="user_name_key", on_change=callback_function, args=('user_name','user_name_key'))

elif st.session_state.user_name:
    # Set the title and the introduction.
    st.title(f"{st.session_state.user_name.strip().title()}, welcome to DD's own SingForJoy 👋")
    # Keep a count of the number of times the page is visited.
    if 'visits' not in st.session_state:
        st.session_state.visits = 0
    st.session_state.visits += 1
    # Write the stats into the file stats/data.
    # TODO: Read the stats from the file stats/data.

    # Display the introduction.
    st.markdown("""
        ##### SingForJoy is a collection of songs that we all sing along, a few have been shared here.
        ##### You can listen to these songs, watch a few of them, and enjoy them all 🎉
        ####   
    """)

    index = 0
    song_indexes = []
    max_cols = 3

    # Display the genre selection box and the stats.
    st.write("")
    col = st.columns(3)
    with col[0]:
        st.markdown(f"##### Genre :")
        genre_selected = st.selectbox("Genre", 
            label_visibility="collapsed",
            options=(
                "All",
                "Instrumental",
                "Bollywood",
                "Tollywood",
                "Tamilwood",
                "Kollywood", 
                "Devotional",
                "Carnatic",
                "Western",
            )
        )
    with col[2]:
        st.markdown(f"""
            #####   
            #####   
            #####   
            ##### {len(singforjoy.Songs)} songs shared here, and enjoyed {st.session_state.visits} times 👏
        """, unsafe_allow_html=True)

        # TODO: Compute the total_views and total_logins.
        ##### Total played ------  {total_played}
        ##### Most  played ------  {most_played}
        ##### Total liked -------  {total_liked}
        ##### Most  liked -------  {most_liked}

    # Identify the songs based on genre selected.
    while index < len(singforjoy.Songs):
        if genre_selected == singforjoy.Songs[index][song_genre] or genre_selected == "All":
            song_indexes.append(index)
        index += 1
    
    # Check if any songs are found for the genre selected.
    if len(song_indexes) == 0:
        st.write(f"Sorry, no songs found for the genre '{genre_selected}'")
        st.stop()
    if len(song_indexes) < max_cols:
        max_cols = len(song_indexes)
    
    # Have multiple random images starting from the 2nd row onwards.
    for i in range( int(len(song_indexes)/max_cols) + 1 ):
        col = st.columns(max_cols)
        for j in range(max_cols):
            if i*max_cols+j < len(song_indexes):
                with col[j]:
                    st.divider()
                    if singforjoy.Songs[song_indexes[i*max_cols+j]][video_url] != None:
                        st.video(singforjoy.Songs[song_indexes[i*max_cols+j]][video_url])
                    else:
                        if singforjoy.Songs[song_indexes[i*max_cols+j]][image_url] != None:
                            st.image(singforjoy.Songs[song_indexes[i*max_cols+j]][image_url], use_column_width=True)
                        else:
                            st.image("https://picsum.photos/540/984", use_column_width=True)            # Random filler image
                    st.markdown(f"##### :blue[**{singforjoy.Songs[song_indexes[i*max_cols+j]][singer_name]}**] -:- :green[**_{singforjoy.Songs[song_indexes[i*max_cols+j]][song_name]}_**]")
                    st.audio(singforjoy.Songs[song_indexes[i*max_cols+j]][audio_url])
