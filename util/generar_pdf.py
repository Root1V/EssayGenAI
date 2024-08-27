from fpdf import FPDF
import re


class PDF(FPDF):
    def header(self):
        # El encabezado está vacío para la primera página
        pass

    def footer(self):
        # Agregar el pie de página solo a partir de la segunda página
        if self.page_no() > 1:
            self.set_y(
                -15
            )  # Posicionar el pie de página en la parte inferior de la página
            self.set_font("Helvetica", "I", 10)
            self.set_text_color(150, 150, 150)  # Color gris suave para marca de agua
            self.cell(0, 10, self.title, 0, 0, "C")  # Marca de agua en el pie de página
            self.set_x(10)  # Posicionar la línea horizontal
            self.set_line_width(0.5)
            self.line(10, self.get_y(), 200, self.get_y())

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 102, 204)  # Color azul
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(2)  # Espacio después del título

    def chapter_body(self, body):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(100, 100, 100)  # Color gris suave
        self.multi_cell(0, 7, body)  # Menor separación entre líneas
        self.ln(10)  # Espacio después del cuerpo


def extract_sections(text):
    # Expresión regular para encontrar secciones
    sections = {
        "title": re.search(r'\*\*Titulo:\*\*\s*"([^"]+)"', text),
        "introduction": re.search(
            r"\*\*Introducción:\*\*\s*(.*?)(?:\*\*|$)", text, re.DOTALL
        ),
        "body": re.search(
            r"\*\*Cuerpo principal:\*\*\s*(.*?)(?:\*\*|$)", text, re.DOTALL
        ),
        "steps": re.search(
            r"\*\*Pasos a seguir:\*\*\s*(.*?)(?:\*\*|$)", text, re.DOTALL
        ),
        "reflection": re.search(
            r"\*\*Reflexion final:\*\*\s*(.*?)(?:\*\*|$)", text, re.DOTALL
        ),
        "conclusion": re.search(r"\*\*Conclusión:\*\*\s*(.*)", text, re.DOTALL),
    }

    # Extraer el texto de cada sección si existe
    return {
        "title": sections["title"].group(1).strip() if sections["title"] else "",
        "introduction": (
            sections["introduction"].group(1).strip()
            if sections["introduction"]
            else ""
        ),
        "body": sections["body"].group(1).strip() if sections["body"] else "",
        "steps": sections["steps"].group(1).strip() if sections["steps"] else "",
        "reflection": (
            sections["reflection"].group(1).strip() if sections["reflection"] else ""
        ),
        "conclusion": (
            sections["conclusion"].group(1).strip() if sections["conclusion"] else ""
        ),
    }


def create_pdf(file_name, text, image_path):

    sections = extract_sections(text)

    pdf = PDF()
    pdf.title = sections["title"]

    # Agregar una página para el título
    pdf.add_page()

    # Agregamos una imagen
    img_width = 190
    pdf.image(image_path, x=(pdf.w - img_width) / 2, w=img_width, type="JPEG")

    # Ajustar posición para el título
    pdf.set_y(210)  # Ajusta la posición vertical del título después de la imagen

    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(0, 51, 102)
    pdf.multi_cell(0, 10, sections["title"])
    pdf.ln(10)

    # Agregar una nueva página para el contenido
    pdf.add_page()
    pdf.ln(10)

    # Agregar introducción
    pdf.chapter_title("Introducción")
    pdf.chapter_body(sections["introduction"])

    # Agregar cuerpo principal
    pdf.chapter_title("Cuerpo principal")
    pdf.chapter_body(sections["body"])

    # Agregar lista de pasos
    pdf.chapter_title("Pasos a seguir")
    pdf.chapter_body(sections["steps"])

    # Agregar reflexión final
    pdf.chapter_title("Reflexión final")
    pdf.chapter_body(sections["reflection"])

    # Agregar conclusión
    pdf.chapter_title("Conclusión")
    pdf.chapter_body(sections["conclusion"])

    # Guardar el PDF
    pdf_path = f"pdfs/{file_name}.pdf"
    pdf.output(pdf_path)

    print("\nPDF Generado:", pdf_path)

    return pdf_path
