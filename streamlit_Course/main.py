import streamlit as st
st.title('Streamlit Basics')
# st.header('Manga')
# st.subheader('One Piece')
# st.text('This is a text')
# st.write('This is a write')
# st.markdown("https://www.streamlit.io/")
# st.markdown("[Streamlit](https://www.streamlit.io/)")
# html_page="""
# <div style="background-color:blue;padding:50px">
# <p style="color:yellow;font-size:50px">Enjoy Streamlit</p>
# </div>
# """
# st.markdown(html_page,unsafe_allow_html=True)

# st.success('Successful')
# st.info('Information')
# st.warning('Warning')
# st.error('Error')

# from PIL import Image
# img=Image.open("Untitled design.png")
# st.image(img,width=300,caption="Streamlit Logo")
# video= open("video.mp4","rb")
# video_bytes=video.read()
# st.video(video_bytes)
# st.video('https://www.youtube.com/watch?v=bBaUDqkU4xs&ab_channel=GAKEIO')
# audio_file=open("Anri.mp3","rb")
# audio_bytes=audio_file.read()
# st.audio(audio_bytes,format='audio/mp3')
st.button("Simple Button")
if st.checkbox('Checkbox'):
    st.write('Checkbox is selected')

radio_but=st.radio("Radio Button",["Option 1","Option 2"])
st.info('Option 1 is selected' if radio_but=='Option 1' else 'Option 2 is selected')
city=st.selectbox("Select City",["New York","London","Tokyo"])
occupation=st.multiselect("Select Occupation",["Programmer","Data Scientist","Doctor","Engineer"])
Name=st.text_input("Enter Name",placeholder="Type Here...")
st.text("Name: "+Name)
Age=st.number_input("Enter Age",min_value=1,max_value=100)
message=st.text_area("Enter Message",placeholder="Type Here...")