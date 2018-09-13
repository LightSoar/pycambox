# pystylebox
A webservice for generating style boxes, inspired by the [Morningstar Style Box](https://www.investopedia.com/terms/s/stylebox.asp).

## In a script
### SVG
```python
from stylebox import SVGStyleBoxBuilder

svg_as_str = SVGStyleBoxBuilder([0, 1], [0, 1], size=50, color="#000000").grid(2,2).point(0.5,0.5).build()

with open("/tmp/stylebox.svg", "w") as svg_file:
    svg_file.write(svg_as_str)
```
#### Result
![pystylebox example](/examples/fifty-fifty.svg)

### ASCII
```python
from stylebox import ASCIIStyleBoxBuilder
print(ASCIIStyleBoxBuilder([0,1],[0,1], size=7).grid(1).point(0.25,0.75).build())
print(ASCIIStyleBoxBuilder([0,1],[0,1], size=7).grid(2).point(0.25,0.75).build())
print(ASCIIStyleBoxBuilder([0,1],[0,1], size=7).grid(5).point(0.25,0.75).build())
```
#### Result
```
┌──┬──┐
│  │  │
│  │  │
├──┼──┤
│ *│  │
│  │  │
└──┴──┘
┌─┬─┬─┐
│ │ │ │
├─┼─┼─┤
│ │ │ │
├─*─┼─┤
│ │ │ │
└─┴─┴─┘
┌┬┬┬┬┬┐
├┼┼┼┼┼┤
├┼┼┼┼┼┤
├┼┼┼┼┼┤
├┼*┼┼┼┤
├┼┼┼┼┼┤
└┴┴┴┴┴┘
```

## As a webservice
Run `./stylebox-webservice.py` and navigate to:
* http://127.0.0.1:5000/svg/0.5/0/1/0.5/0/1, for SVG output
* http://127.0.0.1:5000/html/0.5/0/1/0.5/0/1, for HTML output
* http://127.0.0.1:5000/ascii/0.5/0/1/0.5/0/1, for ASCII output


