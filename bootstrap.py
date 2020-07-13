import pandas as pd
import numpy as np
import random

'''
Name: The update version of BB approach
Author: Jinkai Zhang
Date: July 13, 2020

Description:
    This updated version has fixed the problem of high standard deviation compared to earlier version.

Note:
    The output displays the raw return instead of natural log return
    The output records the statistical description of estimated ANUALIZED RETURN

Data:
    S&P monthly return from 1961 - 2020
    
Results:
    NED Method:
        Predict US 1-year return using bootstrap-NED
        {'Mean(%)': 7.9929, 'Standard Deviation(%)': 15.5686, 'Median(%)': 7.9921, '25th(%)': -2.5086, '75th(%)': 18.4945, 'Confidence Interval(95)(%)': [-17.6128, 33.6049]}
        
        Predict US 3-year return using bootstrap-NED
        {'Mean(%)': 7.2509, 'Standard Deviation(%)': 8.8637, 'Median(%)': 7.2516, '25th(%)': 1.2717, '75th(%)': 13.2297, 'Confidence Interval(95)(%)': [-7.3263, 21.8297]}
        
        Predict US 5-year return using bootstrap-NED
        {'Mean(%)': 6.963, 'Standard Deviation(%)': 7.0249, 'Median(%)': 6.9635, '25th(%)': 2.2241, '75th(%)': 11.7007, 'Confidence Interval(95)(%)': [-4.5901, 18.5193]}
        
        Predict US 10-year return using bootstrap-NED
        {'Mean(%)': 6.8128, 'Standard Deviation(%)': 4.953, 'Median(%)': 6.8126, '25th(%)': 3.4716, '75th(%)': 10.1533, 'Confidence Interval(95)(%)': [-1.3333, 14.96]}
        
        Predict US 20-year return using bootstrap-NED
        {'Mean(%)': 7.4988, 'Standard Deviation(%)': 2.8626, 'Median(%)': 7.499, '25th(%)': 5.5676, '75th(%)': 9.4299, 'Confidence Interval(95)(%)': [2.7899, 12.2069]}

    FS Method: 
        Predict US 1-year return using bootstrap-FS
        {'Mean(%)': 7.9931, 'Standard Deviation(%)': 15.57, 'Median(%)': 9.8223, '25th(%)': -0.8861, '75th(%)': 17.8562, 'Confidence Interval(95)(%)': [-19.179, 31.7078]}
        
        Predict US 3-year return using bootstrap-FS
        {'Mean(%)': 7.2512, 'Standard Deviation(%)': 8.8652, 'Median(%)': 8.287, '25th(%)': 2.318, '75th(%)': 12.6367, 'Confidence Interval(95)(%)': [-9.211, 23.1141]}
       
        Predict US 5-year return using bootstrap-FS
        {'Mean(%)': 6.9621, 'Standard Deviation(%)': 7.025, 'Median(%)': 7.5902, '25th(%)': 0.9303, '75th(%)': 11.6696, 'Confidence Interval(95)(%)': [-3.4578, 20.1115]}
        
        Predict US 10-year return using bootstrap-FS
        {'Mean(%)': 6.8136, 'Standard Deviation(%)': 4.9532, 'Median(%)': 6.799, '25th(%)': 2.7521, '75th(%)': 11.0104, 'Confidence Interval(95)(%)': [-1.293, 14.8059]}
        
        Predict US 20-year return using bootstrap-FS
        {'Mean(%)': 7.4988, 'Standard Deviation(%)': 2.8623, 'Median(%)': 6.8997, '25th(%)': 5.4341, '75th(%)': 9.6596, 'Confidence Interval(95)(%)': [3.57, 13.1759]}
                
'''



#just change the working directory and read this data
#the unit of input and output series return are '%'
#note: the input include two columns named 'Date' and 'Return'

US_monthly = pd.read_csv('sp.csv')


