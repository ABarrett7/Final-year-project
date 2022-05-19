import re
from bs4 import BeautifulSoup
import requests

# Calculates number of months
def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


# Generate data set by extracting the features from the URL
def generate_data_set(url):
    data_set = []

    # Converts the given URL into standard format
    if not re.match(r"^https?", url):
        url = "http://" + url

    # Stores the response of the given URL
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        response = ""
        soup = -999

    # Extracts domain from the given URL
    domain = re.findall(r"://([^/]+)/?", url)[0]
    if re.match(r"^www.", domain):
        domain = domain.replace("www.", "")

    # Requests all the information about the domain

    rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {
        "name": domain
    })

    # Extracts global rank of the website
    try:
        global_rank = int(re.findall(r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
    except:
        global_rank = -1

    # 1.URL_Length
    if len(url) < 50:
        data_set.append(1)
    elif len(url) >= 50 and len(url) <= 75:
        data_set.append(0)
    else:
        data_set.append(-1)

    # 2.Shortining_Service
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net',
                      url)
    if match:
        data_set.append(match)
    else:
        data_set.append(1)

    # 3.having_At_Symbol
    if re.findall("@", url):
        data_set.append(url)
    else:
        data_set.append(1)

    # 4.double_slash_redirecting
    list = [x.start(0) for x in re.finditer('//', url)]
    if list[len(list) - 1] > 6:
        data_set.append(list)
    else:
        data_set.append(1)

    # 5.Prefix_Suffix
    if re.findall(r"https?://[^\-]+-[^\-]+/", url):
        data_set.append(url)
    else:
        data_set.append(1)

    # 6.SSLfinal_State
    try:
        if response.text:
            data_set.append(1)
    except:
        data_set.append(-1)


    # 7. port
    try:
        port = domain.split(":")[1]
        if port:
            data_set.append(-1)
        else:
            data_set.append(1)
    except:
        data_set.append(1)

    # 8. HTTPS_token
    if re.findall(r"^https://", url):
        data_set.append(1)
    else:
        data_set.append(-1)

    # 9. Submitting_to_email
    if response == "":
        data_set.append(-1)
    else:
        if re.findall(r"[mail\(\)|mailto:?]", response.text):
            data_set.append(1)
        else:
            data_set.append(-1)

    # 10. Abnormal_URL
    if response == "":
        data_set.append(response)
    else:
        if response.text == "":
            data_set.append(1)
        else:
            data_set.append(response.text)

    # 11. Redirect
    if response == "":
        data_set.append(response)
    else:
        if len(response.history) <= 1:
            data_set.append(-1)
        elif len(response.history) <= 4:
            data_set.append(0)
        else:
            data_set.append(1)


    # 12. RightClick
    if response == "":
        data_set.append(-1)
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            data_set.append(1)
        else:
            data_set.append(-1)

    # 13. popUpWidnow
    if response == "":
        data_set.append(-1)
    else:
        if re.findall(r"alert\(", response.text):
            data_set.append(1)
        else:
            data_set.append(-1)

    # 14. Iframe
    if response == "":
        data_set.append(-1)
    else:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            data_set.append(1)
        else:
            data_set.append(-1)


    # 15. Page_Rank
    try:
        if global_rank > 0 and global_rank < 100000:
            data_set.append(-1)
        else:
            data_set.append(1)
    except:
        data_set.append(1)



    print(data_set)
    return data_set
