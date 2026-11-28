# (0.1.3) More bug fixes
After testing all the raise areas, and checking the boundary bug again (#1) and stuff, I found like three bugs.

Don't tell my teacher...

## New Features

## Fixed Bugs
- Tested and fixed weight change (#1) bug
- `Validator.__new()` only took case sensitive options; fixed that (#5)
- Crashing program if config contains erroneous values (#4)


# (0.1.2) Fixed Visual bug
A visual bug was found during the presentation (;-;)

The max height needed to be set to `0.0` to be disabled.
When the weight input was taken, the visual bug output:
```
And your current weight?
> -100
Enter a valid weight! Must be numerical and between 0.0 and 0.0.
```

That was fixed.

## New Features

## Fixed Bugs
- Visual bug when max weight was set to `0.0`. (#3)

# (0.1.1) Bug fixes & multiple athlete support
Just some bugfixes after review

## New Features
- Multiple athletes can be registered sequentially

## Fixed Bugs
- Fixed a weight category calculation bug (#2)
- Fixed a weight validation bug (#1)

# (0.1.0) Initial Commit
Base application

## New Features
- Calculates the fees for judo practice
- Prices can be fully customized using the config file

## Fixed Bugs
