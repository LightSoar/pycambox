# pystylebox
A webservice for generating style boxes, inspired by the [Morningstar Style Box](https://www.investopedia.com/terms/s/stylebox.asp).

## Usage examples

```python
from stylebox import SVGStyleBoxBuilder

svg_as_str = SVGStyleBoxBuilder([0, 1], [0, 1], size=50, color="#000000").grid(2,2).point(0.5,0.5).build()

with open("/tmp/stylebox.svg", "w") as svg_file:
    svg_file.write(svg_as_str)
```

### Result
![pystylebox example](/examples/fifty-fifty.svg)