def bootstrap (df, periods_month, method = 'NED', condidence_interval = 95):
    try:
        df.index = range(len(df))
    
        def Return_Detection(df, begin_index, return_history, periods_month):
            begin_index += 1
            end_index = begin_index + periods_month
            if end_index - 1 <= len(df):
                returns_monthly = df.Return[begin_index:end_index].tolist()
                def plus_one (x): return (x/100 + 1)
                returns_monthly = list(map(plus_one, returns_monthly))
                #culmulate the monthly return to LTR
                returns_periods = np.prod(returns_monthly) - 1
                #Transfer from Cumulated return to Anualized return
                # (1 + Montly_Return) ^ periods_month - 1 = Cumul_Ret    ----(1)
                Montly_Return = (returns_periods + 1) ** (1 / periods_month) - 1
                # (1 + Montly_Return) ^ 12 - 1 = Anualized_Return    ----(2)
                Anualized_Return = (1 + Montly_Return) ** 12 - 1
                #transfer back to the unit of '%'
                Anualized_Return = Anualized_Return * 100
                return_history.append(Anualized_Return)
            else:
                pass
            return return_history
        
        returns = []
        for i in range(len(df)):
            Return_Detection(df, i, returns, periods_month)
            
        #method of NED, sampled from normal distribution
        if method == 'NED':
            #mean and standard deviation of historical culmulative return
            mu_NED = np.array(returns).mean()
            sigma_NED = np.array(returns).std()
            mean_collection = []
            std_collection = []
            median_collection = []
            twentyfive_collection = []
            seventyfive_collection = []
            confi_string =  'Confidence Interval(' + str(condidence_interval) + ')(%)'
            confi_right = condidence_interval
            confi_left = 100 - confi_right
            left_collection = []
            right_collection = []
            
            #repeat each simulation of sampling 100000 monthly returns for 1000 times, consistent with Fama and French (2018).
            for i in range(1000):
                data_application = np.random.normal(mu_NED, sigma_NED, 100000)
                
                mean_collection.append(np.mean(data_application))
                std_collection.append(np.std(data_application))
                median_collection.append(np.median(data_application))
                twentyfive_collection.append(np.percentile(data_application, 25))
                seventyfive_collection.append(np.percentile(data_application, 75))
                left_collection.append(np.percentile(data_application, confi_left))
                right_collection.append(np.percentile(data_application, confi_right))
           
            output = dict()
            output['Mean(%)'] = round(np.mean(mean_collection), 4)
            output['Standard Deviation(%)'] = round(np.mean(std_collection), 4)
            output['Median(%)'] = round(np.mean(median_collection), 4)
            output['25th(%)'] = round(np.mean(twentyfive_collection), 4)
            output['75th(%)'] = round(np.mean(seventyfive_collection), 4)
            output[confi_string] = [round(np.mean(left_collection), 4),
                                   round(np.mean(right_collection), 4)]  
            
            #please run 'return output['Mean(%)']' if only need output of return
            return output
       
        elif method == 'FS':
            mean_collection = []
            std_collection = []
            median_collection = []
            twentyfive_collection = []
            seventyfive_collection = []
            confi_string =  'Confidence Interval(' + str(condidence_interval) + ')(%)'
            confi_right = condidence_interval
            confi_left = 100 - confi_right
            left_collection = []
            right_collection = []
            
            for i in range(1000):
                data_application = random.choices(returns, k = 100000)
                mean_collection.append(np.mean(data_application))
                std_collection.append(np.std(data_application))
                median_collection.append(np.median(data_application))
                twentyfive_collection.append(np.percentile(data_application, 25))
                seventyfive_collection.append(np.percentile(data_application, 75))
                left_collection.append(np.percentile(data_application, confi_left))
                right_collection.append(np.percentile(data_application, confi_right))
                
            output = dict()
            output['Mean(%)'] = round(np.mean(mean_collection), 4)
            output['Standard Deviation(%)'] = round(np.mean(std_collection), 4)
            output['Median(%)'] = round(np.mean(median_collection), 4)
            output['25th(%)'] = round(np.mean(twentyfive_collection), 4)
            output['75th(%)'] = round(np.mean(seventyfive_collection), 4)
            output[confi_string] = [round(np.mean(left_collection), 4),
                                   round(np.mean(right_collection), 4)]  
            
            #please run 'return output['Mean(%)']' if only need output of return
            return output
        else:
            print ('Oops! The method is not included..')
    except:
        print('Oops! Something wrong. May check the column name and try again..')


if __name__ == '__main__':
    """
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~ EXAMPLES ~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    """

    print('Predict US 1-year return using bootstrap-NED')
    NED_1_year = bootstrap(US_monthly, periods_month = 1 * 12, method = 'NED')
    print(NED_1_year)
    print('Predict US 3-year return using bootstrap-NED')
    NED_3_year = bootstrap(US_monthly, periods_month = 3 * 12, method = 'NED')
    print(NED_3_year)
    print('Predict US 5-year return using bootstrap-NED')
    NED_5_year = bootstrap(US_monthly, periods_month = 5 * 12, method = 'NED')
    print(NED_5_year)
    print('Predict US 10-year return using bootstrap-NED')
    NED_10_year = bootstrap(US_monthly, periods_month = 10 * 12, method = 'NED')
    print(NED_10_year)
    print('Predict US 20-year return using bootstrap-NED')
    NED_20_year = bootstrap(US_monthly, periods_month = 20 * 12, method = 'NED')
    print(NED_20_year)

    
    #using 'FS' leads to very similar results, but need a couple of minutes to get the results
    print('Predict US 1-year return using bootstrap-FS')
    FS_1_year = bootstrap(US_monthly, periods_month = 1 * 12, method = 'FS')
    print(FS_1_year)
    print('Predict US 3-year return using bootstrap-FS')
    FS_3_year = bootstrap(US_monthly, periods_month = 3 * 12, method = 'FS')
    print(FS_3_year)
    print('Predict US 5-year return using bootstrap-FS')
    FS_5_year = bootstrap(US_monthly, periods_month = 5 * 12, method = 'FS')
    print(FS_5_year)
    print('Predict US 10-year return using bootstrap-FS')
    FS_10_year = bootstrap(US_monthly, periods_month = 10 * 12, method = 'FS')
    print(FS_10_year)
    print('Predict US 20-year return using bootstrap-FS')
    FS_20_year = bootstrap(US_monthly, periods_month = 20 * 12, method = 'FS')
    print(FS_20_year)

