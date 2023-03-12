import json
import xml.etree.ElementTree as ET

def setPolarityOrCategory(label, ann):
    # polarity or category ?
    if (label == 'Positive') or (label == 'Negative') or (label == 'Neutral'):
        ann['polarity'] = label.lower()
    else:
        ann['category'] = label.lower()


def writeSemEvalXML(sentences):
    root = ET.Element('sentences')
    for s in sentences:
        sEl = ET.SubElement(root, 'sentence')
        sEl.attrib['id'] = str(s['id'])
        tEl = ET.SubElement(sEl, 'text')
        tEl.text = s['text']
        aspectTermsEl = ET.SubElement(sEl, 'aspectTerms')
        for a in s['annotations']:
            aTEl = ET.SubElement(aspectTermsEl, 'aspectTerm')
            aTEl.attrib['term'] = a['term']
            aTEl.attrib['polarity'] = a['polarity']
            aTEl.attrib['from'] = str(a['start'])
            aTEl.attrib['to'] = str(a['end'])
        aspectCategoriesEl = ET.SubElement(sEl, 'aspectCategories')
        for a in s['annotations']:
            aCEl = ET.SubElement(aspectCategoriesEl, 'aspectCategory')
            aCEl.attrib['category'] = a.get('category','unknowncategory')
            aCEl.attrib['polarity'] = a['polarity']
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    tree.write('output-semeval.xml', encoding="UTF-8", xml_declaration=True, short_empty_elements=False)
      


f = open('labelstudiodata.json',)
data = json.load(f)
f.close()


sentences = []
for i in data:
    s = {}
    s['id'] = i['id']
    s['text'] = i['data']['Sentences']
    s['annotations'] = []
    for a in i['annotations']:
        for r in a['result']:
            a2 = {}
            a2['start'] = r['value']['start']
            a2['end'] = r['value']['end']
            a2['term'] = r['value']['text']
        
            # ASSUME: there is only one element in r['value']['labels']
            label = r['value']['labels'][0]
            
            # look for an already introduced annotation for the same text
            sametextannfound = False
            for a3 in s['annotations']:
                if (a2['start'] == a3['start']) and (a2['end'] == a3['end']):
                    # found, set Polarity or Category, possibly overwriting them
                    setPolarityOrCategory(label, a3)
                    sametextannfound = True
            if not(sametextannfound): 
                setPolarityOrCategory(label, a2)
                s['annotations'].append(a2)            
    # print(s)
    sentences.append(s);

writeSemEvalXML(sentences)


""" 

<sentence id="813">
          <text>All the appetizers and salads were fabulous, the steak was mouth watering and the pasta was delicious!!!</text>
          <aspectTerms>
                    <aspectTerm term="appetizers" polarity="positive" from="8" to="18"/>
                    <aspectTerm term="salads" polarity="positive" from="23" to="29"/>
                    <aspectTerm term="steak" polarity="positive" from="49" to="54"/>
                    <aspectTerm term="pasta" polarity="positive" from="82" to="87"/>
          </aspectTerms>
          <aspectCategories>
                    <aspectCategory category="food" polarity="positive"/>
          </aspectCategories>
</sentence>

 """

