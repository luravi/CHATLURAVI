import streamlit as st

def main():
    st.title('Chat con OpenAI')

    # Código para insertar el iframe
    iframe_code = """
    <iframe width="100%" height="600px" src="https://chat.openai.com/auth/login" frameborder="0" allowfullscreen scrolling="yes"></iframe>
    """
    st.markdown(iframe_code, unsafe_allow_html=True)

    # Información en la barra lateral
    st.sidebar.markdown("<h3 style='text-align: center; font-size: 20px; color: Red'>Por Melo Jr &reg - 2023</h3>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
