# La méta-boutique

This website is generated from data taken in [this twitter thread](https://twitter.com/garagedeloffre/status/1277912722638876672).

Note: It's a (single-)week-end project, where I did NOT code with cleanliness in mind, so don't judge my way of writing code based on this :) It's not horrible, but if I thought there was to be serious maintenance, I'd change a lot of things :)

### So how does it work:

- The site is static (it's generated dynamically, but once the HTML is generated, it's the same for everyone, not recomputed per-request).
- The front end uses [Bulma](https://bulma.io), organized from their very nice [starter kit](https://bulma.io/bulma-start/) and modified here and there.
- The "back end" is a pure Python script that uses jinja2 and requests for the twitter API
- In order to not do hundreds of API calls each time, and given most of the tweet data is immutable, a JSON file is kept, as a make-do-database

### The script does the following

- Load the JSON database in memory
- Call the twitter API to know if new tweets should be added
- Save it all in the database
- Write the database back
- Iterate on all tweets in the database
- Extract meaningful data from those tweets. In particular, save the images locally.
- Render the jinja template based on those pages

### CI

When running in the CI, GitHub actions will then add the new database & image files to git and push it back to master, and publish the generated site to github pages.

### Twitter API

A few words on "Call the twitter API to know if new tweets should be added".
Twitter does not support getting replies of a tweet. The only thing it supports is:
- Getting all the tweets linked to a thread from the last 7 days
- Getting the parent tweet of a tweet.

The algorithm will recursively add the parent of a tweet until there is no parent. For now it only considers tweets from the original thread author.
The initial DB was generated by providing a single tweet down the thread. As long as the CI runs more often than the 1 week API cutoff, all new tweets should be added here.

### Patches

Some data comes out wrong from the algorithm, and rather than writing the perfect algrotihm, it's easier to just fix the data, so that's what we do. There's a function that manually fixes the DB.

### Possible evolutions

- Add a JS-based sort (by +-date, by random, ...)
- Add tweets by other people when the original thread author has replied to them
- Handle quote-tweets better
