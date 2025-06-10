from flask import Flask, request, send_file
from pydub import AudioSegment
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return "Audio Loop Backend is Running"

@app.route('/loop', methods=['POST'])
def loop_audio():
    if 'file' not in request.files:
        return {"error": "No file part"}, 400

    file = request.files['file']
    duration_minutes = int(request.form.get('duration', 10))

    audio = AudioSegment.from_file(file)
    target_duration_ms = duration_minutes * 60 * 1000
    looped_audio = AudioSegment.empty()

    while len(looped_audio) < target_duration_ms:
        looped_audio += audio

    looped_audio = looped_audio[:target_duration_ms]

    buffer = BytesIO()
    looped_audio.export(buffer, format="mp3")
    buffer.seek(0)

    return send_file(buffer, mimetype="audio/mpeg", as_attachment=True, download_name="looped_audio.mp3")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
