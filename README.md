# Code_for_Bootstrap_of_Bootstraps-Fama-and-French-2018-
This repo provide the code of Bootstrap method proposed by Fama and French (2018) in predicting Long-horizon returns.

Simulation Framework using Bootstrap of Bootstraps
version 1.0 (JZ): May 19, 2020 
This module provides a new framework of estimating future return, particuarly in LTR.

The method Bootstrap of Bootstraps (BB) is proposed by Fama and French (2018)
Full paper: Fama E.F. and French, K.R., 2018. Long-horizon returns. 
Journal: The Review of Asset Pricing Studies
Link: https://academic.oup.com/raps/article-abstract/8/2/232/4810768

This method provides a new estimation complementary to Averaged Historical Returns
Advantages: 1)Realized data become less available in long-term; 2) No restriction to historical data; 3) simplify the distribution

Assumptions:
    1.Monthly return is a process of random walk;
    2.Long-term return is the product of monthly return;
    3.The central limit theorem says bootstraped LTR converge toward nomal distribution;
    
There are two sub-methods called NED and FS:
    1. NED: monthly return sampled from normal distribution with the same mean and standard deviation of historical return;
    2. FS: monthly return sampled directly from historical return.
    
Steps:
    1. sample these monthly returns with replacement to generate each horizon’s 100,000 cumulative returns
    2. repeat the process by 1000 times
    3. calculate the statistical information
