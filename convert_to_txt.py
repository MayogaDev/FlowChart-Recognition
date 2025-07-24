import json
import re

def replace_text(text):
    """Reemplaza los fragmentos de texto según las reglas especificadas."""
    replacements = {
        "INI": "INICIO",
        "ADELA": "ADELANTE",
        "DERE": "DERECHA",
        "QUI": "IZQUIERDA",
        "FIN": "FIN"
    }
    for key, value in replacements.items():
        if key in text:
            match = re.search(r'\b([1-9])\b', text)
            if match:
                return f"{value} {match.group(1)}"
            return value
    return text.strip()

def process_json(json_file, output_file):
    """Lee el archivo JSON, procesa los nodos y guarda los resultados en un archivo de texto."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        processed_lines = []
        for node in data["Node"]:
            name = node["Name"]
            processed_text = replace_text(name)
            processed_lines.append(processed_text)

        # Agregar "INICIO" al principio si el primer patrón no es "INICIO"
        if processed_lines and processed_lines[0] != "INICIO":
            processed_lines.insert(0, "INICIO")

        # Agregar "FIN" al final si el último patrón no es "FIN"
        if processed_lines and processed_lines[-1] != "FIN":
            processed_lines.append("FIN")

        with open(output_file, 'w', encoding='utf-8') as out_file:
            for line in processed_lines:
                out_file.write(line + "\n")

        print(f"Archivo {output_file} generado correctamente.")
    except Exception as e:
        print(f"Error procesando el archivo: {e}")

if __name__ == "__main__":
    json_file = 'data.json'
    output_file = 'resultado_diagrama.txt'
    process_json(json_file, output_file)
