---
marp: true
theme: default
paginate: true

# # Convert to HTML (output auto-named)
# npx @marp-team/marp-cli@latest pitch/slides.marp.md

# # Convert to PDF
# npx @marp-team/marp-cli@latest pitch/slides.marp.md --pdf

# # Convert to PPTX
# npx @marp-team/marp-cli@latest pitch/slides.marp.md --pptx

# # Watch mode (auto-rebuild on save)
# npx @marp-team/marp-cli@latest -w pitch/slides.marp.md

# # Server mode (preview in browser)
# env PORT=1983 npx @marp-team/marp-cli@latest -s ./pitch

style: |
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr; /* two equal columns */
    gap: 2rem;
    align-items: center;
  }
  .columns_40_60 {
    display: grid;
    grid-template-columns: 4fr 6fr; /* 30/70 */
    gap: 2rem;
    align-items: center;
  }
---

# NUH - PRQL / The Stack

(internal presentation ONLY - very informal)

---

## Problem

- We have complicated queries with lots of data
  - read-only SQL Server database
- NDO lists > 100 rows to select against
  - previously _just_ copied and pasted by hand
- Multiple overlapping queries of data from SACT/COSD/et-al
  - map/reduce/scatter/group style stuff
- Security says; please only use SQL Studio
  - ... don't connect new software to the NUH system ...
- Auditing and Logs of what's happened
  - We'd like to know who's doing what with this

---

### Possible Solution; a pre-SQL stack/tool?

"Horizontal Thinking" (maybe) is that just because we can't connect programs to the server, doesn't mean we can't write programs to prepare/template our queries for us.

- Turn something more ... legible ... into SQL
- Construct `.sql` on NUH-Laptop or BC Insight
  - write to real, honest, on-disk files we then run by hand ...
- Inline .csv files into CTE subqueries
  - ... so Save Results from SQL Studio to a `.csv` file noted in the comments

```
$ uv run the_stack.py studies/endo2607A9/ ~/Desktop/endo-cache
```

... assumes `.prql`s, `cdm-template.xlsx` and/or `sheet.py`

---

### I know this is Weird <sup>TM</sup>

This solution is “weird” because it isn't TurnKey; when you run this extraction it turns around and starts asking you to run stuff for it.

It layers around the current trust model.

... but all `.sql` that passes through the system will be seen by a human / Peter so that's fine?

It’s automating compile/copy/paste work for writing `.sql` queries with inlaid data, then binding the data into a `.xlsx` file.

> ... and if we're doing this by a program; we can add logging that pushes to GitHub to that program?

---

## PRQL - PreSQL

First idea<sup>2</sup> (when I was designing this) use a compiles-to-SQL<sup>1</sup> to simplify writing queries.

![height:250px](res/prql-blurb.png)

> <sup>1</sup> The SQL version of TypeScript compiling to `.js`!
>
> <sup>2</sup> ... actually ... my first idea was to write a Python2SQL compiler; best not to get that sort of thing on The Day Job

---

### PRQL – PreSQL (Example)

<div class="columns_40_60">
<div>

- Slightly more concise?
- I didn't make this up!
- ... usage need Googl'ing

Less like the "Götterdämmerung style `.sql`" we need to use now.

... or maybe just steal their ideas and rewrite `.sql` files ourselves with something like `#include "base-query.sql"`?

</div>
<div>

![width:100%](res/prql-example.png)

</div>
</div>

---

### pcpp + sql (Plan B)

Maybe use something like pcpp (a C-Preprocessor written in Python) to allow ...

> One _can_ hook into the `#include` to generate `.sql` from `.csv`

<div class="columns_40_60">
<div>

... something like this ...

```
#define macro(COL, VALUEIS) \
  SELECT COL as #COL \
  FROM table \
  WHERE VALUEIS \
WITH (
macro(dob, diagnosis=3)
UNION ALL
macro(dob, diagnosis=2)
) AS Pre
SELECT *
  FROM Pre
  #include "where.sql"
```

</div>
<div>

... to become this ...

```
WITH (
  SELECT dob as "dob"
    FROM table
    WHERE diagnosis=3
UNION ALL
  SELECT dob as "dob"
    FROM table
    WHERE diagnosis=2
) AS Pre
SELECT *
  FROM Pre
WHERE apples = 'oranges'
```

