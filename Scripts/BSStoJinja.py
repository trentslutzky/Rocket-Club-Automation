#! /bin/python3.9

import sys
#first command line arg should be the html file
html_file = sys.argv[1]

write_file = False

def main():
    linesUpdated = 0
    html_file_name = html_file.replace('.html','')
    r_beg = "{{ url_for('static', filename='" + html_file_name
    r_css = ".css') }}\""
    r_js = ".js') }}\""
    r_png = ".png') }}\""
    file_to_edit = open(html_file)
    lines = file_to_edit.readlines()
    new_lines = []
    for line in lines:
        if 'url_for' in line:
            print('this file has already been converted!')
            return
        if 'assets' in line:
            linesUpdated = linesUpdated + 1
            line_index = lines.index(line)
            line = line.replace('assets',r_beg)
            line = line.replace('.css"',r_css)
            line = line.replace('.js"',r_js)
            line = line.replace('.png"',r_png)
            write_file = True
        new_lines.append(line)
    file_to_edit.close()

    file_to_edit = open(html_file,'w')
    if write_file:
        for line in new_lines:
            file_to_edit.write(line)
    file_to_edit.close()
    print('Converted',linesUpdated,'lines!')

if __name__ == '__main__':
    main()
