from openai import OpenAI
from dotenv import load_dotenv
from .config import Config
import streamlit as st
from PIL import Image
import requests as req
from io import BytesIO
import re
import unicodedata
import os
import sys

# Agregamos la carpeta 'util'  en el sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "../util"))
from generar_pdf import create_pdf

# Cargar las variables de entorno
load_dotenv()

# Obtener todos los valores de configuración
config = Config.get_all()

# Client para interactuar con el modelo de OpenAI
client = OpenAI()


# Obtenemos el titulo del ensayo para usarlo como imput en el prompt de la imagen
def get_title_essay(text):
    title_match = re.search(r'\*\*Titulo:\*\*\s*"([^"]+)"', text)

    title = title_match.group(1).strip() if title_match else ""

    return title


# Obtenemos la conclusion del ensayo en apartado "Conclusión"
def get_conclusion(text):
    conclusion_match = re.search(r"\*\*Conclusión:\*\*\s*(.+)", text, re.DOTALL)

    if conclusion_match:
        # Devuelve solo el texto que está en la conclusión
        conclusion = conclusion_match.group(1).strip()
        conclusion = conclusion.split("\n")[-1].strip()

        return conclusion
    else:
        print("No se encontró una conclusión en el texto.")
        return ""


# Obtenemos un nombre valido para un archivo a partir del titulo del ensayo
def get_name_valid(title, max_length=30):
    # Quitar acentos y caracteres especiales
    title_norm = (
        unicodedata.normalize("NFKD", title).encode("ASCII", "ignore").decode("ASCII")
    )

    # Reemplazar espacios por guiones bajos
    title_empty = title_norm.replace(" ", "_")

    # Eliminar caracteres no permitidos en nombres de archivo (caracteres especiales)
    title_clean = re.sub(r"[^\w\-_]", "", title_empty)

    # Resumir el título a la longitud máxima permitida
    if len(title_clean) > max_length:
        title_clean = title_clean[:max_length]

    return title_clean


# generamos una imagen del ensayo:
def image_prompt(title, conclusion):
    image_prompt = f"""
        Create a photorealistic image inspired by the following title and conclusion from an essay:
        Title: '{title}'
        Conclusion: '{conclusion}'
        The image should reflect the themes and essence conveyed in the title and conclusion,
        translating their meaning into a visual representation that captures the core ideas of the essay.
        At the top of the image, include the title: '{title}'.
    """
    return image_prompt


# Generar texto con un LLM
def generate_text(systemp, userp):
    message = client.chat.completions.create(
        model=config["model"],
        max_tokens=config["max_tokens"],
        temperature=config["temperature"],
        messages=[
            {"role": "system", "content": systemp},
            {"role": "user", "content": userp},
        ],
    )
    return message.choices[0].message.content


# Generar texto con un LLM
def generate_image(prompt):
    response = client.images.generate(
        model=config["model_image"],
        prompt=prompt,
        style="vivid",
        size=config["size_image"],
        quality="standard",
        n=1,
    )

    return response.data[0].url


# Guardamos la imagen
def image_save(img_url, title):

    response = req.get(img_url)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    img_path = f"images/{get_name_valid(title)}.jpg"
    img.save(img_path, "JPEG")

    return img_path


# Descargamos la imagen
def download_file(file):
    with open(file, "rb") as f:
        file_contents = f.read()
    return file_contents


# Generamos el ensayo
def essay_gen(keywords):
    system_prompt = """
        Eres un escritor de renombre, con mucha eperiencia escribiendo ensayos de calidad.
        Tus ensayos reflejan la pasion por la tecnologia y la humanidad.
        Escribe el ensayo siguiendo exactamente el mismo formato que te brinda el usuario, no cambies nada del formato solo agregar los valores
    """

    user_prompt = f"""
        Crea un ensayo con las siguientes palabras clave: '{', '.join(keywords)}'.
        Ponle un titulo bastante innovador y que llame la atencion de los lectores.
        La estructura del ensayo debe de ser el siguiente:
        **Titulo:** "[value]"
        **Introducción:**
        **Cuerpo principal:**
        **Pasos a seguir:**
        **Reflexion final:**
        **Conclusión:**
    """
    print("\nPrompt Ensayo:", user_prompt)
    response_text = generate_text(system_prompt, user_prompt)
    print("\nEnsayo generado:", response_text)
    title = get_title_essay(response_text)
    conclusion = get_conclusion(response_text)

    print("\nTitulo:", title)
    print("\nConclusion:", conclusion)

    img_prompt = image_prompt(title, conclusion)
    print("\nImage_prompt:", img_prompt)

    img_url = generate_image(img_prompt)
    print("\nImage_URL:", img_url)

    img_path = image_save(img_url, title)
    print("\nImage_Path:", img_path)

    return {"title": title, "essay": response_text, "image": img_path}


def prueba_documentacion():
    print("prueba")


if __name__ == "__main__":
    st.title("Generador de Ensayos")
    st.write("Ingrese las palabras clave que tendra el ensayo:")
    user_input = st.text_input("Keywords (separado por comas)")

    if st.button("Generar Ensayo"):
        keywords = [kw.strip() for kw in user_input.split(",")]
        response = essay_gen(keywords)
        print("\nImprimimos el Essay:", response)
        st.session_state.essay = response["essay"]
        st.session_state.title = response["title"]
        st.session_state.image = response["image"]

    if "essay" in st.session_state:
        st.image(st.session_state.image, caption=st.session_state.title)
        st.write(st.session_state.essay)

        if st.button("Guardar ensayo en PDF"):
            pdf_file = create_pdf(
                get_name_valid(st.session_state.title),
                st.session_state.essay,
                st.session_state.image,
            )
            print("\nImprimimos la ruta del PDF:", pdf_file)
            st.download_button(
                label="Decargar en PDF",
                data=download_file(pdf_file),
                file_name=pdf_file,
                mime="application/pdf",
            )

# Sociedad, Inteligencia artificial, etica, evolución