</div>
</div>

---

### PRQL – CTE from `.csv` text

But PRQL is "closer to market" for this, and, a CSV text can become a CTE expression ...

![height:350px](res/prql-csv.png)

... so _that_ step could be automated and inlaid into `.sql` or `.prql`

> I don't know if 100+ NDO rows would be too big as a CTE; can adjust

---

### PRQL – Importing from `.csv` file

PRQL _does_ have builtin DuckDB syntax; we can be consistent and DIY a hook for that.

> ... just for `.csv`
>
> ... this worked on _my PC_ when I tried it at lunch/Friday ...

![width:800px](res/prql-files.png)

---

## The Stack

<div class="columns_40_60">
<div>

[![](https://mermaid.ink/img/pako:eNplUk1vgzAM_SuWT51EUQlQPg67rIcdtk5Tu8tKDxmkFAkSGkI_VvW_L4SWbWqkOLZfnv0c5YypyBjGuCnFId1SqWA5SzjoVctdubI7C5uiZA0UHPJCrXuUZ2Jlp82-c674_G35_04qqlojo-sJaqv3QYASOdO-fOivNV0fbWDXMlnoQmOgZSPu63X4aWQsGILgMP94hsX7CyyY3A8VFf3SglYN3TOQrGlL1eimwNkBjGajd_07JozHjze1w3j3ydscHaDbD-pNwsj6o9MkeyEJRwtzWWQYK9kyCysmK9qFeO4YCerXqFiCsXYly9rjOBWlkAkm_KKpNeWfQlQ3thRtvsV4ox9JR22dUcVmBc0lrYasZDxj8km0XGHsOJ5rqmB8xqOOiW_7rkOIG5HIi5wwsvCEMfFD2594oRt4xA09h1ws_DZ9J7YXBpMgmgZRNPWjgGgCywol5Gv_e8wnuvwASFe7Iw?type=png)](https://mermaid.live/edit#pako:eNplUstO60AM_RXLK67URs2LPBZ3c1ncBQ8hYEPDYkjcNFIyU5xJC1T9d5wJLSAixWP7-NjHo9ljaSrCHFet2ZVrxRbuLwoN8m34pV16o4VV01IPjYa6sU8Tqiuz9Mp-Ozqf-PXN_c-a0nQbQc4-T7Br-XcGrKlJfP4zlfXjHDHwMhA30mgOqu3N734j_nbmLDiC0XD98B_ubi_hjnhLPNVZ9Sx6lr3aEjD1Q2t7mQmaduAkO7lPX1vCfP73KPa03e_kcY0RkOkn8S7hVH2T6ZKTkELjDGtuKswtDzTDjrhTY4j7kVGgXEZHBebiMlXD67w0reECC30Q6kbpR2O6I5vNUK8xX8kdSTRsKmXpolE1q-6UZdIV8T8zaIu574eZ64L5Hl8lDmIvDv0gCLMgizI_FfQN8yBOvXgRpWESBWEa-cFhhu9u7sKL0mSRZOdJlp3HWRIIgarGGr6aHo97Q4cPx3W6_w)

</div>
<div>

So what would this look like when it's running?

- it's a Python program
- the `.py` can run on BC Insights
- `.sql` needs to run on NUH-Laptop
  - ... with SQL Studio

... or could run it all on NUH-Laptop and automate prompting The Operator with the invoke/query/read approach used to extract schemas?

</div>
</div>

> ... running it on NUH-Laptop could push/pull audit logs too ...

---

### Fully Automate CDM with The Stack

<div class="columns_40_60">
<div>

[![height:570px](https://mermaid.ink/img/pako:eNpVks2OozAQhF-l1ccVsSbAEIbDXmau8wK77MECh0ExbqaNI7JR3n39k2wSX7CLqtLnls_YUa-wQbvIRX2McmA5bY55a8Cv0RzpoKABZxVfTxaWLwViPsHMFNzJOvO39sarBraTxnpXUDXRYTQD7IlBdPb4FJD2YFP9QsDOQEfEys5k-pAR9lsnPystT1cS77PxF0jTg5VHT3VvnhQPATp9g-7RfXvi5lvhzSaEAE82s5olK9iPRmogt8xuSUa1dkqnIaS2_ajDGChstO_2FCBWbVd4__hMmd8__sBm8_M6s6dpBvlOEccQpHi_h6tGMTI-4j6H71pkfMQNoofADAcee2wWdipDH5hkOOI5mFv0M5lUi43fsurduulIE7fYmouPztL8IppuaSY3fGGzl9r6k5v7-5P5r7IyveJ3cmbBZpuXVYaqHxfiz_TO4nOLzdicccWmrLaiyPPX6qWsi_q1rsoMT17ORbGty7Ioyp3Xqt0lw7-R5UXUu_LtcV3-ASPl4Lo?type=png)](https://mermaid.live/edit#pako:eNpVksFyozAQRH9lSsctrI2B2IRDLsk1P5CQgwrGhLLQkJEgeF3-95WQHdu6IDXdXU9TOoqaGhSlsE45fO1Uy6pfTWllwK_OTLRHKGG0yOeTBfeFIIcDDEzBHa0Df2tvPGtga2WsdwVVE-0708KOGGRtp7uAsnsb6x0BjwZqIkY7kGlCRtpvHf2MWh3OJN5nl1-gTANWTZ7q2twjtwE6foPu0X175OZL4cUmpQRPNjAOihF2nVEaaHTD6KIR5xp1HEJs23U6jIHCRvvuvzQh_3Dn0POAnLWd4eX1LaY__nzCavV8nt7dXIN85VkGEqTlpjeXXsSF9hb8PnzVFtpb8CB6CJGIlrtGlI5HTIQP9CocxTGYK-Gn02MlSr9lbMZ5VZMmrkRlTj46KPNO1F_STGP7Jcqd0tafxqG5Pp5fldE0yC80GifKdZqnicCmc8Rv8cUtD29pFuVRzKLMN2uZpenj5iEvsuKx2OSJOHg5ldm6yPMsy7de22xPifi3sDzIYps_3a7Tf6i05Mw)

</div>
<div>

Bit of a process change; can _mostly_ just use the date shift `sheet_config:{...}` to map `.csv` data into `study-cdm-template.xlsx`

**No python/prql connection to NUH or TEDX!**

Involves an "orchestration" CLI batch program that loops checking for data, writing `.sql` and prompting The Operator to query SQL Studio and save the results to the proper `.csv`.

> ... and use a column `ROWCOUNT(*) AS row_count` to check for completeness ...

</div>
</div>

---

## What's Wrong?

So what's wrong with this approach?

<div class="columns">
<div>

- Provenance and Auditing
  - want to know who ran what when
- Yet Another Internal Tool
- odd new language
  - ... which none of us know?
- "operator in the middle"
  - ask dev to exec query
  - ... and save results as ...

</div>
<div>

- no external log of what was run
  - could write text/git logs?
- it's another new internal tool
- PRQL is an esoteric language
  - ... could maybe swap `.sql`?
- needs to run SQL Studio
  - python could run `ssms.exe`
  - ... but ONLY to open the `.sql`

</div>
</div>

... so ... I expect this approach could be heckled to pieces and reassembled into something more conventional. It's still what I'd do if left to my own devices.

---

## Solutions For Now

- ~~complicated queries~~
  - more expressive query language
- ~~NDO lists~~
  - substitute them into the queries when compiled
- ~~overlapping queries~~
  - re-use multiple smaller shared sub-queries
- ~~Security / only use .sql~~
  - we're running the generated `.sql` by hand
- Audit Logs
  - ... write to text file/git/commit/push?
  - ... could make the orchestration do that?

---

## À la fin

So the big ideas are;

- perform string substitution to get _better_ `.sql` with less work
  - possibly with fancier not-SQL language
- prompt The Operator to run the generated `.sql`
  - ... and save to specific `.csv`
  - maybe using fancy steps
    - `os.system('ssms.exe path.to/query-34AB32.sql')`
    - checking the results have enough rows
- never ever save the generated `.sql`, `.csv`, or `.xlsx` to git
