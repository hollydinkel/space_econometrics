# Business Innovation in Commercial Space: Culture and Trends in Earth Observation

This repository contains the data and analysis code to support methods in our paper, *Business Innovation in Commercial Space: Culture and Trends in Earth Observation*, by Giulia Cambone*, Holly Dinkel*, Luca Ferrone*, KangSan Kim*, Shinsuke Kito*, Chawalwat Martkamjan*. This work was conducted within the framework of the 2024 International Astronautical Federation (IAF) International Programme/Project Management Committee (IPMC) Young Professionals' Workshop.

*Authors listed in alphabetical order by last name.

## Motivation

Enhanced access to space, climate and natural resource monitoring, space-based awareness, on-demand analytics, and data independence motivate a growing commercial EO market. An increasing number of diverse companies globally strive to establish their own competitive market niche, but often do not reach commercial viability. Existing work provides market intelligence and identifies trends in venture financing. These methods do not indicate cultural and financial mechanisms enabling the innovation required to sustain market share for incumbent players or market penetration for emerging ones.

This study measures the innovation success of selected companies worldwide based on internal policies, management approaches, and market demand. Time-series metrics, including Return on Equity, Net Profit Margin, Financial Leverage, Asset Turnover, Asset Growth Rate, Equity Growth Rate, and Liabilities Growth Rate, indicate financial trends for businesses across the commercial EO landscape. An Auto-Regressive Distributed Lag model is also implemented to identify the impacts of assets, equity, liabilities, and number of satellites on company revenue and EBITDA. The model is used to forecast revenue and EBITDA into the future for each company.

<p align="center">
  <img src="images/revenue_separate.png" width="900" title="Revenue">
  <img src="images/ebitda_separate.png" width="900" title="EBITDA">
</p>

<p align="center">
  <img src="images/ardl_example.png" width="700" title="ARDL Example">
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