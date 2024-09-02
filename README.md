# Business Innovation in Commercial Space: Culture and Trends in Earth Observation

This repository contains the data and analysis code to support methods in our paper, *Business Innovation in Commercial Space: Culture and Trends in Earth Observation*, by Giulia Cambone*, Holly Dinkel*, Luca Ferrone*, Antonio Stark*, Shinsuke Kito*, Chawalwat Martkamjan*. This work was conducted within the framework of the 2024 International Astronautical Federation (IAF) International Programme/Project Management Committee (IPMC) Young Professionals' Workshop.

*Authors listed in alphabetical order by last name.

## Motivation

Enhanced access to space, climate and natural resource monitoring, space-based awareness, on-demand analytics, and data independence motivate a growing commercial EO market. An increasing number of diverse companies globally strive to establish their own competitive market niche, but often do not reach commercial viability. Existing work provides market intelligence and identifies trends in venture financing. These methods do not indicate cultural and financial mechanisms enabling the innovation required to sustain market share for incumbent players or market penetration for emerging ones.

This study measures the innovation success of selected companies worldwide based on internal policies, management approaches, and market demand. Time-series financial metrics indicate innovation trends for businesses across the commercial EO landscape.

<p align="center">
  <img src="images/revenue_separate.png" width="900" title="Revenue">
  <img src="images/ebitda_separate.png" width="900" title="EBITDA">
</p>

## Dependencies

- numpy
- pandas
- matplotlib
- json
- statsmodels

## Using Prepared Data

Clone the repository:

```bash
git clone git@github.com:hollydinkel/space_econometrics.git
```

To run the script and generate results on existing data in the repository, run:

```bash
python src/process.py
```

## BibTex

```bash
@ARTICLE{
  iafipmc2024innovation,
  author={Cambone, Giulia and Dinkel, Holly and Ferrone, Luca and Kim, KangSan and Kito, Shinsuke and Martkamjan, Chawalwat},
  journal={IAF International Astronautical Congress}, 
  title={Business Innovation in Commercial Space: Culture and Trends in Earth Observation}, 
  year={2024},
  month={Oct.},
}
```