# iTunes Scripts

I'm slowly finding out iTunes sucks, and a lot of resources to fix shitty things with
iTunes are some scripts a (generous) guy made in assembly or powerpoint or something :(

I have no choice but to write it in python.

All scripts should be executable by doing:

`python script_name.py args`

Just have Python (2 or 3 I believe) installed. Descriptions of what everything
does are below.

## Convert an iTunes playlist to an HTML list `playlist_to_html_list`

iTunes will export a playlist as a garbled `.txt` file. It sucks. The first step
that should happen (before running this script) is to convert this`.txt` file
into a `.csv` file. This can be done using Excel, or maybe some other program.

To be honest, the text files are formatted so poorly, that it was impossible
trying to convert it via Python. If someone has a way to do it I'd gladly merge it
into this script. 

### Running the script
I've made a script that will run through this playlist and give you back a nicely formatted
HTML list in the following format:

```html
<ul>
  <li>Artist - Song Name</li>
</ul>
```

It's done this way so that you can apply whatever styles you want after.
