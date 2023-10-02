import streamlit as st
from modules import Uploader


def main():
    st.title("APP PART 2(data profiling, great expectations) (Part 2)")

    st.write("Upload a file for this session:")
    uploaded_file = Uploader.file_uploader()

    # More functionalities can be added as you specify further requirements.


if __name__ == "__main__":
    main()
