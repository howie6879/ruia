import ruia

from lxml import etree

HTML = """
<body>
<div class="title" href="/">Ruia Documentation</div>
<ul>
    <li class="tag" href="./easy.html">easy</li>
    <li class="tag" href="./fast.html">fast</li>
    <li class="tag" href="./powerful.html">powerful</li>
</ul>
</body>
"""

html = etree.HTML(HTML)


def test_element_field():
    ul = ruia.ElementField(css_select="ul")
    assert len(ul.extract(html_etree=html).xpath('//li')) == 3


def test_text_field():
    title = ruia.TextField(css_select=".title", default="Untitled")
    assert title.extract(html_etree=html) == "Ruia Documentation"
    tags = ruia.TextField(css_select=".tag", default="No tag", many=True)
    assert tags.extract(html_etree=html) == ["easy", "fast", "powerful"]


def test_attr_field():
    title = ruia.AttrField(css_select=".title", attr="href", default="Untitled")
    assert title.extract(html_etree=html) == "/"
    tags = ruia.AttrField(css_select=".tag", attr="href", default="No tag", many=True)
    assert tags.extract(html_etree=html)[0] == "./easy.html"


def test_html_field():
    title = ruia.HtmlField(css_select=".title", default="Untitled")
    assert (
        title.extract(html_etree=html)
        == '<div class="title" href="/">Ruia Documentation</div>\n'
    )
    tags = ruia.HtmlField(css_select=".tag", default="No tag", many=True)
    assert (
        tags.extract(html_etree=html)[1]
        == '<li class="tag" href="./fast.html">fast</li>\n    '
    )


def test_regex_field():
    title = ruia.RegexField(re_select='<div class="title" href="(.*?)">(.*?)</div>')
    assert title.extract(html=HTML)[0] == "/"
    assert title.extract(html=HTML)[1] == "Ruia Documentation"
    tags = ruia.RegexField(
        re_select='<li class="tag" href="(?P<href>.*?)">(?P<text>.*?)</li>', many=True
    )
    result = tags.extract(html=HTML)
    assert isinstance(result, list)
    assert len(result) == 3
    assert isinstance(result[0], dict)
    assert result[0]["href"] == "./easy.html"
