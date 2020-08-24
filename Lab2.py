#Michael Chen
#Lab HW 2

#Change working directory to desktop (where my .txt file is at)
import os
os.chdir("/Users/michaelchen/Desktop")

#Connect a reader to the book file
reader = open("Frankenstein.txt","r")

#Split the book by lines and store it into variable 'data'
print("Splitting into 'data'")
data = []
for x in reader:
    data.append(x)

#For each group, make a dictionary for each word with the word as the key,
# and 1 as the value. Store it into a variable 'mapping'
print("Mapping into 'mapping'")
mapping = []
for line in data:
    words = []
    for word in line.split():
        words.append({word:1})
    mapping.append(words)

#For each word in each mapping, place it into a new list which groups the
#   same words together in a dictionary, where the key is the word, and the value
#   increments for each time the word is found, starting from 1.
print("Reducing into 'reducing'")
reducing = []
for i,words in enumerate(mapping):  #I use this so I know the progress of the reducer
    if i % 500 == 0 or i == len(mapping)-1:
        print(i,"/",len(mapping)-1)
    for word in words:
        #word: {"word",1}
        #search reducing for matching key
        found = False
        for x in range(len(reducing)):
            #print(list(word.keys())[0],list(reducing[x].keys())[0])
            if list(reducing[x].keys())[0] == list(word.keys())[0]:
                reducing[x] = {
                    list(reducing[x].keys())[0] : reducing[x].get(list(reducing[x].keys())[0]) + 1
                }
                found = True
                break
        if not found:
            reducing.append(word)

#Insert into my NoSQL Dynamodb server.
#Before running this code, make sure you have boto3 installed
#Then configure it by typing this in your terminal:
#$ export AWS_ACCESS_KEY_ID= (your AWS key)
#$ export AWS_SECRET_ACCESS_KEY= (your AWS secret access key)
print("Inserting into DynamoDB Table")
import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
table = dynamodb.Table('michaellab2')

for x in reducing:
    table.put_item(Item={"word" : list(x.keys())[0], "count" : x.get(list(x.keys())[0])})

print("done")

