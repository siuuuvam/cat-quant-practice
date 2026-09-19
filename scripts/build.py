import json, re, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# Load question data
data_path = os.path.join(PROJECT_DIR, 'data', 'questions.json')
with open(data_path, 'r', encoding='utf-8') as f:
    all_q = json.load(f)

# Load image URL -> local filename mapping
map_path = os.path.join(PROJECT_DIR, 'data', 'image_map.json')
with open(map_path, 'r') as f:
    url_map = json.load(f)

# Build reverse map: remote URL -> local relative path
def to_local_url(remote_url):
    # Normalize domain
    remote_url = remote_url.replace('http://cat.fundamakers.com', 'https://qna.fundamakers.com')
    remote_url = remote_url.replace('http://qna.fundamakers.com', 'https://qna.fundamakers.com')
    if remote_url in url_map:
        return 'images/' + url_map[remote_url]
    return remote_url  # fallback to original

total = len(all_q)
topic_counts = {}
year_counts = {}
for q in all_q:
    topic_counts[q['topic']] = topic_counts.get(q['topic'], 0) + 1
    ym = re.search(r'CAT/(\d{4})', q['meta'])
    if ym:
        yr = ym.group(1)
        year_counts[yr] = year_counts.get(yr, 0) + 1

BS = chr(92)

def replace_urls(text):
    """Replace all remote image URLs with local paths."""
    # Handle src='...' format
    def src_replacer(match):
        return "src='" + to_local_url(match.group(1)) + "'"
    text = re.sub(r"src='([^']+)'", src_replacer, text)
    # Handle [IMG:http://...] format
    def img_replacer(match):
        return "[IMG:" + to_local_url(match.group(1)) + "]"
    text = re.sub(r"\[IMG:(https?://[^\]]+)\]", img_replacer, text)
    # Also handle bare http:// URLs in options
    text = text.replace('http://cat.fundamakers.com', 'https://qna.fundamakers.com')
    text = text.replace('http://qna.fundamakers.com', 'https://qna.fundamakers.com')
    return text

js_items = []
for q in all_q:
    t = q['text'].replace('\n', ' ').replace('\r', '')
    t = t.replace(BS + '"', '"')
    # Replace remote URLs with local paths
    t = replace_urls(t)
    # Now escape for JS string output
    t = t.replace(BS, BS + BS).replace('"', BS + '"')

    opts = q.get('options_raw', 'null')
    if not opts or opts == 'null':
        opts = 'null'
    else:
        opts = replace_urls(opts)

    c = q['correct'].replace(BS, BS + BS).replace('"', BS + '"')
    topic = q['topic'].replace('"', BS + '"')
    ym = re.search(r'CAT/(\d{4})', q['meta'])
    year = ym.group(1) if ym else ''
    meta = q['meta'].replace('"', BS + '"')
    js_items.append(
        '{id:' + str(q['id']) +
        ',origId:' + str(q.get('orig_id', q['id'])) +
        ',meta:"' + meta +
        '",type:"' + q['type'] +
        '",topic:"' + topic +
        '",year:"' + year +
        '",text:"' + t +
        '",options:' + opts +
        ',correct:"' + c + '"}'
    )
js_data = ',\n'.join(js_items)

# Topic pills HTML
topic_pills_lines = []
topic_pills_lines.append('<button class="pill active" onclick="filterTopic(\'all\',this)">All (' + str(total) + ')</button>')
for tn in ['Algebra', 'Averages, Ratio & Proportion', 'Percentage, Profit & Loss', 'Time, Speed, Distance & Work']:
    cnt = topic_counts.get(tn, 0)
    label = tn.split(',')[0].split(' &')[0]
    topic_pills_lines.append('<button class="pill" onclick="filterTopic(\'' + tn.replace("'", "\\'") + '\',this)">' + label + ' (' + str(cnt) + ')</button>')
topic_pills_html = '\n        '.join(topic_pills_lines)

# Year pills HTML
year_pills_lines = []
sorted_years = sorted(year_counts.keys(), reverse=True)
for yr in sorted_years:
    cnt = year_counts[yr]
    year_pills_lines.append('<button class="pill" onclick="filterYear(\'' + yr + '\',this)">' + yr + ' (' + str(cnt) + ')</button>')
year_pills_html = '\n        '.join(year_pills_lines)

# Read template
template_path = os.path.join(SCRIPT_DIR, 'template.html')
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# Replace placeholders
template = template.replace('TOTALQUESTIONS', str(total))
template = template.replace('TOPIC_PILLS_HTML', topic_pills_html)
template = template.replace('YEAR_PILLS_HTML', year_pills_html)
template = template.replace('JS_DATA_PLACEHOLDER', js_data)

# Write output
out_path = os.path.join(PROJECT_DIR, 'index.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(template)

# Also update the JSON data with local URLs for reference
for q in all_q:
    q['text'] = replace_urls(q['text'].replace('\n', ' ').replace('\r', ''))
    opts = q.get('options_raw', '')
    if opts and opts != 'null':
        q['options_raw'] = replace_urls(opts)

with open(data_path, 'w', encoding='utf-8') as f:
    json.dump(all_q, f, indent=2, ensure_ascii=False)

print('Done:', total, 'questions written to', out_path)
print('File size:', round(os.path.getsize(out_path) / 1024), 'KB')
print('Local images:', len(url_map))
