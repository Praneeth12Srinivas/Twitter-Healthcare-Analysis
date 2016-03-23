#!/bin/python

import json

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def getFieldsFromJSON(line,fields,collapse=False):
    srcObj = json.loads(line)
    obj = {}
    for field in fields:
        key = field
        if collapse:
            key = field.split('.')[-1]
        obj[key] = dive(srcObj,field)
    return obj
    
def dive(obj,field):
    f = field.split('.',1)
    if len(f) > 1:
        return dive(obj[f[0]],f[1])
    return obj[field]