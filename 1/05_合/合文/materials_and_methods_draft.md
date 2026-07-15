# 2. Materials and Methods

> 适用期刊: Food Chemistry / Computers and Electronics in Agriculture
> 基于: Liu 2024 · Liao 2025 · Guo 2025 · Ivanova 2020 · Omari 2018 · Younas 2020
> 起草日期: 2026-07-15
> ⚠️ 待确认: Section 2.4 需确认 HS-SPME 模块可用性

---

## 2.1 Sample Preparation

Fresh *Morchella sextelata* (L.) Pers. fruiting bodies with an ascocarp length of 9–11 cm, free from pests and diseases, and exhibiting plump morphology were harvested from [farm location, Chengdu, China]. Surface dust was removed by gentle manual shaking. Samples were transported to the laboratory at 4 °C within 4 h of harvest.

Prior to drying, the stipes were removed and the pilei were cut vertically into slices of 2 ± 0.2 mm thickness using a sterile vegetable slicer. Slices taken from the middle portion of each fruiting body were used for all experiments to minimize positional variation. The initial moisture content of fresh *M. sextelata* was determined by the AOAC oven method (105 °C to constant weight) and was [XX]% ± [XX]% on a wet basis.

Samples were randomly divided into four treatment groups corresponding to four drying temperatures (Section 2.2). Each treatment group consisted of three biological replicates, with each replicate containing approximately [XX] g of fresh mushroom slices.

## 2.2 Hot-Air Drying Experimental Design

### 2.2.1 Drying Equipment

Drying experiments were conducted in a laboratory-scale hot-air convection dryer ([Model, Manufacturer, City, Country]) with a temperature control accuracy of ±1 °C and an air velocity of 1.5 ± 0.1 m·s⁻¹ measured using a hand-held anemometer (HT9829, Xinsite, Dongguan, China) with an accuracy of ±5 % (Guo et al., 2025). The dryer was equipped with a real-time weighing system to record mass changes at 1 min intervals.

### 2.2.2 Experimental Design

A completely randomized factorial design was employed with two factors: **drying temperature** (4 levels: 45, 55, 65, and 75 °C) and **drying time** (6 sampling points: 0, 1.5, 3.0, 5.0, 7.0 h, and the drying endpoint at which the moisture content on a wet basis fell below 15 %). Each temperature × time combination was replicated in triplicate.

```
Table 1. Experimental design summary.

Temperature   Sampling points                   Replicates   Total samples
45 °C        0, 1.5, 3, 5, 7 h + endpoint      3           18
55 °C        0, 1.5, 3, 5, 7 h + endpoint      3           18
65 °C        0, 1.5, 3, 5, 7 h + endpoint      3           18
75 °C        0, 1.5, 3, 5, 7 h + endpoint      3           18
─────────────────────────────────────────────────────────────────
Total                                                                72
```

The temperature range of 45–75 °C was selected to encompass the entire practical drying range for *Morchella*: 45 °C represents the lowest temperature at which effective drying occurs within a reasonable timeframe (Liu et al., 2024; Ivanova et al., 2020), while 75 °C represents an elevated temperature beyond the commonly studied range (55–65 °C) to evaluate potential quality degradation thresholds.

At each sampling point, one replicate batch per temperature was removed from the dryer. The samples were immediately divided into three sub-portions for parallel analyses: (a) volatile compound analysis by HS-SPME-GC–MS (Section 2.3), (b) non-volatile metabolite profiling by LC-MS/MS (Section 2.4), and (c) color and textural measurements (Section 2.5). Sub-samples for GC–MS and LC-MS/MS were flash-frozen in liquid nitrogen and stored at −80 °C until analysis.

## 2.3 Drying Kinetics Analysis

The moisture ratio (MR) was calculated according to Eq. (1):

$$MR = \frac{M_t - M_e}{M_0 - M_e} \quad (1)$$

where $M_t$ is the moisture content at time $t$ (g·g⁻¹, dry basis), $M_0$ is the initial moisture content, and $M_e$ is the equilibrium moisture content. Since $M_e$ is negligible relative to $M_t$ and $M_0$, the equation was simplified to $MR = M_t / M_0$ (Ivanova et al., 2020; Omari et al., 2018).

The drying rate (DR, g·g⁻¹·min⁻¹) was calculated as:

$$DR = \frac{M_{t1} - M_{t2}}{t_2 - t_1} \quad (2)$$

Eleven thin-layer drying models (Lewis, Henderson–Pabis, Logarithmic, Two-term exponential, Page, Modified Page, Wang–Singh, Midilli et al., Diffusion approach, Modified Henderson–Pabis, and Verma et al.) were fitted to the experimental MR data using non-linear regression in Python (SciPy v1.x) (Ivanova et al., 2020). The effective moisture diffusivity ($D_{eff}$, m²·s⁻¹) was calculated from the slope ($K$) of ln(MR) versus time plots using Fick's second law for slab geometry:

$$\ln(MR) = \ln\left(\frac{8}{\pi^2}\right) - \frac{\pi^2 D_{eff}}{4L^2}t \quad (3)$$

$$D_{eff} = \frac{4KL^2}{\pi^2} \quad (4)$$

where $L$ is the half-thickness of the mushroom slice (m). The activation energy ($E_a$, kJ·mol⁻¹) was determined from the Arrhenius relationship:

$$D_{eff} = D_0 \exp\left(-\frac{E_a}{R(T + 273.15)}\right) \quad (5)$$

where $D_0$ is the pre-exponential factor (m²·s⁻¹), $R$ is the universal gas constant (8.314 × 10⁻³ kJ·mol⁻¹·K⁻¹), and $T$ is the drying temperature (°C).

## 2.4 HS-SPME-GC–MS Analysis of Volatile Compounds

> ✅ **已确认**: Agilent 8890-5977B，完全支持 HS-SPME。

### 2.4.1 HS-SPME Extraction

Volatile organic compounds (VOCs) were extracted using headspace solid-phase microextraction according to Liao et al. (2025) with modifications. A 0.1 g aliquot of freeze-dried mushroom powder was transferred to a 15 mL headspace vial containing 5 mL of ultrapure water and 10 µL of 4-methyl-2-pentanol internal standard solution (100 mg·L⁻¹). The vial was sealed with a PTFE/silicone septum cap.

The SPME fiber (50/30 µm DVB/CAR/PDMS, Supelco, Bellefonte, PA, USA) was pre-conditioned at 250 °C for 30 min in the GC injection port. Sample equilibration was performed at 55 °C for 15 min with agitation at 350 r·min⁻¹, followed by headspace extraction at 55 °C for 30 min. The fiber was then immediately desorbed at 250 °C for 5 min in the GC injection port in splitless mode.

### 2.4.2 GC–MS Conditions

Analysis was performed on an Agilent 8890 gas chromatograph coupled to an Agilent 5977B single quadrupole mass spectrometer (Agilent Technologies, Santa Clara, CA, USA). Volatile compounds were separated on a DB-WAX capillary column (30 m × 0.25 mm × 0.25 µm film thickness; Agilent Technologies) or an equivalent polar column. The carrier gas was helium (purity ≥ 99.999 %) at a constant flow rate of 1.0 mL·min⁻¹.

The oven temperature program was as follows: initial temperature 40 °C held for 3 min, ramped to 120 °C at 5 °C·min⁻¹, then to 230 °C at 10 °C·min⁻¹, held for 5 min. The total run time was approximately 35 min. The MS transfer line and ion source temperatures were set to 250 °C and 230 °C, respectively. Mass spectra were acquired in electron ionization (EI) mode at 70 eV over an *m/z* range of 35–450 amu in full-scan mode.

### 2.4.3 Compound Identification and Quantification

Volatile compounds were tentatively identified by matching mass spectra against the NIST 2020 library (National Institute of Standards and Technology, Gaithersburg, MD, USA) and confirmed by comparison of linear retention indices (LRI) calculated against a homologous series of *n*-alkanes (C₇–C₃₀) with literature values. Semi-quantification was performed by the internal standard method, with compound concentrations expressed as µg 4-methyl-2-pentanol equivalents per kg dry weight (µg·kg⁻¹ DW).

The odor activity value (OAV) for each identified compound was calculated as the ratio of its concentration to its orthonasal odor detection threshold in water, as reported in the literature. Compounds with OAV ≥ 1 were considered to contribute to the overall aroma profile of dried *M. sextelata*.

### 2.4.4 Instrument Configuration — Confirmed

