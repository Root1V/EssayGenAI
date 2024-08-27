#!/bin/bash

# Limpiar el directorio de docs
rm -rf docs
mkdir -p docs

# Generar documentación Markdown usando pdoc
pdoc --output-dir docs .

# Crear o vaciar el archivo README.md
> README.md

# Encontrar el nombre de la subcarpeta del proyecto dentro de docs
project_subdir=$(find docs -mindepth 1 -maxdepth 1 -type d)

# Verificar si se encontró la subcarpeta del proyecto
if [ -d "$project_subdir" ]; then
    echo "Subcarpeta del proyecto encontrada: $project_subdir"

    # Añadir contenido de index.md a README.md
    index_md_path="$project_subdir/index.md"
    if [ -f "$index_md_path" ]; then
        echo "Añadiendo contenido de $index_md_path a README.md..."
        cat "$index_md_path" >> README.md
        echo -e "\n\n" >> README.md
    else
        echo "El archivo $index_md_path no se encontró."
    fi

    # Combinar archivos Markdown de la subcarpeta en README.md
    find "$project_subdir" -type f -name '*.md' ! -name 'index.md' | while read -r file; do
        echo "Añadiendo contenido de $file a README.md..."
        cat "$file" >> README.md
        echo -e "\n\n" >> README.md
    done

else
    echo "No se encontró la subcarpeta del proyecto en docs."
fi

echo "README.md ha sido generado con éxito."
