#################################################
'''
ocho_indexer.py creates index.html for indexing all headers in all of the lecture
and exercise pages. This makes searching for information much faster.
'''
#################################################

import os


def get_lecture_list(dir_path):
    '''
    Create list of lectures/exercises from local folders
    '''

    LECTURE_LIST = next(os.walk(dir_path))[1]
    return LECTURE_LIST


def clean_headers_and_links(lecture, dir_path, headers, links):
    '''
    From list of lectures, open each html file and grab headers and anchors
    '''

    # open file
    lecture_file = dir_path + '/' + lecture + '/' + lecture + '.html'
    file = open(lecture_file, 'r')

    for line in file:
        line = line.strip('\n')
        line = line.strip(' ')
        if 'href="#' in line:
            header = line
            header = header.split('">')[1].split('</a>')[0]

            anchor_and_text = line
            anchor_and_text = anchor_and_text.split(
                'href="')[1].split('</a>')[0]

            top = dir_path.split('/')[1]
            link = f'<a href="{top}/{lecture}/{lecture}.html{anchor_and_text} > {lecture}</a>'

            # if the header isn't empty, check for duplicates
            if len(headers) > 0:
                headers_check = headers[-1].split('">')[1].split('</a>')[0]
                if headers_check != header:
                    # not a duplicate, append to header to headers
                    headers.append(line)
                    # add header and link to links
                    links[header] = link

            # append to headers since headers is empty
            else:
                headers.append(line)
                # add header and link to links
                links[header] = link

    return links


def create_html(links, sorted_headers, links_ex, sorted_headers_ex, contents_list=[], contents_list_ex=[]):
    '''
    Create index.html in local directory
    '''

    file = open('index.html', 'w')

    file.write('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Indexer</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
        <style>
            body {
                background-color: rgb(248, 248, 240);
            }

            a {
                color: black;
            }

            a:hover,
            a:active {
                color: gray;
                text-decoration: none;
            }

            .header {
                background-color: rgb(247, 122, 123);
                padding: 10px 10px;
                margin: 10px 10px;
                border-radius: 10px;
            }

            h1 {
                color: white;
            }

            ul li{
                color: rgb(247, 122, 123);
            }
        </style>
    </head>
    <body>
    
    <div class="container">
        <div class="row text-center">
            <div class="col header">
            <h1>Table of Contents</h1>
            </div>
        </div>
        <div class="row text-center">
            <div class="col-6 list-group">
                <h3>Lectures</h3>
                <ul class="text-left">''')

    for contents in contents_list:
        file.write(f'''
            <li><a href="lectures/{contents[2]}">
                <div class="row">
                    <div class="col text-left">
                        <b>{contents[1]}</b>
                    </div>
                    <div class="col text-left">
                        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                        {convert_date(contents[0])}
                    </div>
                </div>
            </a></li>
        ''')

    file.write('''
                </ul>
            </div>
            <div class="col-6 list-group">
                <h3>Exercises</h3>
                <ul class="text-left">''')

    for contents in contents_list_ex:
        file.write(f'''
            <li><a href="exercises/{contents[2]}">
                <div class="row">
                    <div class="col text-left">
                        <b>{contents[1]}</b>
                    </div>
                    <div class="col text-left">
                        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                        {convert_date(contents[0])}
                    </div>
                </div>
            </a></li>
        ''')

    file.write(''' 
                </ul>
            </div>
        </div>
        <div class="row text-center">
            <div class="col header">
                <h1>Index</h1>
            </div>
        </div>
        <div class="row text-center">
            <div class="col-6 list-group">
                <h3>Lectures</h3>
                <ul class="text-left">''')

    for header in sorted_headers:
        file.write(
            f'<li>{links[header]}</li>\n'
        )

    file.write('''
                </ul>
            </div>

            <div class="col-6 list-group">
                <h3>Exercises</h3>
                <ul class="text-left">''')

    for header in sorted_headers_ex:
        file.write(
            f'<li>{links_ex[header]}</li>\n'
        )

    file.write('''
                </ul>
            </div>
        </div>
    </div>
    </body>
    </html>
    ''')

    file.close()


def convert_date(date_string):
    '''
    Recieves a string of 8 numbers and converts to a better looking
    date string.
    '''

    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    return f'{months[int(date_string[0:2]) - 1]} {int(date_string[2:4])}, {date_string[4:]}'


def index(contents_list=[], contents_list_ex=[]):
    '''
    Runs the script on the lectures and exercises directories.
    '''

    headers = []
    links = {}

    headers_ex = []
    links_ex = {}

    LECTURE_LIST = get_lecture_list('./lectures')
    EXERCISE_LIST = get_lecture_list('./exercises')

    for lecture in LECTURE_LIST:
        links = clean_headers_and_links(
            lecture, './lectures', headers, links)

    for exercise in EXERCISE_LIST:
        links_ex = clean_headers_and_links(
            exercise, './exercises', headers_ex, links_ex)

    sorted_headers = sorted(links)
    sorted_headers_ex = sorted(links_ex)

    create_html(links, sorted_headers, links_ex,
                sorted_headers_ex, contents_list, contents_list_ex)
