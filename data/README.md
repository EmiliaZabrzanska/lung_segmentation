# Data folder

The X-ray images are **not** stored on GitHub (`.gitignore` ignores everything in this
folder except this file). Put your copy of the Montgomery County X-ray set here so it looks like:

```
data/
└── MontgomerySet/
    ├── CXR_png/                  MCUCXR_0001_0.png, ...   (the X-rays)
    └── ManualMask/
        ├── leftMask/             MCUCXR_0001_0.png, ...   (left lung masks)
        └── rightMask/            MCUCXR_0001_0.png, ...   (right lung masks)
```

Where to get it:

* **CDT server copy:** `/data/cdtshared/Cohort-2024/HDS-M03/MontgomerySet`
  (if you work on the server you don't need to copy anything – just change `DATA_DIR` in `lungseg.py`).
* **Online:** http://openi.nlm.nih.gov/imgs/collections/NLM-MontgomeryCXRSet.zip – unzip it into this folder.

If your copy uses different folder names (e.g. `left/` and `right/`), edit the three
folder lines at the top of `lungseg.py` – nothing else needs to change.
