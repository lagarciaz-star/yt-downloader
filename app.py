from flask import Flask, request, render_template_string, send_file
import yt_dlp
import os
import tempfile

app = Flask(__name__)

HTML_FORM = """ ... """  # Tu HTML aquí

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")

        # Carpeta temporal
        temp_dir = tempfile.gettempdir()
        output_file = os.path.join(temp_dir, "%(title)s.%(ext)s")

        ydl_opts = {
            'format': 'best',
            'outtmpl': output_file,
            'noplaylist': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                nombre_archivo = ydl.prepare_filename(info)

            return send_file(nombre_archivo, as_attachment=True)
        except Exception as e:
            return f"? Error al descargar el video: {str(e)}"

    return render_template_string(HTML_FORM)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))