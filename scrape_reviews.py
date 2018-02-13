from lxml import html
import requests
from time import sleep
import sys

def ParseReviews(url):
	for i in range(5):
		try:
			# Add some recent user agent to prevent amazon from blocking the request
			headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

			page = requests.get(url,headers = headers)
			page_response = page.text

			parser = html.fromstring(page_response)
			XPATH_REVIEW_SECTION = '//div[@data-hook="review"]'

			reviews = parser.xpath(XPATH_REVIEW_SECTION)

			reviews_list = []

			if not reviews:
				raise ValueError('unable to find reviews in page')

			#Parsing individual reviews
			for review in reviews:
				XPATH_REVIEW_TEXT = './/span[@data-hook="review-body"]//text()'
				raw_review_text = review.xpath(XPATH_REVIEW_TEXT)

				#cleaning data
				review_text = ' '.join(' '.join(raw_review_text).split())

				reviews_list.append(review_text)

			return reviews_list
		except ValueError:
			print "Retrying to get the correct response"

	return {"error":"failed to process the page","url":url}

def ChangeReview(strs):
	res = ''
	for char in strs:
		if ord(char) < 128 and char != '\n':
			res += char
	return res

def ReadAsin():
	AsinList = ['B017HW9DEW','B009ZJ2M7G','B00VNGYZUG','B00N1VDCGO','B01C4UY0JK','B015HTJDDS','B00D3F9H2G','B01IWALX00','B01GU6TINM',
	'B017EHVNZW','B01HJVCBTK','B01EO35KGM','B003NX87U6','B006UEOQ5K','B000O03F4O','B008XNJXXQ','B019ZZB3O2','B0051D3MP6','B0091CC1OG',
	'B019DB5QQ4', 'B0094BB4TW', 'B00ZV9RDKK', 'B00005OU9D', 'B00YOP0T7G', 'B017GPB09Q', 'B015HVACEA', 'B01AVKKG8Y', 'B00IXHBMLS',
	'B077VS58CF', 'B00UMVW4VA', 'B06W9M3QDJ', 'B001STPJJO', 'B0002DJEYI', 'B0007QCNGG', 'B00M1I0WES', 'B01JKG95Q4', 'B000P7BMR8',
	'B01B1OGQH4', 'B002PXW1IE', 'B00ID0OWUS', 'B00HZYD5KQ', 'B0758CLT53', 'B00QU5M4MG', 'B0037V0EW8', 'B01AFRSQGW', 'B00IOY8XWQ',
	'B01CO4XWDQ', 'B075DHS7JK', 'B074ZMJZ6P', 'B00BTGMI5O', 'B0033P1O6S', 'B002VA464S', 'B000BNG4VU', 'B00325D0WK', 'B0050QJHTO',
	'B01GEW27DA', 'B00N1EJXUU', 'B074RRNB77', 'B00L40R76A', 'B01KJTB4ME', 'B003C1QQPW', 'B00GB85JR4', 'B002DRLESA', 'B00CQBKF9M',
	'B008LR8YMA']
	pos_list = []
	neg_list = []
	for asin in AsinList:
		url_five_star = 'http://www.amazon.com/product-reviews/'+asin+'/ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&reviewerType=all_reviews&filterByStar=five_star&pageNumber=1'
		url_four_star = 'http://www.amazon.com/product-reviews/'+asin+'/ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&reviewerType=all_reviews&filterByStar=four_star&pageNumber=1'
		url_one_star = 'http://www.amazon.com/product-reviews/'+asin+'/ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&reviewerType=all_reviews&filterByStar=one_star&pageNumber=1'
		url_two_star = 'http://www.amazon.com/product-reviews/'+asin+'/ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&reviewerType=all_reviews&filterByStar=two_star&pageNumber=1'
		sys.stdout.write("Downloading and processing asin: " + asin +"\r")
		sys.stdout.flush()
		pos_list += ParseReviews(url_five_star) + ParseReviews(url_four_star)
		neg_list += ParseReviews(url_one_star) + ParseReviews(url_two_star)
		sleep(5)
	with open('pos_reviews.txt', 'w') as f1, open('neg_reviews.txt', 'w') as f2:
		for elem in pos_list: f1.write(ChangeReview(elem) + '\n')
		for elem in neg_list: f2.write(ChangeReview(elem) + '\n')

if __name__ == '__main__':
	ReadAsin()
