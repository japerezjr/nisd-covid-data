#! /usr/bin/env python
import requests, sqlite3, re, json
from bs4 import BeautifulSoup

def getWeeklyReport(url, selector):
    # Download HTML from given url
    res = requests.get(url)
    # Raise an exception if we have a problem getting the page
    res.raise_for_status()
    # Create soup data and parse it as html
    soup = BeautifulSoup(res.text, 'html.parser')
    # Get the elements from the given CSS selector
    elems = soup.select(selector)
    # Strip empty spaces and replace unicode '\xa0' with a space
    report = elems[0].text.strip().replace(u'\xa0', ' ')
    # split the text by new line deliminator or by ': ' deliminator
    entries = re.split('\n|: ',report)
    # All that is left is an array with the text of the weekly reports
    return(entries,soup)

def getSchoolCases(soup, selector):
    school_cases = soup.select(selector)
    previous_text = ''
    school_stats = {}
    for elem in school_cases:
        current_text = elem.text
        if 'enrollment' in current_text.lower():
            school_name=previous_text
            school_stats[school_name] = {}
            try:
                school_stats[school_name]['Enrollment'] = int(current_text.split(":")[1].strip())
            except ValueError:
                school_stats[school_name]['Enrollment'] = 'Not Reported'
        elif 'cases' in current_text.lower():
            try:
                school_stats[school_name]['Cases'] = int(current_text.split(":")[1].strip())
            except ValueError:
                school_stats[school_name]['Cases'] = 'Not Reported'
        previous_text = current_text
    return(school_stats)

def lookfornumber(test_value):
    regex_number = re.compile(r"^(\d),(\d){3}|^(\d)$")
    if regex_number.search(test_value):
        return True
    else:
        return False

def main():
    url = 'https://www.nisd.net/schools/health'
    weekly_selector = 'body > div.dialog-off-canvas-main-canvas > div.main-container.container-fluid.js-quickedit-main-content > div.region.region-content > article > div > div.lr-padding.special-gutters.equal.spotlight-action-grid.pb-20.row.bs-3col > div.col-sm-6.bs-region.bs-region--left > section > div'
    thisWeeksReport,soup = getWeeklyReport(url, weekly_selector)
    selector=('div span')
    thisWeekSchoolStats = getSchoolCases(soup, selector)

    value = ''
    hdr = ''
    columns = []
    for entry in thisWeeksReport:
        if value != '':
            hdr = ''
        value = ''
        if re.search('covid-19 report', entry.lower()) is not None:
            continue
        elif entry.isnumeric() or re.search('na|n/a', entry.lower()) is not None or lookfornumber(entry):
            if entry.isnumeric():
                value = int(entry)
            else:
                value = entry
        elif re.search('2021|2022', entry):
            value = entry
            if re.search('[Aa]ctive', entry):
                temp = entry.split()
                hdr = ' '.join(temp[0:3])
                value = ' '.join(temp[3:])
        else:
            hdr = entry
        if value != '' and hdr != '':
            columns.append((hdr,value))
    print(columns)
    if len(thisWeekSchoolStats) > 0:
        print(json.dumps(thisWeekSchoolStats, indent=4, sort_keys=True))
    else:
        print('No stats for individual schools found!')

if __name__ == "__main__":
    main()
