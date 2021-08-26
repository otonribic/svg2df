# svg2df
Convert SVG files into Dark Forces .LEV geometry

An experiment for a PoC level I've experimented with - feed this script an SVG file, and it should produce geometry that can be pasted into a Dark Forces .LEV file.

It doesn't handle sector gaps yet, perhaps that will be added when needed. And it creates no adjoins, though these are easy enough to auto-generate in WDFUSE editor in a few seconds.

Lightness/floor/ceiling values are lists - and if a list with only one value is given (e.g. [23]) then the corresponding value will always be 23. If multiple values are present (e.g. [10,12,13,16,21]), then the script will choose one of these randomly.
