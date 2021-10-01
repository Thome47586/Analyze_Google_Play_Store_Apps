# Explore data analysis Google Play Store Apps


## Introduction
I found it on Kaggle when studied Data Analysis. It provides an overview, useful information to help new learners easily access and practice analysis.

link: https://www.kaggle.com/ysthehurricane/generate-eda-report-using-pandas-profiling

<img width="875" alt="Screen Shot 2021-09-30 at 10 08 12" src="https://user-images.githubusercontent.com/86963378/135382050-abfcaf61-79e6-44d9-8251-db57139189be.png">


## I. Content EDA
   ### 1. Define question
   - Explore top high attention-paid categories. 
   - Discover paid categories above
   - Detect developer is the most effective
 
   ### 2. Explore top high attention-paid categories.
   Rating count is total user's review, who pays attention to categories. 
   Observe correlation of rating_count with other features.
   
   <img width="875" alt="Screen Shot 2021-09-30 at 10 17 00" src="https://user-images.githubusercontent.com/86963378/135385066-07a818dd-bb24-4495-aa7c-477b34cf9d69.png">
   
   Find out top high attention-paid categories
    <img width="875" alt="Screen Shot 2021-09-30 at 10 16 45" src="https://user-images.githubusercontent.com/86963378/135381541-6cd44f0a-675b-4a95-8937-1e4f8104eb3f.png">

**Strategy category ranked first, over 40% ranked second.**

    
   ### 3. Discover paid categories above
   Discover top 10 categories above and Srategy in paid-section 
   
   
   <img width="875" alt="Screen Shot 2021-09-30 at 11 34 31" src="https://user-images.githubusercontent.com/86963378/135387917-6fc22701-7b29-4691-bb74-d36c1e516950.png">
   
   Expose range of price recommended by developers

   <img width="463" alt="Screen Shot 2021-09-30 at 11 34 38" src="https://user-images.githubusercontent.com/86963378/135387930-1ef90d16-42d2-45e7-95ef-67233e74fa32.png">



   ### 4. Detect developer is the most effective
   Actually, only 2 developers own top favorite apps in strategy categories
   
   <img width="875" alt="Screen Shot 2021-09-30 at 11 42 17" src="https://user-images.githubusercontent.com/86963378/135388637-1b433ad9-3a47-4683-8233-2e9185bea646.png">
   
   We notice IGG.COM is the best development because quantity install and ratingng_count is low but their app is in the top.
   
<img width="875" alt="Screen Shot 2021-09-30 at 11 47 34" src="https://user-images.githubusercontent.com/86963378/135389071-f08472d6-84c6-4603-b6e5-e78ef62f0620.png">

   
   

## II. Code
### 1. Basic exploration
    Over view data with basic syntax
### 2. Clean data
    2.1 Remove duplicated
    2.2 Check and change datatype
    2.3 Working with missing values
    2.4 Drop columns no need to EDA
    2.5 Covert numerical feature to float
### 3. EDA
    3.1 Overview quantity
    3.2 Top 10 categories highest number
    3.3 More explore like content EDA above
    

# III. Libraries
    1. Pandas
    2. Matplotlib
    3. Seasborn
