Namespace EssayGenAI
====================

Sub-modules
-----------
* EssayGenAI.model
* EssayGenAI.util


Module EssayGenAI.util.generar_pdf
==================================

Functions
---------

`create_pdf(file_name, text, image_path)`
:

`extract_sections(text)`
:

Classes
-------

`PDF(orientation='P', unit='mm', format='A4')`
:   PDF Generation class

    ### Ancestors (in MRO)

    * fpdf.fpdf.FPDF

    ### Methods

    `chapter_body(self, body)`
    :

    `chapter_title(self, title)`
    :

    `footer(self)`
    :   Footer to be implemented in your own inherited class

    `header(self)`
    :   Header to be implemented in your own inherited class


Module EssayGenAI.model.app
===========================

Functions
---------

`download_file(file)`
:

`essay_gen(keywords)`
:

`generate_image(prompt)`
:

`generate_text(systemp, userp)`
:

`get_conclusion(text)`
:

`get_name_valid(title, max_length=30)`
:

`get_title_essay(text)`
:

`image_prompt(title, conclusion)`
:

`image_save(img_url, title)`
:


Module EssayGenAI.model.config
==============================

Classes
-------

`Config()`
:

    ### Static methods

    `get_all(filepath='model/config-model.json')`
    :   Carga y devuelve todos los valores del archivo config-model.json.
