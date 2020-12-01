# bear-backlinks

Automated backlinks for [the Bear app](https://bear.app), in case you'd like those for a Zettelkasten-style notes library.

## TODO

- [x] Document installation & usage for this script
- [x] Figure out scheduling for the script (launchd job)
- [x] Figure out security/accessibility preferences required to run this script reliably, particularly from a background launchd job. (When running from iTerm, add iTerm to the list of apps allowed to use Accessibility.)
- [x] Fork [python-xcall](https://github.com/robwalton/python-xcall) & update it with my Python 3 version (see [xcall.py](https://github.com/cdzombak/bear-backlinks/blob/master/xcall.py))
- [ ] Fork [xcall](https://github.com/martinfinke/xcall) & build fat binaries, to ensure future Apple Silicon compatibility

## What it Does

In a Bear note, you will write the following to opt into automatic backlinking:

```
## Backlinks

*This space intentionally left blank.*

---
```

When this script runs, it looks for notes which contain the string `## Backlinks\n`. It'll search Bear for any notes that link to this set of notes; and it replaces everything between `## Backlinks` and `---` with a list of links. For example, it produced this output for one of my notes:

```
## Backlinks
- [[Anatomy of a Zettel]]
- [[Bear as Zettelkasten]]
- [[Zettelkasten Basics]]

---
```

This is useful for certain note-taking practices such as [Evergreen Notes](https://notes.andymatuschak.org/Evergreen_notes) and [Zettelkasten](https://zettelkasten.de), though there is [debate](https://zettelkasten.de/posts/backlinks-are-bad-links/) about its effectiveness.

A backup of each modified note is written to a timestamped backups directory as a Markdown file.

## Requirements / Compatibility

**Tested on macOS Mojave, on various Intel Macs.**

Should work on newer versions of macOS, except that changes to automation/privacy/Apple Events/security policies in newer macOS versions might make the automated interaction with Bear flakier, or make authorizing this program to use Accessibility more complex. (As it is, running this script via eg. iTerm requires iTerm to be allowed to use Accessibility automation).

I imagine this should run under Rosetta 2 on Apple Silicon, but this is untested. The main potential issue is that the checked-in copy of xcall is AFAIK not built for ARM.

**A working Python 3.x installation is required.**

Install it with eg. `brew install python`. See [Homebrew's docs on Python](https://docs.brew.sh/Homebrew-and-Python) for background information.

**Also, `brew install terminal-notifier` is required.**

## Installation

Simply `git clone https://github.com/cdzombak/bear-backlinks.git`. You can run the program from the checked-out repo.

### launchd job

Customize the included launchd plist file, adjusting:
- path to the `main.py` script
- working directory path
- your Bear app API token

Then:
```
cp com.dzombak.bear-backlinks.plist ~/Library/LaunchAgents
launchctl load -w com.dzombak.bear-backlinks
```

To start the job (ie. run the program), which you'll need to do at least once to allow automation permissions:
```
launchctl start com.dzombak.bear-backlinks
```

Editing & debugging this job is all easier with the excellent [LaunchControl application](https://www.soma-zone.com/LaunchControl/).

## Config

One configuration element is required, the Bear API token for Bear.app on the Mac you're running this program on. Get it from Bear's Help menu > API Token > Copy Token.

Supply it either in the env variable `CDZ_BEAR_API_TOKEN` or in a file `.bear-api-token` in the same directory as `main.py`.

To customize the backup directory, supply the environment variable `CDZ_BEAR_BACKUPS_DIR`.

## Usage

1. Ensure Bear is running and is not in any weird state (eg. it is not currently displaying a modal window).
1. Run `./main.py`.

## Troubleshooting

**Verbose logging:** enable by setting env var `CDZ_BEAR_VERBOSE` to `True`.

**If xcall hangs** returning x-callback-url values, it may be because you've (re)moved an instance of the xcall application somewhere on your filesystem. Fix this by opening the instance in this repo's `lib` folder, via Finder.

**Automation permission (as of macOS Mojave):** on first run, you'll see something like this in the output:

```
2020-12-01 08:40:37,901 DEBUG:updating content for note DEADBEEF-64
80:112: execution error: System Events got an error: osascript is not allowed to send keystrokes. (1002)
2020-12-01 08:40:40,496 INFO:completed successfully; updated 2 notes.
``` 

This should show up alongside a GUI dialog asking if you want to allow "main.py" to control System Events (or, if you're running from a terminal, it'll ask if your terminal app should be allowed to do so). Approve this request & re-run the program.

**launchd job returns 127:** `main.py` cannot be run. This probably is because `#!/usr/bin/env python3` is not finding a Python 3 binary. Adjust PATH for the launchd job to include `python3`. 

## About

- Issues: https://github.com/cdzombak/bear-backlinks/issues/new
- Author: [Chris Dzombak](https://www.dzombak.com)
