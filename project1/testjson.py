import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "U3uqCHQ1o8RHbLOuR6bA", "isbns":"0439139600"})
print(res)
data = res.json()
print(type(data))
print(data)
print(data['books'][0]['average_rating'])
#average_rating = data[average_rating]
#print(average_rating)