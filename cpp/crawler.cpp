#include <iostream>
#include <fstream>
#include <pqxx/pqxx>
#include <json/reader.h>
#include <json/writer.h>
#include <json/value.h>
#include <curl/curl.h>

static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp){
  ((std::string*)userp)->append((char*)contents, size * nmemb);
  return size * nmemb;
}

int openSafely(std::string *url, std::string *read_buffer, int segment, ofstream errLog){
  CURL *curl;
  CURLcode res;
  //this init might burst into flames if we are using threads
  curl = curl_easy_init();
  if(curl) {
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, read_buffer);
    res = curl_easy_perform(curl);
    if(res!=CURLE_OK){
      errLog << "curl performance error " << res << ", at segment " << segment << std::endl;
    }
    curl_easy_cleanup(curl);
  }else{
    errLog << "curl init error " << curl << ", at segment " << segment << std::endl;
  }
  return 0;
  std::cout << *read_buffer << std::endl;
}