The Agilent 8890-5977B system fully supports HS-SPME as a standard inlet configuration. The SPME fiber assembly (50/30 µm DVB/CAR/PDMS, 24 Ga, 2 cm; Supelco) was used with the Agilent SPME inlet liner (0.75 mm i.d., deactivated, splitless type) for optimized desorption efficiency and peak shape.

## 2.5 LC-MS/MS Analysis of Non-Volatile Metabolites

### 2.5.1 Metabolite Extraction

Non-volatile metabolites were extracted following Liu et al. (2024). A 100 mg aliquot of freeze-dried mushroom powder was homogenized in 1,000 µL of methanol/acetonitrile/water (2:2:1, v/v/v) at 4 °C. The homogenate was centrifuged at 14,000 × *g* for 20 min at 4 °C. The supernatant was collected and dried under vacuum centrifugation (SpeedVac, [Model]). The dried residue was reconstituted in 100 µL of acetonitrile/water (1:1, v/v) and centrifuged at 14,000 × *g* for 15 min at 4 °C. The resulting supernatant was transferred to an autosampler vial for analysis.

### 2.5.2 UHPLC-QTOF-MS Conditions

Metabolite profiling was performed on an ultra-high performance liquid chromatography system (1290 Infinity LC, Agilent Technologies) coupled to a quadrupole time-of-flight mass spectrometer (TripleTOF 6600, AB Sciex, Framingham, MA, USA) equipped with an electrospray ionization (ESI) source.

Hydrophilic interaction liquid chromatography (HILIC) separation was carried out on an ACQUITY UPLC BEH Amide column (2.1 mm × 100 mm, 1.7 µm; Waters, Wexford, Ireland). The mobile phase consisted of (A) 25 mM ammonium acetate and 25 mM ammonium hydroxide in water (pH ~9) and (B) acetonitrile. The gradient program was: 0–0.5 min, 95 % B; 0.5–7.0 min, 95–65 % B (linear); 7.0–8.0 min, 65–40 % B; 8.0–9.0 min, 40 % B (isocratic); 9.0–9.1 min, 40–95 % B; 9.1–12.0 min, 95 % B (re-equilibration). The flow rate was 0.3 mL·min⁻¹, the column temperature was 40 °C, and the injection volume was 2 µL.

ESI source parameters were: Ion Source Gas 1 (GS1) 60 psi, Ion Source Gas 2 (GS2) 60 psi, curtain gas (CUR) 30 psi, source temperature 600 °C, and IonSpray Voltage Floating (ISVF) ±5,500 V. For MS-only acquisition, spectra were collected over an *m/z* range of 60–1,000 Da with a TOF MS accumulation time of 0.20 s·spectrum⁻¹. For auto MS/MS acquisition, the *m/z* range was 25–1,000 Da with a product ion scan accumulation time of 0.05 s·spectrum⁻¹, using information-dependent acquisition (IDA) in high-sensitivity mode.

### 2.5.3 Quality Control and Data Processing

Quality control (QC) samples were prepared by pooling equal aliquots of all experimental samples and were injected every 10 analytical samples throughout the run to monitor instrumental stability (Liu et al., 2024). Blank samples (acetonitrile/water, 1:1) were analyzed prior to each sample batch.

