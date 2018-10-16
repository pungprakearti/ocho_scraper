#################################################
'''
ocho_scraper.py checks a URL and grabs the files listed. If ran multiple times,
it grabs new files added to the directory without redownloading all the files again.

To download newer versions of individual files, just delete the folder you want to
redownload and run the script again.

The folders will be created where you run this script.

If you want to delete all content and redownload to get the newest files, use
the -a flag: python3 ocho_scaper.py -a

This script also creates an index.html which helps you find what you are looking
for in all of the course materials.

A log of operations can be found in this directory. It is called .ocho_log


DEPENDENCIES:

1. ocho_indexer.py
2. ocho_progress_bar.py


USE:

1. Run script:
    python3 ocho_scraper.py
2. PROFIT $$$$$:
    COHORT 8 FOREVER!
'''
#################################################

import urllib
from urllib import request
import os
import sys
import shutil
import math
import datetime
from ocho_indexer import index
import ocho_progress_bar


def find_and_keep(list_to_edit, key_to_find):
    '''
    This function looks through the html page and returns just the links
    '''

    temp_list = []
    for i in list_to_edit:
        if key_to_find in i and not ">../<" in i:
            temp_list.append(i)
    return temp_list


def split_and_append(list_to_edit, split_at, keep_index):
    '''
    Lots of work has to be done to the html to grab just the URL.
    This is used as a callback to help cut stuff out.
    keep_index is the index you want to keep after splitting the value.
    '''

    temp_list = []
    for i in list_to_edit:
        temp_list.append(i.split(split_at)[keep_index])
    return temp_list


def sanatize_input(response):
    '''
    This function groups all of the necessary steps to clean the links
    '''

    response_list = []
    response_list = response.split()
    response_list = find_and_keep(response_list, "</a>")
    response_list = split_and_append(response_list, '="', 1)
    response_list = split_and_append(response_list, '/"', 0)
    response_list = split_and_append(response_list, '">', 0)
    return response_list


def dl_and_search(url, local_path, filename):
    '''
    Download and search the html file for more links containing ".html"
    if other links are found, start another dl_and_search with new URL
    '''

    # grab the index page of URL
    try:
        request.urlretrieve(url + filename, filename=local_path + filename)
    except urllib.error.HTTPError:
        append_log(url + filename + " not found, skipping")
        return

    append_log('created ' + filename + ' from ' + url + filename)

    # open file
    file = open(local_path + filename, 'r')

    # iterate through lines of file
    for line in file:
        line = line.strip('\n')
        line = line.strip(' ')

        # find line with .html link and get new_filename
        if '.html">' in line:
            new_filename = line.split('href="')[1].split('">')[0]

            # run new dl_and_search
            dl_and_search(url, local_path, new_filename)

    file.close()


def check_and_create_files(URL, TOPDIR, response_list):
    '''
    This function creates the files and directories and skips over files in
    the list if you already have a folder for them. If you want to update that
    file, you can just delete that directory and rerun the script.
    '''

    progress_tick = 0

    for lecture in response_list:

        if(URL.split('/')[-2] == 'lectures'):
            progress_total = len(response_list)
            bar_name = '[LECTURES] SCRAPE PROGRESS'
        else:
            progress_total = len(response_list)
            bar_name = '[EXERCISES] SCRAPE PROGRESS'

        ocho_progress_bar.progress_bar(
            bar_name, bar, progress_total, progress_tick)

        # variables used for file paths
        html_dir = TOPDIR + "/" + lecture
        html_path = TOPDIR + "/" + lecture + "/" + lecture + ".html"
        static_url = URL + lecture + "/_static/"
        static_dir = TOPDIR + "/" + lecture + "/_static/"
        images_url = URL + lecture + "/_images/"
        images_dir = TOPDIR + "/" + lecture + "/_images/"
        zip_url = URL + lecture
        zip_dir = TOPDIR + "/" + lecture

        # If lectures folder doesn't exist, create it
        if not os.path.exists(TOPDIR):
            os.makedirs(TOPDIR)

        # HTML pages are created here
        if not ".zip" in lecture:

            if not os.path.exists(TOPDIR + "/" + lecture):

                # Make HTML directory
                append_log("\n" + html_dir + " doesn't exist.")
                lecture_dir = URL + lecture
                os.makedirs(html_dir)
                append_log("created " + html_dir)

                # Make HTML file
                request.urlretrieve(lecture_dir, filename=html_path)
                append_log("created " + html_path +
                           " from " + lecture_dir + ".html")

                # If working on exercises, create solution folder and grab all files
                if TOPDIR == 'exercises':
                    EX_TOPDIR = TOPDIR + "/" + lecture + "/solution"
                    DL_URL = lecture_dir + "/solution/"

                    os.makedirs(EX_TOPDIR)
                    append_log("created " + EX_TOPDIR)

                    dl_and_search(DL_URL, EX_TOPDIR, 'index.html')

                # Make static directory
                os.makedirs(static_dir)
                append_log("created " + static_dir)

                # Check to see if there are static items in the static directory.
                static = True

                try:
                    static_response = request.urlopen(static_url)
                except urllib.error.HTTPError:
                    append_log('There are no static files')
                    static = False

                # If there are images, create them
                if(static):
                    static_response = str(static_response.read())
                    static_response = sanatize_input(static_response)
                    for static in static_response:
                        request.urlretrieve(
                            static_url + static, filename=static_dir + static)
                        append_log("created " + static_dir +
                                   static + " from " + static_url + static)

                # Make images directory
                os.makedirs(images_dir)
                append_log("created " + images_dir)

                # Check to see if there are images in the image directory.
                images = True

                try:
                    images_response = request.urlopen(images_url)
                except urllib.error.HTTPError:
                    append_log('There are no images')
                    images = False

                # If there are images, create them
                if(images):
                    images_response = str(images_response.read())
                    images_response = sanatize_input(images_response)
                    for image in images_response:
                        request.urlretrieve(
                            images_url + image, filename=images_dir + image)
                        append_log("created " + images_dir + image +
                                   " from " + images_url + image)

            else:
                append_log("Skipping " + URL + lecture)

        else:
            # ZIP files are created here
            if not os.path.exists(zip_dir):
                append_log("\n" + zip_dir + " doesn't exist.")
                request.urlretrieve(zip_url, filename=zip_dir)
                append_log("created " + zip_dir + " from " + zip_url)

            else:
                append_log("Skipping " + URL + lecture)

        progress_tick += 1
        ocho_progress_bar.progress_bar(
            bar_name, bar, progress_total, progress_tick)


