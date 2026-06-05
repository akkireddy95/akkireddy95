---
title: GitHub Contribution Graph Legend
date: 2019-02-26 04:55:17
type: post
blog: true
excerpt: Ever wonder what it takes to achieve certain colors in the GitHub contribution graph? Here's a quick post on what I found.
tags:
commitLegend:
  - numberOfCommits: '0'
    color: '#ebedf0'
  - numberOfCommits: '1-6'
    color: '#c6e48b'
  - numberOfCommits: '7-13'
    color: '#7bc96f'
  - numberOfCommits: '14-19'
    color: '#239a3b'
  - numberOfCommits: '20+'
    color: '#196127'
---

On every GitHub user's profile page, there is a graph that is hard to ignore:

<blog-image alt="My GitHub contribution graph" src="/images/2019/2019-02-26-contribution-graph.png"></blog-image>

While there is controversy whether the graph is more harmful to developers ([see discussion thread](https://twitter.com/EmmaWedekind/status/1099235211555074048)), I have always been curious the amount of commits needed to generate a certain color within the graph. And while the internet is great for finding random information like this, I was unsuccessful at finding it.

So, thankfully my GitHub contribution graph has a fair amount of variance in the data to allow me to figure it out.

## Contribution Square Legend

- `0` commits: `#ebedf0`
- `1-6` commits: `#c6e48b`
- `7-13` commits: `#7bc96f`
- `14-19` commits: `#239a3b`
- `20+` commits: `#196127`

## Contributions Are Not Created Equal

In case you didn't notice, the legend I generated above is based on "commits" rather than other contribution tasks like Issue creation and PRs. After talking with [@TheAlexLichter](https://twitter.com/TheAlexLichter), it suddenly made me realize that all contributions are not counted equally. As far as I can tell, committing code to a repository has the highest weight when it comes to how it impacts your contribution graph.

## Final Thoughts

If it isn't obvious, I have been embarking to try and fill all of my squares for 2019. Is this gamification ultimately negative? Only time will tell. At the very least though, it has helped me to build a habit of working on something consistently rather than in one big swoop. I'll probably need a whole post dedicated to this, but that's for another time.

Till next time!
