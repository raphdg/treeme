import os, sys

from optparse import OptionParser


def templatize(title, content):
    return """<!DOCTYPE html>
<html>
<head>
<title>{0}</title>
</head>
<body>
{1}
</body>
</html>
""".format(title, content)


def walkthrough(baseHREF, directory):
    icon = '<img src="/icons/folder.gif">'
    for folder, subfolders, files in os.walk(directory):
        root = folder[len(directory):]
        title = "Index of /%s" % root
        parent = '/'.join(root.split('/')[:-1]) or '/'
        content = '<ul>'
        content += '<li>' + icon + '<a href="%s">Parent</a></li>' % parent

        subfolders.sort()
        for sub in subfolders:
            link = os.path.join(baseHREF, root, sub)
            content += '<li>' + icon + '<a href="%s">%s</a></li>' % (link, sub)

        files.sort()
        for fn in files:
            if fn == "index.html":
                continue
            link = os.path.join(baseHREF, root, fn)
            content += '<li><a href="%s">%s</a></li>' % (link, fn)

        content += '</ul>'

        index_path = os.path.join(folder, "index.html")
        html = templatize(title, content)
        try:
            with open(index_path, 'wb') as fd:
                fd.write(html)
            print "Created %s" % index_path
        except IOError as err:
            print err

if __name__ == "__main__":
    usage = "usage: %prog [options] path"
    parser = OptionParser(usage=usage)
    parser.add_option("-H", "--baseHREF", dest="href",
                      default="/", help="Base location of HREF. Default to /")

    (options, args) = parser.parse_args()

    if not len(args):
        root = os.path.relpath('.')
    else:
        root = args[0]

    if not os.path.isdir(root):
        sys.exit("Error: The specified path is not a folder")

    prompt = "\nThis will create an index.html in every folder and " \
             "subfolder of %s \nContinue ? (y|N): " % os.path.abspath(root)
    ans = raw_input(prompt)
    if ans.lower() in ['y', 'yes']:
        walkthrough(options.href, root)
    else:
        exit()
