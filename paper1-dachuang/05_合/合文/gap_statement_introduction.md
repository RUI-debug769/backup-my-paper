# 3.4 Research Gap Statement

> 适用章节：Introduction（最后一段 / gap & objective paragraph）
> 语言：学术英语 | 字数：~400 words | 参考文献：13 篇

---

## Gap Statement

Despite these advances in both drying kinetics modeling and flavor chemistry of edible fungi, a critical methodological gap persists: **no study has simultaneously captured time-resolved drying kinetics and volatile flavor evolution within the same experiment.** The existing literature falls into two disconnected streams.

The first stream—**drying kinetics research**—has established robust mathematical models for moisture ratio (MR) curves, effective moisture diffusivity (D*eff*), and activation energy (E*a*) during mushroom dehydration. Ivanova et al. (2020) fitted eleven thin-layer drying models to *Morchella esculenta* and reported D*eff* values ranging from 6.17 to 24.63 × 10⁻⁹ m²·s⁻¹ across 35–55°C. Omari et al. (2018) developed a dynamic artificial neural network (R² = 0.9914) to predict moisture content during microwave–hot air drying of mushroom. Guo et al. (2025) combined DeepLabV3+ semantic segmentation with LSTM to predict drying rate, shrinkage, and color change of *Pleurotus eryngii* slices in real time, achieving R² > 0.99. However, these kinetics-focused studies **did not measure volatile organic compounds (VOCs)**, leaving the relationship between drying parameters and flavor outcomes entirely unexamined.

The second stream—**flavor chemistry research**—has comprehensively characterized VOC profiles and non-volatile metabolites in dried mushrooms. Liu et al. (2024) identified 33 volatile compounds in hot-air dried *M. sextelata* using GC-IMS and 1,645 metabolites via LC-MS/MS, demonstrating that aldehydes, hydrocarbons, and pyrazines increased with drying temperature while acids, alcohols, and esters decreased. Liao et al. (2025) provided absolute quantification (μg·kg⁻¹ DW) of 29 VOCs across five drying processes using HS-SPME-GC–MS, revealing that total aroma compound content varied over 100-fold (from 2.0 × 10⁴ to 2.5 × 10⁶ μg·kg⁻¹) depending on the drying method. Yet these flavor-focused studies **sampled only at drying endpoints**, providing static snapshots rather than dynamic trajectories.

**These two streams have never been integrated.** The consequence is that the food industry cannot answer a deceptively simple question: *at what point during the drying process does Morchella achieve its optimal flavor profile?* Current practice relies entirely on experience-based endpoint determination rather than data-driven, real-time flavor optimization.

To bridge this gap, the present study proposes an integrated framework that simultaneously collects **(1) drying kinetics parameters** (MR, drying rate, D*eff*) and **(2) time-resolved VOC profiles** (HS-SPME-GC–MS) at multiple time points across a temperature gradient. This paired time-series dataset enables, for the first time, the application of machine learning models—from Random Forest and XGBoost baselines to Long Short-Term Memory (LSTM) networks—to predict dynamic flavor evolution from drying parameters, with SHapley Additive exPlanations (SHAP) providing mechanistic interpretability of the underlying causal pathways.

---

## 参考文献 (Gap Statement 引用)

1. Ivanova, M., Katrandzhiev, N., Dospatliev, L., Papazov, P., & Denev, P. (2020). Mathematical modeling of drying kinetics of *Morchella esculenta* mushroom. *Bulgarian Chemical Communications, 52*(A), 39–46.
2. Omari, A., Behroozi-Khazaei, N., & Sharifian, F. (2018). Drying kinetic and artificial neural network modeling of mushroom drying process in microwave-hot air dryer. *Journal of Food Process Engineering, 41*(7), e12849.
3. Guo, J., Liu, Y., Lei, D., Peng, Z., Mowafy, S., Li, X., Jia, Z., Ai, Z., & Xiao, H. (2025). Combining DeepLabV3+ and LSTM for intelligent drying strategy optimization in fruits and vegetables based on appearance quality: A case study of *Pleurotus eryngii*. *Computers and Electronics in Agriculture, 230*, 109929.
4. Liu, T., Wu, X., Long, W., Xu, Y., Yu, Y., & Wang, H. (2024). The effects of different postharvest drying temperatures on the volatile flavor components and non-volatile metabolites of *Morchella sextelata*. *Horticulturae, 10*, 812.
5. Liao, Y., Xin, M., Dong, H., Liu, Y., Li, L., Guo, X., Cheng, S., & Chen, G. (2025). Comparison of different drying processes of *Morchella sextelata*: Changes in volatile and non-volatile components, color and texture. *Food Chemistry: X, 25*, 102220.
6. Zhang, Y., Li, X., Zhao, Z., Hengchao, E., Fan, T., Dong, H., He, X., Zhao, X., Tang, L., & Zhou, C. (2023). Comprehensive investigation on non-volatile and volatile flavor compounds in the *Morchella sextelata* and *Morchella importuna* by UPLC-MS/MS and GC×GC-TOF-MS. *Food Chemistry: X, 20*, 100961.
7. Schreurs, M., et al. (2024). Predicting and improving complex beer flavor through machine learning. *Nature Communications, 15*, 2368.
8. Shi, J., et al. (2026). Machine learning for food flavor prediction and regulation: models, data, and challenges. *Trends in Food Science & Technology, 156*, 104784.
9. Younas, S., Liu, C., Qu, H., Mao, Y., Liu, W., Wei, L., Yan, L., & Zheng, L. (2020). Multispectral imaging for predicting the water status in mushroom during hot-air dehydration. *Journal of Food Science, 85*(6), 1808–1817.
10. Li, X., et al. (2023). Deep learning driven methodology for the prediction of mushroom drying characteristics. *Journal of Food Engineering, 350*, 111489.
11. Wen, X., et al. (2022). Quality characteristics and non-volatile taste formation mechanism of *Lentinula edodes* during hot air drying. *Food Chemistry, 393*, 133378.
12. Hu, S., Feng, X., Huang, W., Ibrahim, S. A., & Liu, Y. (2020). Effects of drying methods on non-volatile taste components of *Stropharia rugosoannulata* mushrooms. *LWT-Food Science and Technology, 127*, 109390.
13. Politowicz, J., Lech, K., Lipan, L., Figiel, A., & Carbonell-Barrachina, Á. A. (2018). Volatile composition and sensory profile of shiitake mushrooms as affected by drying method. *Journal of the Science of Food and Agriculture, 98*, 1511–1521.
