### Smoke

This is a small utility application I created to check whether specified Steam users own particular games. I did this due to a limitation in the tools available to me at a previous workplace.

> Smoke will not work unless you are in possession of a Steamworks Web API publisher authentication key pertinent for the game(s) you are checking users' ownership of.

The included `secrets.env` file includes placeholders for the publisher authentication key & the app ID. The latter can be obtained from the URL for the store page of your game. For example, looking at the URL https://store.steampowered.com/app/500/Left_4_Dead/ we can see Left 4 Dead's ID is 500.