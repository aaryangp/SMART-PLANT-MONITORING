from flask import Flask, render_template_string, Response
import cv2

app = Flask(__name__)

# HTML template for video stream
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Plant Camera Stream</title>
</head>
<body>
    <h1 style="text-align:center;">Live Plant Stream</h1>
    <div style="text-align:center;">
        <img src="{{ url_for('video_feed') }}" width="640" height="480">
    </div>
</body>
</html>
"""

camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
