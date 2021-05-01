import picoweb

app = picoweb.WebApp(__name__)


@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    test = "Heisenberg"
    yield from app.render_template(resp, 'website.tpl', (test))

app.run(debug=True, host="192.168.1.50")
