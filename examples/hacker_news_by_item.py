#!/usr/bin/env python
"""
 Created by howie.hu at 2018/7/10.
 Target: https://news.ycombinator.com/
"""
import asyncio

from pprint import pprint

from aspider import AttrField, TextField, Item


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self,value):
        return value

items = asyncio.get_event_loop().run_until_complete(HackerNewsItem.get_items(url="https://news.ycombinator.com/"))
pprint(items)

# Output
# [{'title': 'Show HN: Browsh – A modern, text-based browser',
#   'url': 'https://www.brow.sh'},
#  {'title': 'The Effects of CPU Turbo: 768X Stddev',
#   'url': 'https://www.alexgallego.org/perf/compiler/explorer/flatbuffers/smf/2018/06/30/effects-cpu-turbo.html'},
#  {'title': 'What industry has the highest revenue per employee?',
#   'url': 'https://craft.co/reports/where-do-the-most-productive-employees-work'},
#  {'title': 'The 111M Record Pemiblanc Credential Stuffing List',
#   'url': 'https://www.troyhunt.com/the-111-million-pemiblanc-credential-stuffing-list/'},
#  {'title': 'How to Analyze Billions of Records per Second on a Single Desktop '
#            'PC',
#   'url': 'https://clemenswinter.com/2018/07/09/how-to-analyze-billions-of-records-per-second-on-a-single-desktop-pc/'},
#  {'title': 'One in three fish caught never makes it to the plate – UN report',
#   'url': 'https://www.theguardian.com/environment/2018/jul/09/one-in-three-fish-caught-never-makes-it-to-the-plate-un-report'},
#  {'title': 'Historic Tale Construction Kit – Bayeux',
#   'url': 'http://htck.github.io/bayeux'},
#  {'title': 'The staggering rise of India’s super-rich',
#   'url': 'https://www.theguardian.com/news/2018/jul/10/the-staggering-rise-of-indias-super-rich'},
#  {'title': 'What do Stanford CS PhD students think of their PhD program? [pdf]',
#   'url': 'https://archive.org/download/phd_student_survey_summary_report_0a5c/phd_student_survey_summary_report_0a5c.pdf'},
#  {'title': 'A Short History of Prediction-Serving Systems',
#   'url': 'https://rise.cs.berkeley.edu/blog/a-short-history-of-prediction-serving-systems/'},
#  {'title': 'Heatwave unveils ancient settlements in Wales',
#   'url': 'https://www.bbc.co.uk/news/uk-wales-44746447'},
#  {'title': 'Half of ICOs Die Within Four Months After Token Sales Finalized',
#   'url': 'https://www.bloomberg.com/news/articles/2018-07-09/half-of-icos-die-within-four-months-after-token-sales-finalized'},
#  {'title': 'Tab (YC W15) is hiring full-stack software developers in London',
#   'url': 'https://jobs.tab.travel'},
#  {'title': 'Azure Storage: How fast are disks?',
#   'url': 'https://www.grsplus.com/blog/2018/07/azure-storage-how-fast-are-disks/'},
#  {'title': 'From shallow to deep learning in fraud',
#   'url': 'https://eng.lyft.com/from-shallow-to-deep-learning-in-fraud-9dafcbcef743'},
#  {'title': 'Research-backed strategies for better learning',
#   'url': 'https://stories.sagefy.org/eight-big-ideas-of-learning-tl-dr-edition-95302c848d87'},
#  {'title': 'CeramicSpeed’s Driven Concept Might Become the Most Efficient '
#            'Bicycle Drivetrain',
#   'url': 'https://www.bicycling.com/bikes-gear/a22092182/ceramicspeeds-driven-concept-might-become-the-worlds-most-efficient-drivetrain/'},
#  {'title': 'An Old Conjecture on Stream Transducers',
#   'url': 'https://www.pvk.ca/Blog/2018/06/24/an-old-conjecture-on-stream-transducers/'},
#  {'title': 'German court issues first GDPR ruling',
#   'url': 'https://www.natlawreview.com/article/german-court-issues-first-gdpr-ruling'},
#  {'title': 'The Children of Anaxagoras: Did hands make us human?',
#   'url': 'https://www.laphamsquarterly.org/roundtable/children-anaxagoras'},
#  {'title': 'Declassified videos of atmospheric nuclear tests (2017)',
#   'url': 'https://www.llnl.gov/news/llnl-releases-newly-declassified-test-videos'},
#  {'title': 'An app that reads Wikipedia to teach you about cities you’re '
#            'driving through',
#   'url': 'https://www.theverge.com/2018/7/9/17549668/app-wikipedia-location-facts'},
#  {'title': 'Why Does Your Company Deserve More Money?',
#   'url': 'https://blog.ycombinator.com/why-does-your-company-deserve-more-money/'},
#  {'title': 'Nissan Admits Internal Emissions-Test Results were Falsified',
#   'url': 'https://www.wsj.com/articles/nissan-admits-emission-test-data-was-falsified-1531139749'},
#  {'title': 'Reinforcement learning’s foundational flaw',
#   'url': 'https://thegradient.pub/why-rl-is-flawed/'},
#  {'title': 'Undershoot: Parsing theory in 1965',
#   'url': 'http://jeffreykegler.github.io/Ocean-of-Awareness-blog/individual/2018/07/knuth_1965_2.html'},
#  {'title': "Lay Out Your Code Like You'd Lay Out Your House",
#   'url': 'https://www.frederikcreemers.be/posts/code-layout/'},
#  {'title': "Monsanto 'bullied scientists' and hid weedkiller cancer risk, "
#            'lawyer tells court',
#   'url': 'https://www.theguardian.com/business/2018/jul/09/monsanto-trial-roundup-weedkiller-cancer-dewayne-johnson'},
#  {'title': 'Meet Your Mappers: A tool to find OpenStreetMap contributors near '
#            'you',
#   'url': 'https://ma.rtijn.org/2018/07/08/meet-your-mappers.html'},
#  {'title': 'CO2 shortage: Lessons learned from a storm in a pint glass?',
#   'url': 'https://www.gasworld.com/co2-shortage-lessons-learned/2015003.article'}]
