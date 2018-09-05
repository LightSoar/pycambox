#!env/bin/python

from flask import Flask, jsonify, abort
from werkzeug.routing import FloatConverter as BaseFloatConverter
import re
from stylebox import SVGStyleBoxBuilder, HTMLStyleBoxBuilder


class FloatConverter(BaseFloatConverter):
    # https://stackoverflow.com/a/20640550/3516684
    # https://www.regular-expressions.info/floatingpoint.html
    regex = r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'


app = Flask(__name__)
app.url_map.converters['float'] = FloatConverter

@app.route(('/<string:fmt>/<float:x>/<float:x_lo>/<float:x_hi>'
                         '/<float:y>/<float:y_lo>/<float:y_hi>'), methods=['GET'])
def general_explicit(fmt, x, x_lo, x_hi, y, y_lo, y_hi):
    if fmt.lower()=='svg':
        return SVGStyleBoxBuilder([x_lo, x_hi], [y_lo, y_hi], size=50, color="#000000").grid(2,2).point(x,y).build()
    elif fmt.lower()=='html':
        return HTMLStyleBoxBuilder([x_lo, x_hi], [y_lo, y_hi], size=50, color="#000000").grid(2,2).point(x,y).build()
    else:
        abort(400)

@app.route('/<float:x>/<float:y>', methods=['GET'])
def unit_square(x, y):
    return general_explicit('svg', x, 0, 1, y, 0, 1)

if __name__ == '__main__':
    app.run(debug=True)