def get_toc_data(contents):
    '''
    Extract the data from the html response and return a list
    '''

    contents = contents.split()

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    contents_list = []
    i = 0
    for line in contents:
        if 'href=' in line and '>../<' not in line and '.zip' not in line:

            # date
            day = contents[i+1].split('-')[0]
            month = int(months.index(contents[i+1].split('-')[1])) + 1

            if len(str(month)) == 1:
                month = '0' + str(month)
            year = contents[i+1].split('-')[2]

            date = str(month) + str(day) + str(year)

            # header
            header = line.split('"')[1].split('"')[0].rstrip('/')

            # path
            path = link = line.split('"')[1].split('"')[0] + header + '.html'

            contents_list.append((date, header, path))

        i += 1

    contents_list.sort()

    return contents_list


def append_log(str='', start=False):
    '''
    Create a log of each operation and store in .ocho_log
    '''

    file = open(".ocho_log", 'a+')

    # if start is True, add the current date and time to the top of the entry
    if start == True:
        file.write('\n' + datetime.datetime.now().strftime('%B %d, %Y - %H:%M\n'))
        file.write('##################################################')

    file.write(str + '\n')
    file.close()


def scrape(URLS):
    '''
    This function starts the script with a list of urls. It iterates through the list and
    creates both folders and all of the elements inside of them. After that, it runs the
    indexer, which creates an index.html that helps you find what you are looking for in
    all of the course materials.
    '''

    # Check for -a flag:
    # -a removes all folders recursively that were previously created, and creates all
    # new files with a new scrape.

    # initial URLs check. If the URL errors, stop entire script.
    for URL in URLS:
        try:
            response = request.urlopen(URL)
        except urllib.error.HTTPError:
            print(
                f'{URL} is creating an HTTP Error.\nStopping operation.\n')
            return

    # start log
    append_log(start=True)

    # too many arguments given
    if len(sys.argv) > 2:
        print('ERROR: Incorrect number of arguments.')
        print(sys.argv[0])
        print('Scrape files and skip over existing folders.')
        print(f'{sys.argv[0]} -a')
        print('Remove folders and rescrape all files.')
        return

    elif len(sys.argv) == 2:

        # one argument, but it isn't "-a"
        if sys.argv[1] != "-a":
            print('ERROR: Incorrect input.')
            print(sys.argv[0])
            print('Scrape files and skip over existing folders.')
            print(f'{sys.argv[0]} -a')
            print('Remove folders and rescrape all files.')
            return

        # -a given, so remove all previous folders recursively and scrape
        elif sys.argv[1] == "-a":

            # check the URLs one more time to make sure they work before deleting
            for URL in URLS:
                try:
                    response = request.urlopen(URL)
                except urllib.error.HTTPError:
                    print(
                        f'{URL} is creating an HTTP Error.\nStopping operation.\nNO FILES DELETED! YA VELCOME.')
                    append_log(
                        f'{URL} is creating an HTTP Error.\nStopping operation.\nNO FILES DELETED! YA VELCOME.')
                    return

            for folder in URLS:
                folder = folder.split('/')[-2]
                if os.path.exists(folder):
                    shutil.rmtree(folder)
                    print(f'Removed {folder} folder')
                    append_log(f'Removed {folder} folder')

    TOPDIR = ''
    contents_list = []
    contents_list_ex = []

    # loop through URLs
    for URL in URLS:
        TOPDIR = URL.split('/')[4]
        response_list = request.urlopen(URL)
        response_list = str(response_list.read())

        # store contents of request for table of contents
        contents = response_list

        if not contents_list:
            contents_list = get_toc_data(contents)

        else:
            contents_list_ex = get_toc_data(contents)

        response_list = sanatize_input(response_list)

        check_and_create_files(URL, TOPDIR, response_list)

    # create index.html
    index(contents_list, contents_list_ex)
    print('\ncreated index.html\n\nAll up to date!')
    append_log('\ncreated index.html\n\nAll up to date!')


#################################################
# Start scraper

bar = ocho_progress_bar.create_bar()

URLS = ['URL1',
        'URL2']

scrape(URLS)
