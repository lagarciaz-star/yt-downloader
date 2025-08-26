from flask import Flask, request, render_template_string, send_file
import yt_dlp
import os

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Descargador de YouTube</title>
</head>
<body style="font-family: Arial; text-align: center; margin-top: 50px;">
    <h2>🎥 Descargador de YouTube</h2>
    <form method="POST">
        <input type="text" name="url" placeholder="Pega el enlace de YouTube" size="50" required>
        <br><br>
        <button type="submit">⬇ Descargar Video</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        output_file = "%(title)s.%(ext)s"

        ydl_opts = {
            'format': 'best',
            'outtmpl': output_file,
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            nombre_archivo = ydl.prepare_filename(info)

        return send_file(nombre_archivo, as_attachment=True)

    return render_template_string(HTML_FORM)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))