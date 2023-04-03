#!/bin/bash
set -euxo pipefail

/Users/cdzombak/code/bear-backlinks/bear_backlinks.py
open "bear://x-callback-url/open-note?id=D12A6C48-0498-4675-9F57-7236F8C45BF4-474-00005B86341E9E69"
osascript -e 'tell application "System Events" to set visible of application process "Bear" to false'
