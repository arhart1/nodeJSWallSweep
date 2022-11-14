import praw
import pandas as pd
import csv
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

#Post limit selection
sn = 1000 #int(input("Please select post limit: "))
search = False
sr = ''
rLimit = sn
 
#Open the stocks json file and save to a dict
#f = open('nasdaq_stocks.json')
#data = json.load(f)
#f.close()

data = [{"stock":"AAPL"},{"stock":"Activision Blizzard"},{"stock":"ADBE"},{"stock":"ADI"},{"stock":"Adobe"},{"stock":"ADP"},{"stock":"ADSK"},{"stock":"Advanced Micro Devices"},{"stock":"AEP"},{"stock":"ALGN"},{"stock":"Align Technology"},{"stock":"Alphabet (Class A)"},{"stock":"Alphabet (Class C)"},{"stock":"AMAT"},{"stock":"Amazon.com"},{"stock":"AMD"},{"stock":"American Electric Power"},{"stock":"Amgen"},{"stock":"AMGN"},{"stock":"AMZN"},{"stock":"Analog Devices"},{"stock":"ANSS"},{"stock":"Ansys"},{"stock":"Apple"},{"stock":"Applied Materials"},{"stock":"ASML"},{"stock":"ASML Holding"},{"stock":"Atlassian"},{"stock":"ATVI"},{"stock":"Autodesk"},{"stock":"Automatic Data Processing"},{"stock":"AVGO"},{"stock":"Baidu"},{"stock":"BBBY"},{"stock":"BIDU"},{"stock":"BIIB"},{"stock":"Biogen"},{"stock":"BKNG"},{"stock":"Booking Holdings"},{"stock":"Broadcom"},{"stock":"Cadence Design Systems"},{"stock":"CDNS"},{"stock":"CDW"},{"stock":"CDW"},{"stock":"CERN"},{"stock":"Cerner"},{"stock":"Charter Communications"},{"stock":"Check Point"},{"stock":"CHKP"},{"stock":"CHTR"},{"stock":"Cintas"},{"stock":"Cisco Systems"},{"stock":"CMCSA"},{"stock":"Cognizant"},{"stock":"Comcast"},{"stock":"Copart"},{"stock":"COST"},{"stock":"Costco"},{"stock":"CPRT"},{"stock":"CrowdStrike"},{"stock":"CRWD"},{"stock":"CSCO"},{"stock":"CSX"},{"stock":"CSX Corporation"},{"stock":"CTAS"},{"stock":"CTSH"},{"stock":"DexCom"},{"stock":"DLTR"},{"stock":"DOCU"},{"stock":"DocuSign"},{"stock":"Dollar Tree"},{"stock":"DXCM"},{"stock":"EA"},{"stock":"eBay"},{"stock":"EBAY"},{"stock":"Electronic Arts"},{"stock":"EXC"},{"stock":"Exelon"},{"stock":"FAST"},{"stock":"Fastenal"},{"stock":"FB"},{"stock":"Fiserv"},{"stock":"FISV"},{"stock":"FOX"},{"stock":"Fox Corporation (Class A)"},{"stock":"Fox Corporation (Class B)"},{"stock":"FOXA"},{"stock":"GILD"},{"stock":"Gilead Sciences"},{"stock":"GOOG"},{"stock":"GOOGL"},{"stock":"HON"},{"stock":"Honeywell"},{"stock":"Idexx Laboratories"},{"stock":"IDXX"},{"stock":"Illumina"},{"stock":"ILMN"},{"stock":"INCY"},{"stock":"Incyte"},{"stock":"INTC"},{"stock":"Intel"},{"stock":"INTU"},{"stock":"Intuit"},{"stock":"Intuitive Surgical"},{"stock":"ISRG"},{"stock":"JD"},{"stock":"JD.com"},{"stock":"KDP"},{"stock":"Keurig Dr Pepper"},{"stock":"KHC"},{"stock":"KLA Corporation"},{"stock":"KLAC"},{"stock":"Kraft Heinz"},{"stock":"Lam Research"},{"stock":"LRCX"},{"stock":"LULU"},{"stock":"Lululemon Athletica"},{"stock":"MAR"},{"stock":"Marriott International"},{"stock":"Marvell Technology"},{"stock":"Match Group"},{"stock":"MCHP"},{"stock":"MDLZ"},{"stock":"MELI"},{"stock":"MercadoLibre"},{"stock":"Meta Platforms"},{"stock":"Microchip Technology"},{"stock":"Micron Technology"},{"stock":"Microsoft"},{"stock":"MNST"},{"stock":"Moderna"},{"stock":"Mondel\u0113z International"},{"stock":"Monster Beverage"},{"stock":"MRNA"},{"stock":"MRVL"},{"stock":"MSFT"},{"stock":"MTCH"},{"stock":"MU"},{"stock":"NetEase"},{"stock":"Netflix"},{"stock":"NFLX"},{"stock":"NTES"},{"stock":"NVDA"},{"stock":"Nvidia"},{"stock":"NXP Semiconductors"},{"stock":"NXPI"},{"stock":"O'Reilly Automotive"},{"stock":"Okta"},{"stock":"OKTA"},{"stock":"ORLY"},{"stock":"Paccar"},{"stock":"Paychex"},{"stock":"PayPal"},{"stock":"PAYX"},{"stock":"PCAR"},{"stock":"PDD"},{"stock":"Peloton Interactive"},{"stock":"PEP"},{"stock":"PepsiCo"},{"stock":"Pinduoduo"},{"stock":"PTON"},{"stock":"PYPL"},{"stock":"QCOM"},{"stock":"Qualcomm"},{"stock":"Regeneron Pharmaceuticals"},{"stock":"REGN"},{"stock":"Ross Stores"},{"stock":"ROST"},{"stock":"SBUX"},{"stock":"Seagen"},{"stock":"SGEN"},{"stock":"SIRI"},{"stock":"Sirius XM"},{"stock":"Skyworks Solutions"},{"stock":"SNPS"},{"stock":"SPLK"},{"stock":"Splunk"},{"stock":"Starbucks"},{"stock":"SWKS"},{"stock":"Synopsys"},{"stock":"T-Mobile US"},{"stock":"TCOM"},{"stock":"TEAM"},{"stock":"Tesla"},{"stock":"Texas Instruments"},{"stock":"TMUS"},{"stock":"Trip.com Group"},{"stock":"TSLA"},{"stock":"TXN"},{"stock":"Verisign"},{"stock":"Verisk Analytics"},{"stock":"Vertex Pharmaceuticals"},{"stock":"VRSK"},{"stock":"VRSN"},{"stock":"VRTX"},{"stock":"Walgreens Boots Alliance"},{"stock":"WBA"},{"stock":"WDAY"},{"stock":"Workday"},{"stock":"Xcel Energy"},{"stock":"XEL"},{"stock":"Xilinx"},{"stock":"XLNX"},{"stock":"ZM"},{"stock":"Zoom Video Communications"},{"stock":"|"}]

