from lxml import html
import requests

URL = 'https://portswigger.net/web-security/all-labs'
#XPATH = "//*[contains(concat(' ', normalize-space(@class), ' '), ' widgetcontainer-lab-link ')]/div/span[{}]/following-sibling::a";
#TARGETS = ['APPRENTICE', 'PRACTITIONER'] #, 'EXPERT']

LABS_XPATH = "//*[contains(concat(' ', normalize-space(@class), ' '), ' widgetcontainer-lab-link ')]/div/span[text()='APPRENTICE' or text()='PRACTITIONER']/following-sibling::a";
SOLUTION_XPATH = "//*[contains(concat(' ', normalize-space(@class), ' '), ' component-solution ')][1]/div"

print("Fetching labs page...")
page = requests.get(URL)
print("Parsing HTML...")
tree = html.fromstring(page.content)

print("Pathing all labs...")
labs = tree.xpath(LABS_XPATH)
no_labs = len(labs)

storage = []

for idx, lab in enumerate(labs):
    title = lab.text
    url = 'https://portswigger.net' + lab.attrib['href']

    print(f'Fetching {idx+1} out of {no_labs}: {title}')
    page = requests.get(url)
    tree = html.fromstring(page.content)
    solution = html.tostring(tree.xpath(SOLUTION_XPATH)[0])

    storage.append([title, solution])

print('\n\nWriting...')
with open('solutions.md', 'w') as f:
    f.write('# Portswigger Academy Solutions\n\n')

    for i in storage:
        f.write(f'### {i[0]}\n' + i[1].decode('utf-8') + '\n')
 
