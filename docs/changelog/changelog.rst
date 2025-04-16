v0.3.0 (2025-04-16)
===================

Feat
----

- **index**: add ability to get liquidity index (:pull:`171`)
- **index**: add ability to get plasticity index (:pull:`170`)
- **index**: add ability to get plastic limit (:pull:`169`)
- **index**: add ability to get liquid limit (:pull:`167`)

v0.2.0 (2025-04-14)
===================

Feat
----

- **index**: add prefix to get_moisture_content method (:pull:`156`)
- **index**: add ability to get moisture content (:pull:`141`)
- **index**: add subaccessor for index property tests (:pull:`105`)
- **lab**: add lab subaccessor (:pull:`104`)

Perf
----

- use list comprehension in column validation (:pull:`140`)

v0.1.1 (2023-12-12)
===================

Fix
---

- **spt**: fix report on samples with only 150mm total penetration (:pull:`102`)

v0.1.0 (2023-12-05)
===================

Feat
----

- **spt**: add ability to get a simple descriptive report (:pull:`74`)
- **spt**: add ability to check if any sample is hammer weight (:pull:`73`)
- **spt**: add ability to check if any sample is a refusal (:pull:`72`)
- **spt**: add ability to get the seating penetration of each layer (:pull:`70`)
- **spt**: add ability to get the main penetration of each layer (:pull:`69`)
- **spt**: add ability to get the total drive of each layer (:pull:`68`)
- **spt**: add ability to get the N-value of each layer (:pull:`67`)
- **spt**: add ability to get the main drive of each layer (:pull:`65`)
- **spt**: add ability to get the seating drive of each layer (:pull:`62`)
- **spt**: add ability to get the total penetration of each layer (:pull:`61`)
- **spt**: add spt subaccessor (:pull:`60`)
- **in-situ**: add in-situ subaccessor (:pull:`59`)
- **point**: add property that lists unique point IDs (:pull:`45`)
- **layer**: add layer subaccessor (:pull:`43`)
- **utils**: add sub-accessor object for auto-documentation (:pull:`34`)
- **accessor**: register geotech accessor on package import (:pull:`33`)
- **accessor**: register dataframe accessor as geotech (:pull:`15`)
- **point**: add ability to split layers (:pull:`13`)
- **point**: add ability to get thickness of depth values (:pull:`12`)
- **point**: add ability to get center depth values (:pull:`11`)
- **point**: add ability to get top depth values (:pull:`9`)
- **point**: add ability to get group from point groups (:pull:`8`)
- **point**: add point dataframe accessor (:pull:`7`)
- **base**: add automatic validation on init (:pull:`6`)
- **base**: add duplicate validation (:pull:`5`)
- **base**: add monotony validation (:pull:`4`)
- **base**: add column name validation (:pull:`3`)
- **base**: add base class (:pull:`2`)