Raw MS data were converted to mzXML format using ProteoWizard and processed with XCMS (v3.x, R/Bioconductor) for peak detection, retention time alignment, and peak area integration. Metabolites were identified by accurate mass matching against the Human Metabolome Database (HMDB, http://www.hmdb.ca) and the Kyoto Encyclopedia of Genes and Genomes (KEGG, http://www.kegg.jp) compound databases with a mass tolerance of 25 ppm. Metabolite annotation confidence followed Level 2 criteria (putative annotation) of the Metabolomics Standards Initiative (MSI) unless authentic standards were available for Level 1 confirmation.

## 2.6 Color and Appearance Quality Measurement

Surface color of mushroom slices was measured at each sampling point using a computer vision system comprising an industrial RGB camera and a closed LED illumination chamber, following Guo et al. (2025). CIE *L\** (lightness), *a\** (redness–greenness), and *b\** (yellowness–blueness) values were extracted from the segmented mushroom region. The total color difference (Δ*E*) relative to fresh samples was calculated as:

$$\Delta E = \sqrt{(L^*_0 - L^*_t)^2 + (a^*_0 - a^*_t)^2 + (b^*_0 - b^*_t)^2} \quad (6)$$

The shrinkage ratio (SR, %) was determined from the projected area of mushroom slices segmented from digital images, as:

$$SR = \frac{A_0 - A_t}{A_0} \times 100\% \quad (7)$$

where $A_0$ and $A_t$ are the projected pixel areas at time 0 and time $t$, respectively.

## 2.7 Machine Learning Pipeline

### 2.7.1 Feature Engineering

**Input features ($X$).** The input feature vector for each sample comprised 11 variables: drying temperature (*T*, °C), drying time (*t*, min), moisture ratio (MR), drying rate (DR, g·g⁻¹·min⁻¹), effective moisture diffusivity ($D_{eff,1}$ and $D_{eff,2}$, m²·s⁻¹), activation energy ($E_{a,1}$ and $E_{a,2}$, kJ·mol⁻¹), color difference (Δ*E*), shrinkage ratio (SR, %), and a categorical variable encoding the drying phase (initial / falling rate I / falling rate II).

**Output labels ($y$).** Three parallel output target sets were constructed: (i) individual VOC concentrations (µg·kg⁻¹ DW) of identified compounds with OAV ≥ 0.1; (ii) non-volatile metabolite abundances (peak areas) of the top 50 metabolites ranked by Spearman correlation with drying temperature; and (iii) aggregate flavor quality indices comprising total VOC content, equivalent umami concentration (EUC, g MSG 100 g⁻¹ DW, calculated from free amino acid and 5'-nucleotide contents as described by Liao et al., 2025), and the ratio of pleasant-flavor (aldehydes + pyrazines) to unpleasant-flavor (acetic acid) compounds.

### 2.7.2 Baseline Models: Random Forest and XGBoost

Random Forest (RF, Breiman, 2001) and eXtreme Gradient Boosting (XGBoost, Chen & Guestrin, 2016) models were implemented as baseline regressors using scikit-learn (v1.x) and xgboost (v2.x) Python libraries, respectively. Hyperparameters were tuned via five-fold cross-validation on the training set. RF hyperparameters included the number of trees (100–500), maximum tree depth (3–10), minimum samples per leaf (2–5), and the number of features considered at each split. XGBoost hyperparameters included the learning rate (0.01–0.3), maximum depth (3–6), subsample ratio (0.7–1.0), and L2 regularization parameter (λ, 0.1–10).

**Model evaluation.** Given the modest sample size (*N* = 72 observations from the factorial design, reduced to 48 independent observations after accounting for the 6 time points as partially nested), model performance was assessed by Leave-One-Out Cross-Validation (LOOCV) and bootstrap resampling (*B* = 1,000 iterations with replacement). Performance metrics included the coefficient of determination ($R^2$), root mean square error (RMSE), and mean absolute error (MAE).

### 2.7.3 Deep Learning: Long Short-Term Memory (LSTM)

For time-series prediction of volatile compound evolution during drying, a Long Short-Term Memory (LSTM) network (Hochreiter & Schmidhuber, 1997) was constructed following the dynamic ANN architecture validated by Guo et al. (2025) and Omari et al. (2018).

**Network architecture.** The LSTM model adopted a 3–6–7–1 structure: 3 input neurons (*T*, MR(*t*), and the target VOC abundance at the current time step), 6 neurons in the first hidden LSTM layer, 7 neurons in the second hidden LSTM layer, and 1 output neuron (the predicted VOC abundance at the next time step, *t* + Δ*t*). The Tanh activation function was used in the LSTM cells, and the Adam optimizer (learning rate = 0.01, β₁ = 0.9, β₂ = 0.999) was employed with Mean Squared Error (MSE) as the loss function.

**Training.** The dataset was partitioned into training (70 %), validation (15 %), and test (15 %) sets, with time-series sequences preserved within each partition. The model was trained for 15,000 iterations with early stopping when validation loss failed to improve for 500 consecutive iterations. Truncated Backpropagation Through Time (TBPTT) with a truncation length of 10 steps was applied to manage memory constraints (Guo et al., 2025).

**Comparison models.** The LSTM was benchmarked against: (i) a baseline Gated Recurrent Unit (GRU) network with an equivalent parameter budget; (ii) a Transformer encoder with positional encoding and multi-head self-attention (4 heads, 2 layers); and (iii) the static RF and XGBoost models described in Section 2.7.2, which use only current time-step features without temporal context.

### 2.7.4 Model Interpretability: SHAP Analysis

SHapley Additive exPlanations (SHAP, Lundberg & Lee, 2017) were computed for the best-performing tree-based model (RF or XGBoost) using the TreeSHAP algorithm. SHAP summary plots, dependence plots, and feature interaction plots were generated to identify: (a) which drying parameters most strongly influence specific volatile compound abundances, (b) the direction and functional form of each feature's effect, and (c) feature–feature interactions that may indicate synergistic or antagonistic effects during the Maillard reaction and lipid oxidation pathways.

For the LSTM model, permutation feature importance and integrated gradients were computed as post-hoc interpretability methods. The top 10 features (by mean |SHAP| value) were subsequently mapped to the 5 KEGG metabolic pathways (fructose and mannose metabolism, glycerolipid metabolism, *N*-glycan biosynthesis, amino acid metabolism, and nucleotide metabolism) identified as significantly enriched in Liu et al. (2024) to construct a putative causal mechanism model.

## 2.8 Metabolic Pathway Causal Mechanism Model

To bridge the gap between predictive power and mechanistic understanding, a five-pathway causal model was constructed. For each of the five KEGG pathways, the set of differentially abundant metabolites (DMs; VIP > 1 and *p* < 0.05 from OPLS-DA) was mapped to their corresponding enzymes and reactions. The temporal trajectories of key DMs were related to the time-resolved VOC profiles using Spearman rank correlation. Metabolites with |ρ| > 0.7 and *p* < 0.05 were retained as candidate mechanistic mediators linking drying conditions to volatile flavor compound formation.

## 2.9 Statistical Analysis

All experiments were conducted in triplicate and results were expressed as mean ± standard deviation (SD). One-way analysis of variance (ANOVA) followed by Tukey's honestly significant difference (HSD) post-hoc test was used to assess significant differences among temperature treatments at each sampling point, with the significance threshold set at *p* < 0.05 (SPSS v22, IBM Corp., Armonk, NY, USA).

Multivariate analysis of volatile and metabolite profiles was performed by principal component analysis (PCA) for unsupervised visualization and orthogonal partial least squares discriminant analysis (OPLS-DA) for supervised class separation. OPLS-DA model robustness was evaluated by seven-fold cross-validation and 200-iteration response permutation testing. Variable importance in projection (VIP) scores > 1.0 combined with Student's *t*-test *p*-values < 0.05 were used to select differentially abundant volatile compounds (DVFCs) and metabolites (DMs).

KEGG pathway enrichment analysis of DMs was performed using Fisher's exact test with a significance threshold of *p* < 0.05, and the significantly enriched pathways were visualized using the KEGG Mapper tool. All statistical analyses and machine learning model implementations were performed in Python (v3.x; scikit-learn, xgboost, shap, PyTorch) with R (v4.x; XCMS, ropls) for metabolomics data preprocessing. Analysis scripts are available at [GitHub repository URL] for reproducibility.

---

## References (Methods Section)

- Breiman, L. (2001). Random Forests. *Machine Learning, 45*, 5–32.
- Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *KDD '16*, 785–794.
- Guo, J., Liu, Y., Lei, D., et al. (2025). Combining DeepLabV3+ and LSTM for intelligent drying strategy optimization. *Computers and Electronics in Agriculture, 230*, 109929.
- Hochreiter, S., & Schmidhuber, J. (1997). Long Short-Term Memory. *Neural Computation, 9*(8), 1735–1780.
- Ivanova, M., Katrandzhiev, N., Dospatliev, L., et al. (2020). Mathematical modeling of drying kinetics of *Morchella esculenta* mushroom. *Bulgarian Chemical Communications, 52*(A), 39–46.
- Liao, Y., Xin, M., Dong, H., et al. (2025). Comparison of different drying processes of *Morchella sextelata*. *Food Chemistry: X, 25*, 102220.
- Liu, T., Wu, X., Long, W., et al. (2024). The effects of different postharvest drying temperatures on the volatile flavor components and non-volatile metabolites of *Morchella sextelata*. *Horticulturae, 10*, 812.
- Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *NeurIPS, 30*, 4765–4774.
- Omari, A., Behroozi-Khazaei, N., & Sharifian, F. (2018). Drying kinetic and artificial neural network modeling of mushroom drying process. *Journal of Food Process Engineering, 41*(7), e12849.
