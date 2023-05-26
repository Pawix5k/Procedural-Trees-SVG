# Procedural-Trees-SVG

## Checking out SVG

This example will do the trick for now.

```
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <line x1="0" y1="80" x2="100" y2="20" stroke="black" />

  <!-- If you do not specify the stroke
       color the line will not be visible -->
</svg>
```

## Generating trees.

We need some probabilities and (maybe temporarily) limits.
List of needed params:
* offshoot chance
```
\|
 |
```

* split chance
```
\ /
 |
```
* no growth chance
```
end
 |
```
* angle of offshoot
* angle of split
* angle of no offshoot-split
* delta of chances to split and to no growth

For now enough i guess.
