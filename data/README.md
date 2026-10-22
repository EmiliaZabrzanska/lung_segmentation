# Data

The X-ray images are not version-controlled (`.gitignore` ignores everything in this folder except
this file). Download `MontgomerySet.zip` from Canvas and unzip it here, so that the folder looks like:

```
data/
└── MontgomerySet/
    ├── CXR_png/             MCUCXR_0001_0.png, ...   (X-rays)
    └── ManualMask/
        ├── leftMask/        MCUCXR_0001_0.png, ...   (left lung masks)
        └── rightMask/       MCUCXR_0001_0.png, ...   (right lung masks)
```

If the folder names differ, change the paths in the first code cell of Part 1 in `solution.ipynb`.
