"""
Changes delimiter of files from CSV to \x1f
Credit: Raymond
"""

import json, sys, io

def run(input_file, output_file, delimiter=u'\x1f'):
    j = json.load(open(input_file))
    
    top = j[j.keys()[0]]
    files = init(top, output_file, delimiter)
    
    for id in j.keys():
        build(j[id], files, id, delimiter)
    
def init(d, output_file, delimiter, tag=None):
    out = None
    ret = {}
    order = []
    for key in d.keys():
        order.append((key,type(d[key])))
        if type(d[key]) == dict:
            if tag == None:
                ret[key] = init(d[key], output_file, delimiter, '{0}'.format(key))
            else:
                ret[key] = init(d[key], output_file, delimiter, '{0}.{1}'.format(tag, key))
        else:
            if out == None:
                out = mk_outfile(output_file, tag)
                out.write(u'id')
            out.write(u'{0}{1}'.format(delimiter, key))
    if out != None:
        out.write(u'\n')
        ret['top'] = out
    ret['order'] = order
    return ret
    
def build(d, files, id, delimiter):
    if 'top' in files.keys():
        top = files['top']
        top.write(u'{0}'.format(id))
    for key,keytype in files['order']:
        try:
            if keytype == dict:
                build(d[key], files[key], id, delimiter)
            else:
                top.write(u'{0}{1}'.format(delimiter, repr(d[key])))
        except KeyError:
            if keytype != dict:
                top.write(u'{0}'.format(delimiter))
    if 'top' in files.keys():
        top.write(u'\n')
    
def mk_outfile(output_file, tag=None):
    if tag == None:
        s = '{0}.out'.format(output_file)
    else:
        s = '{0}.{1}.out'.format(output_file,tag)

    return io.open(s, 'w+', encoding='utf8')

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 4:
        run(args[1],args[2])
    else:
        print "Bad Input. Format is:"
        print "csv_convert [INPUT] [OUTPUT]"
