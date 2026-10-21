"""Print a JS snippet that seeds Studio's editor store with an experiment script as a new project.

Usage: python make_js.py SCRIPT "TITLE" COLLECTION START END W,S,E,N BAND [BAND ...] > snippet.js
"""
import json
import sys

script, title, collection, start, end, bbox, *bands = sys.argv[1:]
cfg = {"collectionId": collection, "temporalRange": [start, end], "cloudCover": 100, "selectedBands": bands, "boundingBox": [float(v) for v in bbox.split(",")]}
print("const code = " + json.dumps(open(script).read()) + ";")
print("const st = {state: {code, selectedConfig: " + json.dumps(cfg) + ", sceneId: null, sceneName: " + json.dumps(title) + ", isDirty: true}, version: 0};")
print("sessionStorage.setItem('openeo-editor-storage', JSON.stringify(st)); 'seeded ' + st.state.sceneName + ' ' + code.length")
