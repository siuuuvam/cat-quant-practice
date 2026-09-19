import json, re, os

with open(r'C:\Users\soova\AppData\Local\Temp\opencode\all_questions_final.json', 'r', encoding='utf-8') as f:
    all_q = json.load(f)

total = len(all_q)
topic_counts = {}
year_counts = {}
for q in all_q:
    topic_counts[q['topic']] = topic_counts.get(q['topic'], 0) + 1
    ym = re.search(r'CAT/(\d{4})', q['meta'])
    if ym:
        yr = ym.group(1)
        year_counts[yr] = year_counts.get(yr, 0) + 1

# Build JS question data
BS = chr(92)  # backslash
SQ = chr(39)  # single quote

js_items = []
for q in all_q:
    t = q['text'].replace('\n', ' ').replace('\r', '')
    # First unescape source text: \" -> " (these are literal quotes in the question)
    t = t.replace(BS + '"', '"')
    # Fix image URLs: dead domain + http -> https
    t = t.replace('http://cat.fundamakers.com', 'https://qna.fundamakers.com')
    t = t.replace('http://qna.fundamakers.com', 'https://qna.fundamakers.com')
    # Now escape for JS string output
    t = t.replace(BS, BS + BS).replace('"', BS + '"')
    opts = q.get('options_raw', 'null')
    if not opts or opts == 'null':
        opts = 'null'
    else:
        # Fix image URLs in options too
        opts = opts.replace('http://cat.fundamakers.com', 'https://qna.fundamakers.com')
        opts = opts.replace('http://qna.fundamakers.com', 'https://qna.fundamakers.com')
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

# Read the HTML template
template_path = r'C:\Users\soova\AppData\Local\Temp\opencode\template.html'
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# Replace placeholders
template = template.replace('TOTALQUESTIONS', str(total))
template = template.replace('TOPIC_PILLS_HTML', topic_pills_html)
template = template.replace('YEAR_PILLS_HTML', year_pills_html)
template = template.replace('JS_DATA_PLACEHOLDER', js_data)

out = r'C:\Users\soova\Desktop\CAT Quant Practice.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(template)
print('Done:', total, 'questions written to', out)
print('File size:', round(os.path.getsize(out) / 1024), 'KB')
