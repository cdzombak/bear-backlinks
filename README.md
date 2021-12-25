# bear-backlinks

Automated backlinks for [the Bear app](https://bear.app), in case you'd like those for a Zettelkasten-style notes library.

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

A backup of each modified note is written as a Markdown file to a timestamped backups directory.

## Requirements / Compatibility

**Please read through the Troubleshooting section, below, thoroughly,** as getting this to work is especially challenging on Catalina/Big Sur.

Tested on **macOS Mojave and Big Sur, on Intel and Apple Silicon**.

**A working Python 3.x installation is required.** Install it with eg. `brew install python`. See [Homebrew's docs on Python](https://docs.brew.sh/Homebrew-and-Python) for background information.

**`brew install terminal-notifier`** is required.

## Installation

`git clone https://github.com/cdzombak/bear-backlinks.git`. You will run the program from the checked-out repo.

### Full Disk Access permissions

Under Catalina or Big Sur, the script needs to be run with Full Disk Access permission. If running the script via Terminal.app or iTerm.app, adding the terminal app to the Full Disk Access permissions list in System Preferences > Security & Privacy should be sufficient.

### Setting up the launchd job to run daily

Customize the included launchd plist file, adjusting:

- Path to the `bear_backlinks.py` script.
- Working directory path.
- Your Bear app API token, from Bear's Help menu.
- *For Catalina and Big Sur:* prefix the script with `/usr/local/bin/fdautil exec `. This requires [LaunchControl.app](https://www.soma-zone.com/LaunchControl/); read through the Troubleshooting section for details.

Then:
```
cp com.dzombak.bear-backlinks.plist ~/Library/LaunchAgents
launchctl load -w ~/Library/LaunchAgents/com.dzombak.bear-backlinks.plist
```

To start the job (ie. run the program), which you'll need to do at least once to allow automation permissions:
```
launchctl start com.dzombak.bear-backlinks
```

ℹ️ Editing & debugging this job is much easier with the excellent [LaunchControl application](https://www.soma-zone.com/LaunchControl/).

Unfortunately, I have not figured out how to give the `bear_backlinks.py` Python script full disk access directly, to allow running it via launchd. So, **running with launchd on Big Sur or Catalina requires [LaunchControl.app](https://www.soma-zone.com/LaunchControl), which comes with a helper program called [`fdautil`](https://www.soma-zone.com/LaunchControl/FAQ.html)**. Read through Troubleshooting, below, for discussion.

## Configuration

One configuration element is required, the Bear API token for Bear.app on the Mac you're running this program on. Get it from Bear's Help menu > API Token > Copy Token.

Supply it either in the environment variable `CDZ_BEAR_API_TOKEN` or in a file `.bear-api-token` in the same directory as `bear_backlinks.py`.

To customize the backup directory, supply the environment variable `CDZ_BEAR_BACKUPS_DIR`.

## Usage

1. Ensure Bear is running and is not in any weird state (eg. it is not currently displaying a modal window).
1. Run `./bear_backlinks.py`.

## Troubleshooting

**launchd job returns 127:** `bear_backlinks.py` cannot be run. This probably is because `#!/usr/bin/env python3` is not finding a Python 3 binary. Adjust PATH for the launchd job to include `python3`.

**Verbose logging:** enable by setting the environment variable `CDZ_BEAR_VERBOSE` to `True`. This is a good first step in debugging any issues.

**If `xcall` hangs** returning `x-callback-url` values, it may be because you've (re)moved an instance of the xcall application somewhere else on your filesystem. Fix this by opening the instance in this repo's `lib` folder, via Finder.

*Alternatively, if the program hangs waiting on `xcall`:* I experienced `xcall` hanging when running [commit `95aa09d8`](https://github.com/cdzombak/bear-backlinks/commit/95aa09d8ac05aa64edd8421193aa32631a78bcee) of bear-backlinks on a new Apple Silicon M1 Mac, running Big Sur. I [rebuilt xcall](https://github.com/cdzombak/xcall) as a universal binary, which is now included in this repo. If this situation applies to you: try updating your checkout of this repository, opening `lib/xcall.app` via Finder, and running `bear_backlinks.py` again.

**Crash when trying to write note backup (on macOS Catalina/Big Sur):** if you get something like this in your standard error output:

```
  File "/Users/cdzombak/code/bear-backlinks/bear_backlinks.py", line 97, in <module>
    main()
  File "/Users/cdzombak/code/bear-backlinks/bear_backlinks.py", line 76, in main
    os.mkdir(backup_dir)
PermissionError: [Errno 1] Operation not permitted: '/Volumes/curie-ext/Backup/bear-backlinks/2021-05-13T15-55-11'
```

The script needs to be run with Full Disk Access permission. If running the script via Terminal.app or iTerm.app, adding the terminal app to the Full Disk Access permissions list in System Preferences > Security & Privacy should be sufficient.

Unfortunately, I have not figured out how to give the `bear_backlinks.py` Python script full disk access directly, to allow running it via launchd. So, **running with launchd on Big Sur or Catalina requires [LaunchControl.app](https://www.soma-zone.com/LaunchControl), which comes with a helper program called [`fdautil`](https://www.soma-zone.com/LaunchControl/FAQ.html)**.

Install LaunchControl, open the `com.dzombak.bear-backlinks` job, and modify the "Program to run" to `/usr/local/bin/fdautil exec /Users/me/path/to/bear-backlinks/bear_backlinks.py` (changing the path as needed). Finally, you'll need to install fdautil from LaunchControl's Preferences > Utilities window.

## About

- Issues: https://github.com/cdzombak/bear-backlinks/issues/new
- Author: [Chris Dzombak](https://www.dzombak.com)