reddit_read_only = praw.Reddit(client_id="llvTBy2FzFIQQRh4ukwMHg",         # your client id
                               client_secret="JbiED47CLhMop3YQnngMtdD63ANGSw",      # your client secret
                               user_agent="Nearby_Ad_7159 ")        # your user agent
 
# Scraping the top posts of the current month
subreddit = reddit_read_only.subreddit("wallstreetbets")
posts = subreddit.hot(limit = rLimit)

calculations = rLimit * len(data)

#Layout of dictionaries
posts_dict = {"Title": [], "Post Text": [],
              "ID": [], "Score": [],
              "Total Comments": [], "Post URL": []
              }
 
locate_dict = {"Title": [], "Post URL":[], "Stock":[], "Score":[]}
stocksUsed = []
counter = 0

print('Searching... \n')

for post in posts:
    # Title of each post
    posts_dict["Title"].append(post.title)
     
    # Text inside a post
    posts_dict["Post Text"].append(post.selftext)
     
    # Unique ID of each post
    posts_dict["ID"].append(post.id)
     
    # The score of a post
    posts_dict["Score"].append(post.score)
     
    # Total number of comments inside the post
    posts_dict["Total Comments"].append(post.num_comments)
     
    # URL of each post
    posts_dict["Post URL"].append(post.url)

    #Check if a post contains stock name

    for stock in data:
        counter = counter + 1
        stk = stock['stock']
                
        if (((' ' + stk + ' ') in post.title) or (('$' + stk) in post.title)or ((stk + ' ') in post.title) or ((' ' + stk + ' ') in post.selftext)or (('$' + stk) in post.selftext) or ((stk + ' ') in post.selftext)):
            locate_dict["Title"].append(post.title)
            locate_dict["Post URL"].append(post.url)
            locate_dict["Stock"].append(stk)  
            locate_dict["Score"].append(0)

            if stk not in stocksUsed:
                stocksUsed.append(stk)

    if ((counter /10) % (calculations) == 0):
        print('*', end ='')

