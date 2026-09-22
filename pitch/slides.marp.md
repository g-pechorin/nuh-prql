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

- We have complicated queries with lots of data to run against a read-only SQL Server database
- NDO lists > 100 rows to select against
- Multiple overlapping queries to group/regroup data from SACT/COSD/...
- Security says ... please only use .sql files ...
  - ... don't connect new software to the NUH system ...

---

## Possible Solution; a pre-SQL stack/tool?

- Turn something more ... legible ... into SQL
- Run locally or on BC Insight when ready
- Inline .csv files into CTE subqueries

> This solution is “weird” because it isn't TurnKey and implies we need to work around the current trust model. It’s not sneaking anything in though - it’s just automating copy/paste work for writing `.sql` queries.

---

## PRQL - PreSQL

![blurp](res/prql-blurb.png)

---

### PRQL – PreSQL (Example)

<div class="columns_40_60">
<div>

- Not "married to" the idea of this language
- ... and usage will have a lot of Googl'ing

The goal is more-concise than the Götterdämmerung style `.sql` we use now. Embed `.csv` and/or import `.sql` or other queries.

Maybe just an `.sql` rewriter?

</div>
<div>

![width:100%](res/prql-example.png)

</div>
</div>

---

### PRQL – CTE from `.csv` text

When compiled, a blurb of CSV becomes a CTE expression.

![height:400px](res/prql-csv.png)

> I don't know if 100+ NDO records are too much

---

### PRQL – Importing from `.csv` file

The builtin syntax exists, but, it's limited to DuckDb. We can perform string substitution with Python before compiling it.

> I've checked and this is ... fine?
> `.csv` substitution worked on Friday afternoon.

![width:800px](res/prql-files.png)

---

## The Stack

<div class="columns_40_60">
<div>

