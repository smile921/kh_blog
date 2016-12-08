# greybeard devtools

![greybeard devtools screenshot](https://raw.githubusercontent.com/xero/greybeard-devtools/master/preview1.png)
![greybeard devtools screenshot](https://raw.githubusercontent.com/xero/greybeard-devtools/master/preview2.png)

greybeard is a fork of [SO-Dark-Monokai-v3](https://github.com/s10wen/SO-Dark-Monokai-v3) chrome developer tools theme. ui elements have been updated to match the [greybeard sublime text theme](https://github.com/xero/greybeard-sublime).

## automated installation:

### chrome webstore

free to download and install via the [chrome webstore](https://chrome.google.com/webstore/detail/greybeard-devtools-theme/cckelcjlkjehoepkfcpgdpjfagodhimd)

after installing you need to enable custom themes:
- navigate to `chrome://flags/`
- enable `Developer Tools experiments`
- reload chrome
- open devtools
- click settings > experiments
- click `allow custom ui themes`
- reload devtools for theme to fully apply

## manual installation:

as of chrome / chromium version 32 devtools themes are deprecated :( but, there is a work around. 

### version 33+

1. clone this repo somewhere

2. in chrome, open chrome://extensions

3. select "Developer mode"

4. click on "Load unpacked extension"

5. select this directory

6. optionally restart (required for some systems)

### version 32

read this and follow the directions: http://stackoverflow.com/questions/17042547/how-to-inject-javascript-into-chrome-devtools-itself/17044405#17044405

### version > 31

1. find chrome's user stylesheets directory:

	mac - Finder > shift + cmd + g:

	`~/Library/Application Support/Google/Chrome/Default/User StyleSheets/`

	mac - terminal:

	`~/Library/Application\ Support/Google/Chrome/Default/User\ StyleSheets/`

	windows:

	`C:\Users\**Your Username**\AppData\Local\Google\Chrome\User Data\Default\User StyleSheets\`

	linux (chromium / goole chrome):

	`~/.config/chromium/Default/User StyleSheets/`

	or

	`~/.config/google-chrome/Default/User StyleSheets/`

2. replace the existing "Custom.css" file with [this one](https://raw.githubusercontent.com/xero/greybeard-devtools/master/Custom.css)

3. no restart needed, changes are applied immediately, which is awesome! so hack away!

## sublime

greybeard also available for as a matching [sublime text 2 theme](https://github.com/xero/greybeard-sublime).

![greybeard devtools and sublime screenshot](https://raw.githubusercontent.com/xero/greybeard-devtools/master/preview3.png)

## credits

greybeard
xero harrison
https://github.com/xero/greybeard-devtools

SO-Dark-Monokai-v3
simon owen
https://github.com/s10wen/SO-Dark-Monokai-v3

IR_Dark_Monokai
Designed and developed by Andres Pagella:
http://www.andrespagella.com/customising-chrome-devtools

James Doyle:
https://github.com/james2doyle/SO-Dark-Monokai-v3/commits/master

Ben Truyman, Todd Werth:
http://blog.toddwerth.com/entries/2

Toolbar code by Harris Novick:
https://gist.github.com/4316646

Inspired by Darcy Clarke's blog post:
http://darcyclarke.me/design/skin-your-chrome-inspector/

Dock-To-Right when using vertical splitting:
https://github.com/mauricelam/DockToRight

Automatic rake file by Rodolfo Puig:
https://github.com/simonowendesign/SO-Dark-Monokai-v3/pull/21
