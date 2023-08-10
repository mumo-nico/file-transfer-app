from flask import Flask, render_template, request
import socket
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        source_ip = request.form['source_ip']
        target_ip = request.form['target_ip']
        port = int(request.form['port'])

        file = request.files['file']
        filename = file.filename
        file.save(filename)

        try:
            with open(filename, 'rb') as f:
                file_data = f.read()

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((target_ip, port))
                sock.sendall(file_data)

            os.remove(filename)
            message = "File transferred successfully!"
        except Exception as e:
            message = f"Error: {e}"

        return render_template('index.html', message=message)
    return render_template('index.html', message="")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