[![](https://mermaid.ink/img/pako:eNplUk1vgzAM_SuWT51EUQlQPg67rIcdtk5Tu8tKDxmkFAkSGkI_VvW_L4SWbWqkOLZfnv0c5YypyBjGuCnFId1SqWA5SzjoVctdubI7C5uiZA0UHPJCrXuUZ2Jlp82-c674_G35_04qqlojo-sJaqv3QYASOdO-fOivNV0fbWDXMlnoQmOgZSPu63X4aWQsGILgMP94hsX7CyyY3A8VFf3SglYN3TOQrGlL1eimwNkBjGajd_07JozHjze1w3j3ydscHaDbD-pNwsj6o9MkeyEJRwtzWWQYK9kyCysmK9qFeO4YCerXqFiCsXYly9rjOBWlkAkm_KKpNeWfQlQ3thRtvsV4ox9JR22dUcVmBc0lrYasZDxj8km0XGHsOJ5rqmB8xqOOiW_7rkOIG5HIi5wwsvCEMfFD2594oRt4xA09h1ws_DZ9J7YXBpMgmgZRNPWjgGgCywol5Gv_e8wnuvwASFe7Iw?type=png)](https://mermaid.live/edit#pako:eNplUstO60AM_RXLK67URs2LPBZ3c1ncBQ8hYEPDYkjcNFIyU5xJC1T9d5wJLSAixWP7-NjHo9ljaSrCHFet2ZVrxRbuLwoN8m34pV16o4VV01IPjYa6sU8Tqiuz9Mp-Ozqf-PXN_c-a0nQbQc4-T7Br-XcGrKlJfP4zlfXjHDHwMhA30mgOqu3N734j_nbmLDiC0XD98B_ubi_hjnhLPNVZ9Sx6lr3aEjD1Q2t7mQmaduAkO7lPX1vCfP73KPa03e_kcY0RkOkn8S7hVH2T6ZKTkELjDGtuKswtDzTDjrhTY4j7kVGgXEZHBebiMlXD67w0reECC30Q6kbpR2O6I5vNUK8xX8kdSTRsKmXpolE1q-6UZdIV8T8zaIu574eZ64L5Hl8lDmIvDv0gCLMgizI_FfQN8yBOvXgRpWESBWEa-cFhhu9u7sKL0mSRZOdJlp3HWRIIgarGGr6aHo97Q4cPx3W6_w)

</div>
<div>

- this isn't a complex Python setup
- creating `.sql` can be run on BC Insights

</div>
</div>

---

### (Future?) Automate CDM with The Stack

<div class="columns_40_60">
<div>

[![](https://mermaid.ink/img/pako:eNpVkrFugzAQhl_FurEC1AAhiKFLO7ZD1a2lA8IHsYptctgRaZR3r7HThrLA_fru_J3MGVrNESqYTGPwSTQ9NTI-prVi7jlYpBOr2EhajobZCYkZzcgqNmmJ7O31OYAjHQbHtQ4TA7LE14PWX0L1rNPEhBw1mSnQEqlHh4d30k5HJpSba_bojxR4BXFuMcxVbWMC2QnVDCyZh2lmXLdWojKBnvaiM47mbpNrsUwMaMtloD7uPlkcP3jllfwS-XXXmy-hl1x7_2--gV527b2EXmOtt4ROASLoSXCoDFmMwE2WzVLCeYFrcOISa6jcJyG3c9zqQVMNtbq41rFR71rL327Stt9D1TXD5Co78ttV_qWEiiM9aqsMVJs0LyNALoyml3D__jfwk6E6wwxVXmySLE23xX1eZuW2LPIITi5Ok2xT5nmW5TuXFbtLBN_e5T4pd9vLD1I_u9Y?type=png)](https://mermaid.live/edit#pako:eNpVkrFugzAQhl_FurEC1AAhiKFLO7ZD1a2lA8IHsYptctgRaZR3r7HThrLA_fru_J3MGVrNESqYTGPwSTQ9NTI-prVi7jlYpBOr2EhajobZCYkZzcgqNmmJ7O31OYAjHQbHtQ4TA7LE14PWX0L1rNPEhBw1mSnQEqlHh4d30k5HJpSba_bojxR4BXFuMcxVbWMC2QnVDCyZh2lmXLdWojKBnvaiM47mbpNrsUwMaMsD9HH3yeL4wRuv3JfIb7tefAm941r7f_MN9K5r7SX0Fmu7JXQKEEFPgkNlyGIEbrJslhLOC1yD85ZYQ-U-Cbmd41YPmmqo1cW1jo1611r-dpO2_R6qrhkmV9mR327yLyVUHOlRW2Wg2qR5HgFyYTS9hOv3f4GfDNUZZqjyYpNkabot7vMyK7dl4TpOLk6TbFPmeZblO5cVu0sE397lPil328sPaGG7ZQ)

</div>
<div>

Using an existing `.xlsx` file as a template, and the `sheet_config:{...}` from date shifting, automate the creation of date-shifted documents.

> ... or skip the shifting step until later ...

_Just_ need a python script that digests the configuration and prompts the user to query / save results to `.csv` and combine into new queries.

> ... and add something like `ROWCOUNT(*) AS row_count` then check it to verify of the results are complete ...

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
  - ... we can write text logs though ...
- it's another new internal tool
- PRQL is an esoteric language
  - ... could maybe swap `.sql`?
- complex usage needs to run SQL
  - python could run `ssms.exe`
  - ONLY to open the `.sql`

</div>
</div>

... so ... I expect this approach could be heckled to pieces and reassembled into something more conventional.

---

## Solutions For Now ...

- ~~complicated queries~~
  - more expressive query language
- ~~NDO lists~~
  - substitute them into the queries when compiled
- ~~overlapping queries~~
  - re-use multiple smaller shared sub-queries
- ~~Security / only use .sql~~
  - we're running the generated `.sql` by hand

---

## À la fin

So the big ideas are;

- perform string substitution to get _better_ `.sql` with less work
  - possibly with fancier not-SQL language
- prompt Human to run the generated `.sql`
  - maybe using fancy steps
    - opening it for them
    - checking the results have enough rows
- never ever save the generated `.sql` or `.csv` to git
