# generate_readme.py

import os
import subprocess
import shutil

def clean_docs_directory():
    """Elimina el directorio 'docs' si existe para evitar conflictos de archivos."""
    if os.path.exists('docs'):
        shutil.rmtree('docs')

def generate_markdown_documentation():
    """Genera documentación Markdown usando pdoc."""
    subprocess.run(['pdoc', '--output-dir', 'docs', '.'], check=True)


def combine_markdown_files(output_file, exclude_files):
    """Combina todos los archivos Markdown en el directorio 'docs' en un solo archivo README.md en la raíz, excluyendo archivos específicos."""
    with open(output_file, 'w') as outfile:
        for root, _, files in os.walk('docs'):
            for file in files:
                if file.endswith('.md') and file not in exclude_files:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as infile:
                        outfile.write(infile.read())
                        outfile.write('\n\n')  # Añadir separación entre archivos


def main():
    clean_docs_directory()
    generate_markdown_documentation()
    exclude_files = ['generate_readme.md']
    combine_markdown_files('README.md', exclude_files)

if __name__ == '__main__':
    main()
