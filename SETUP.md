# Setup – step by step

Everything below is typed into the **Terminal** app on your Mac.
Lines starting with `#` are comments explaining the command – you don't type those.

---

## Step 1 · Create the repository on GitHub

1. Go to <https://github.com/new>.
2. **Repository name:** `lung_segmentation`
3. Choose **Private** (you can make it public after the module is marked).
4. **Leave all the "Initialize" boxes unticked** (no README, no .gitignore, no licence) –
   this repository already has those files.
5. Click **Create repository**. Leave the page open; you need its URL in Step 3.

## Step 2 · Put the project folder on your Mac

Unzip `m03_lung_segmentation.zip` somewhere sensible, e.g. `~/Documents/CDT/`, then:

```bash
cd ~/Documents/CDT/lung_segmentation   # go into the project folder
ls                                         # you should see README.md, lungseg.py, the notebooks...
```

## Step 3 · Connect the folder to GitHub and upload it

```bash
git init                     # turn the folder into a git repository
git branch -M main           # call the main branch "main" (GitHub's default)
git add .                    # stage every file (data/ is skipped thanks to .gitignore)
git commit -m "Initial project structure"   # save a snapshot
git remote add origin https://github.com/EmiliaZabrzanska/lung_segmentation.git
git push -u origin main      # upload; -u remembers "origin main" for future pushes
```

Refresh the GitHub page – your files should be there.
(If `git push` asks for a password, use a GitHub *personal access token* or
sign in through GitHub Desktop / `gh auth login`, the same way you did for A2/A7.)

## Step 4 · Create a Python environment and install packages

A virtual environment keeps this project's packages separate from everything else.

```bash
python3 -m venv .venv               # create the environment in a hidden folder .venv
source .venv/bin/activate           # switch it on (your prompt now starts with (.venv))
pip install -r requirements.txt     # install numpy, scikit-image, scikit-learn, jupyter...
```

Next time you only need `source .venv/bin/activate`.
(`.venv/` is in `.gitignore`, so it's never uploaded.)

## Step 5 · Get the data

**Option A – on your Mac.** Copy the `MontgomerySet` folder from the CDT server (or download
the zip – see `data/README.md`) into `data/`, so you have `data/MontgomerySet/CXR_png/...`.
For example, from the server:

```bash
scp -r YOUR_USERNAME@SERVER_ADDRESS:/data/cdtshared/Cohort-2024/HDS-M03/MontgomerySet data/
```

**Option B – work on the CDT server.** Clone your repo there instead, and change one line in
`lungseg.py`:

```python
DATA_DIR = Path("/data/cdtshared/Cohort-2024/HDS-M03/MontgomerySet")
```

Then check the folder names inside match `CXR_png`, `ManualMask/leftMask`, `ManualMask/rightMask`
(run `ls` on the folder). If they're different, edit the three lines below `DATA_DIR` in `lungseg.py`.

## Step 6 · Run the notebooks

```bash
jupyter notebook
```

Open `01_data_exploration.ipynb` and run each cell with **Shift + Enter**.
The first cell after the imports prints how many images were found – it should say
**138 total, 80 normal, 58 TB** (the instruction sheet says 53 TB, but the data set has 58). If it says 0, go back to Step 5.
Then work through 02 → 03 → 04.

## Step 7 · Save your progress to GitHub as you go

After each notebook (or whenever something works):

```bash
git add .                                    # stage what changed
git commit -m "Finish thresholding notebook" # describe what you did
git push                                     # upload
```

Tip: before committing, use **Kernel → Restart & Run All** so the saved notebook shows
outputs that match the code, from top to bottom.
