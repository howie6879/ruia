#!/usr/bin/env python
"""
 Created by howie.hu at 2018/7/10.
 Target: https://news.ycombinator.com/
"""
import asyncio

from aspider import AttrField, TextField, Item


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        return value


items = asyncio.get_event_loop().run_until_complete(HackerNewsItem.get_items(url="https://news.ycombinator.com/"))
for item in items:
    print(item.title, item.url)

# Output
# Notorious ‘Hijack Factory’ Shunned from Web https://krebsonsecurity.com/2018/07/notorious-hijack-factory-shunned-from-web/
# Unix system programming in OCaml (2014) https://ocaml.github.io/ocamlunix/index.html
# Red Flags Signaling That a Rebuild Will Fail http://www.pkc.io/blog/five-red-flags-signaling-your-rebuild-will-fail/
# A biologist who believes that trees speak a language we can learn to listen to https://qz.com/1116991/a-biologist-believes-that-trees-speak-a-language-we-can-learn/
# Ask HN: As a team lead how to handle project going off the rails? item?id=17511850
# Bulletproofs – Short zero-knowledge arguments of knowledge https://github.com/adjoint-io/bulletproofs
# Neatly bypassing CSP https://lab.wallarm.com/how-to-trick-csp-in-letting-you-run-whatever-you-want-73cb5ff428aa
# A Clone of the Classic Mac OS Finder in Modern Cocoa and Objective-C https://bszyman.com/blog/classic-finder
# Show HN: Solving Rush Hour, the 6x6 Sliding Block Puzzle https://www.michaelfogleman.com/rush/
# To Explain or to Predict? (2010) [pdf] http://www.galitshmueli.com/system/files/Stat%20Science%20published.pdf
# Using Apple’s New Controls to Limit a Teenager’s iPhone Time https://www.nytimes.com/2018/07/11/technology/personaltech/apple-iphone-screen-time.html
# Hospitalism: On 'The Butchering Art' https://www.lrb.co.uk/v40/n13/sarah-perry/hospitalism
# Internally, NASA believes Boeing ahead of SpaceX in commercial crew https://arstechnica.com/science/2018/07/nasa-commercial-crew-analysis-finds-boeing-slightly-ahead-of-spacex/
# Battling Fake Accounts, Twitter to Slash Millions of Followers https://www.nytimes.com/2018/07/11/technology/twitter-fake-followers.html
# Loon and Wing graduate from Google/Alphabet X https://www.wired.com/story/alphabet-google-x-innovation-loon-wing-graduation/
# Logic programming courses https://edu.swi-prolog.org/
# At Initialized Capital, Odd Couple Looks to Do VC Differently https://www.forbes.com/sites/alexkonrad/2018/07/09/at-initialized-capital-odd-couple-alexis-ohanian-and-garry-tan-look-to-do-vc-differently/#456e13c43efe
# How ProPublica Illinois Uses GNU Make to Load Data https://www.propublica.org/nerds/gnu-make-illinois-campaign-finance-data-david-eads-propublica-illinois#146596
# The San Franciso Fire Department makes its own wooden ladders by hand https://gizmodo.com/inside-san-francisos-fire-department-where-ladders-are-1552279252
# Inside the Paper: Build Systems a La Carte https://neilmitchell.blogspot.com/2018/07/inside-paper-build-systems-la-carte.html
# FCC Proposes Changing Comment System After WSJ Found Thousands of Fakes https://www.wsj.com/articles/fcc-proposes-rebuilding-comment-system-after-thousands-revealed-as-fake-1531315654
# How Inlined Code Makes for Confusing Profiles http://psy-lob-saw.blogspot.com/2018/07/how-inlined-code-confusing-profiles.html
# At Play: A Personal Odyssey in Chess https://www.metapsychosis.com/at-play-personal-odyssey-chess/
# Why local US newspapers are sounding the alarm https://www.bbc.com/news/world-us-canada-44688274
# The rescue of the crew of the yacht Django (2016) https://boatingnz.co.nz/articles/deep-impact/
# A browser extension to make Medium more readable https://makemediumreadable.com/
# Comparing City Street Orientations http://geoffboeing.com/2018/07/comparing-city-street-orientations/
# The Entire History of Steel https://www.popularmechanics.com/technology/infrastructure/a20722505/history-of-steel/
# The libkern C++ Runtime https://developer.apple.com/library/archive/documentation/DeviceDrivers/Conceptual/WritingDeviceDriver/CPluPlusRuntime/CPlusPlusRuntime.html
# Solar Just Hit a Record Low Price in the U.S https://earther.com/solar-just-hit-a-record-low-price-in-the-u-s-1826830592
