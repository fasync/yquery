# yquery
Query, play and download youtube videos from your cli

__NOTE__: For now you need a API developer key for using this tool, because this is still in development and OAuth is not implemented yet

### What is this??
A very simple script, so don't expect too much.

### Requirements
- py37-google-api-python-client
- mpv (for playing)
- youtube-dl (optional, for downloading)

### Ideas
Maybe I'll be update this script so far so we don't need mpv or youtube-dl anymore. But yet I just wanted a little tool for searching my music over the cli.

### Howto
I prefer using interactive mode. 
```
yquery.py -i
```

This opens a menu.
If you browse to the query menu, you can edit some settings, and with index 0 (search [STRING]) you will be asked for a search string.
After starting a query, the results will be listed. No you can use H J K L for navigating through the results.

`h` or `q` will get you back to the query menu.
`j` and `k` will navigate down and up
`l` will play the marked video.
`d` will download the marked video.

### TODO
I plan to implement the following features:

```
[x] Play
[x] Download
[ ] Autoplay
[ ] Download Options
[ ] Implement complete cli command
[ ] OAuth
[?] Maybe command completion
[?] Maybe something different than a index based menu, something more modern
```
