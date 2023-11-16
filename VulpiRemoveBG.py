from flask import Flask, abort, render_template, request, send_file, send_from_directory
from rembg import remove
from PIL import Image
import os
import threading

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__),'public', 'src'))

# Configurando o diretório de modelos
app.template_folder = os.path.join(os.path.dirname(__file__), 'public', 'templates')

@app.route('/')
def index():
    return render_template('index.html')

# Procesando e removendo a imagem
@app.route('/process', methods=['POST'])
def process_image():
    uploaded_file = request.files['image']

    if uploaded_file.filename != '':
        # Abrindo a imagem
        input_image = Image.open(uploaded_file)

        # Removendo o fundo da imagem
        output_image = remove(input_image)

        # Definindo o caminho de salvamento com o nome do arquivo imagem sem fundo
        output_image_path = os.path.join(os.path.dirname(__file__), 'public', 'src', 'img', (uploaded_file.filename + '_bg.png'))
        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)

        # Definindo o caminho de salvamento com o nome do arquivo imagem com fundo
        input_image_path = os.path.join(os.path.dirname(__file__), 'public', 'src', 'img', (uploaded_file.filename + '_or.png'))
        os.makedirs(os.path.dirname(input_image_path), exist_ok=True)

        # Salvando a imagem processada
        output_image.save(output_image_path)
        input_image.save(input_image_path)

        # retornando o resultado da imagem sem fundo
        return render_template('result.html', output_download_path='/download/'+(uploaded_file.filename + '_bg.png'), output_image_path='/images/'+(uploaded_file.filename + '_bg.png'), input_image_path='/images/'+(uploaded_file.filename + '_or.png'))

 # Rota para download da imagem   
@app.route('/download/<filename>')
def download_image(filename):
    file_path = os.path.join(os.path.dirname(__file__), 'public', 'src', 'img', filename)

    # Verifique se o arquivo existe
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        abort(404, "Arquivo não encontrado")

# Função para remover um arquivo
def remove_file(file_path):
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Imagem {file_path} removida.")
        except Exception as e:
            print(f"Erro ao remover arquivo {file_path}: {str(e)}")
    else:
        print(f"O arquivo {file_path} não existe, portanto não foi removido.")

# Rota para acessar a imagem
@app.route('/images/<filename>')
def serve_image(filename):
    file_path = os.path.join(os.path.dirname(__file__), 'public', 'src', 'img', filename)

    # Agende a função para remover o arquivo após 1 minutos
    threading.Timer(60, remove_file, args=[file_path]).start()

    return send_from_directory('public/src/img', filename)

@app.route('/svg/<filename>')
def serve_svg(filename):
    file_path = os.path.join(os.path.dirname(__file__), 'public', 'src', 'svg', filename)

    # Verifique se o arquivo existe
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        abort(404, "Arquivo não encontrado")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
