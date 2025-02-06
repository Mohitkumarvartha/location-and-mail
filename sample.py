from flask import Flask, render_template
import smsandmap as s
app = Flask(__name__)

@app.route('/')
def home():
    # s.send_email("help")
    s.map()
    return "hello"

if __name__ == '__main__':
    app.run(debug=True)
