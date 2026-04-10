from flask import Flask, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/transcript/<video_id>')
def get_transcript(video_id):
    try:
        api = YouTubeTranscriptApi()
        tl = api.list(video_id)
        try:
            transcript = tl.find_transcript(['ko', 'en'])
        except:
            transcript = tl.find_generated_transcript(['ko', 'en'])
        raw = transcript.fetch()
        segments = [
            {"text": i.text, "start": round(i.start, 3), "duration": round(i.duration, 3)}
            for i in raw
        ]
        return jsonify({"status": "ok", "transcript": segments})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("✅ Flask 서버 시작 (포트 5000)")
    app.run(host='0.0.0.0', port=5000)