print("\n")
print(stocksUsed)
print("Calculations: " + str(counter))
# Saving the data in a pandas dataframe
top_posts = pd.DataFrame(posts_dict)

check_posts = pd.DataFrame(locate_dict)
check_posts = check_posts.drop_duplicates()

count = 0
scores = []

final_scores = dict.fromkeys(stocksUsed, 0)
final_counts = dict.fromkeys(stocksUsed, 0)

for row in check_posts.itertuples():
    sid = SentimentIntensityAnalyzer()
    sentiment_dict = sid.polarity_scores(row.Title)
    
    scores.append(sentiment_dict['compound'])

    #Update total score (not average) and update counts
    for key, value in final_scores.items():
        if key == row.Stock:
            final_scores[key] = final_scores[key] + sentiment_dict['compound']
            final_counts[key] = final_counts[key] + 1

    print(row.Title + "\n")

    print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
 
    print("Sentence Overall Rated As", end = " ")
 
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        print("Positive")
 
    elif sentiment_dict['compound'] <= - 0.05 :
        print("Negative")
 
    else :
        print("Neutral")
    print("\n")
    count = count + 1

print("Final Counts: \n")
print(final_counts)

#Update final scores and round them
for key, value in final_scores.items():
    final_scores[key] = round(final_scores[key] / final_counts[key],4)

#*********************Debugging Console Info*********************
print("Final Scores: \n")
print(final_scores)

print("\n" + str(count))

check_posts = check_posts.assign(points = scores)

print(check_posts)
top_posts.to_csv('myData.csv')

#*****************************************************************

sortedCounts = dict(sorted(final_counts.items(), key = lambda x:x[1]))
sortedFinal = dict(sorted(final_scores.items(), key = lambda x:x[1]))
print("Sorted: ")
print(sortedFinal)

#Menu UI and options
menu = True
while menu:
    print("\n##     ## ######## ##    ## ##     ## \n###   ### ##       ###   ## ##     ## \n#### #### ##       ####  ## ##     ## \n## ### ## ######   ## ## ## ##     ## \n##     ## ##       ##  #### ##     ## \n##     ## ##       ##   ### ##     ## \n##     ## ######## ##    ##  #######  \n")
    menSel = int(input("\n1. Most Positive\n2. Most Negative\n3. Most Discussed\n4. Search\n5. Exit\n Selection: "))
    os.system('cls')

    if menSel == 1:
        print("Most Positive Stock: ")
        print(list(sortedFinal.items())[-1])
        print('')
    elif menSel == 2:
        print("Most Negative Stock: ")
        print(list(sortedFinal.items())[0])
        print('')
    elif menSel == 3:
        print("Most Discussed Stock: ")
        print(list(sortedCounts.items())[-1])
        print('')
    elif menSel == 4:
        #Search for specific stock
        searchSel = input("Stock: ")

        if searchSel not in stocksUsed:
            print("No available data.")
        else:
            print("Score: ")
            searchKey = list(sortedFinal.keys()).index(searchSel)
            print(list(sortedFinal.items())[searchKey])

            print("Count: ")
            searchKey = list(sortedCounts.keys()).index(searchSel)
            print(list(sortedCounts.items())[searchKey])

    elif menSel == 5:
        menu = False
    else:
        print("Invalid selection.")