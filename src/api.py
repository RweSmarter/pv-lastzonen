#!/usr/bin/env python3
"""api.py — lokale JSON-API fuer die PoC-Module (Cleanroom-PoC, 21.10.2026).

Stdlib-only. Bindet NUR auf 127.0.0.1 (localhost, Dev-only).
Routen:
  GET /                      -> ui/index.html
  GET /api/zonen?bundesland=HE          -> geobasis.zonen_vorschlag
  GET /api/berechnen?schneezone=1&windzone=1&hoehe=180&neigung=25
       -> zonen.lastheftigkeit + formbeiwerte (mu1, dachlast)
ValueError aus den Modulen -> HTTP 400 mit JSON-Fehler.
"""
import json, pathlib, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import zonen, formbeiwerte, geobasis  # noqa: E402

UI_PATH = pathlib.Path(__file__).resolve().parent.parent / "ui" / "index.html"

class Handler(BaseHTTPRequestHandler):
    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        try:
            if u.path == "/":
                html = UI_PATH.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(html)))
                self.end_headers()
                self.wfile.write(html)
            elif u.path == "/api/zonen":
                self._json(200, geobasis.zonen_vorschlag(q["bundesland"][0]))
            elif u.path == "/api/berechnen":
                schnee = q.get("schneezone", ["1"])[0]
                wind = q.get("windzone", ["1"])[0]
                hoehe = float(q.get("hoehe", ["0"])[0])
                neigung = float(q.get("neigung", ["0"])[0])
                base = zonen.lastheftigkeit(schnee, wind, hoehe)
                mu1 = formbeiwerte.formbeiwert_schnee(neigung)
                base["mu1"] = round(mu1, 3)
                base["sk_dach_knm2"] = round(formbeiwerte.schneelast_dach(base["sk_knm2"], neigung), 3)
                base["stau_hinweis"] = formbeiwerte.hinweis_stau()
                self._json(200, base)
            else:
                self._json(404, {"fehler": "unbekannte Route", "pfad": u.path})
        except ValueError as exc:
            self._json(400, {"fehler": str(exc)})
        except Exception as exc:  # bewusst breit: API darf nie mit Traceback sterben
            self._json(500, {"fehler": f"interner Fehler: {exc}"})

    def log_message(self, fmt, *args):  # ruhig im Testbetrieb
        pass

def serve(port=8765):
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    return srv

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print(f"PoC-API auf http://127.0.0.1:{port} (Dev-only)", flush=True)
    serve(port).serve_forever()