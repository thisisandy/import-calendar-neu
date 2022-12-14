import glob
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from icalendar import Calendar, Event


# refactor get_events() to get_events_from_file()
# and add a new get_events_from_folder() to get events from all html files
# in the current folder
def get_events_from_file(file):
    events = []
    with open(file, 'r') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        # get all the p tags inside body and extract the inner text
        paragraphs = [i.text.strip() for i in soup.body.find_all('p')[2:]]
        summary = ""
        dtstart = ""
        for p in paragraphs:
            # if the text is a valid date, then it's the date of the event
            if is_valid_date(p):
                # remove the heading and tailing space and •
                dtstart = p
            else:
                summary = p.replace('•', '')
                # if the summary is not empty, then we have a valid event
                if summary:
                    events.append({'summary': summary, 'dtstart': dtstart})
    return events


def get_events_from_folder(folder):
    # search the current folder for html files
    html_files = glob.glob('*.html')
    events = []
    for html_file in html_files:
        events.extend(get_events_from_file(html_file))
    return events


# write a fun to test if a string is a valid date like "Sep 7 2022 Wed "
def is_valid_date(date):
    try:
        datetime.strptime(date, '%b %d %Y %a')
        return True
    except ValueError:
        return False


def create_calendar(events):
    cal = Calendar()
    for event in events:
        e = Event()
        e.add('summary', event['summary'])
        # since the date is a string with the format like 'Jan 16 2023 Mon', we
        # need to convert it to a date object
        e.add('dtstart', datetime.strptime(event['dtstart'], '%b %d %Y %a').date())
        # add all day
        endDate = datetime.strptime(event['dtstart'], '%b %d %Y %a').date() + timedelta(days=1)
        e.add(
            'dtend', endDate
            )
        e.add('dtstamp', datetime.now())
        e.add('uid', event['summary'])
        cal.add_component(e)
    return cal


def main():
    events = get_events_from_folder('.')
    cal = create_calendar(events)
    with open('calendar.ics', 'wb') as ics_file:
        ics_file.write(cal.to_ical())


if __name__ == '__main__':
    main()
