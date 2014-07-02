#include <iostream>
#include <fstream>
#include <pqxx/pqxx>
#include <curl/curl.h>
#include <rapidjson/document.h>
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>
//when we open our ofstream, we should write a representation of our SID to the damn thing.

using namespace rapidjson;

static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp){
  ((std::string*)userp)->append((char*)contents, size * nmemb);
  return size * nmemb;
}

//return 0 on success, d 
//return 1 on error, 
//pass an unallocated pointer to the thing.
int openSafely(std::string *url, Document d, int segment, std::ofstream errLog){
  CURL *curl;
  CURLcode res;
  std::string *read_buffer = NULL;
  //this init might burst into flames if we are using threads.
  //otherwise, read_buffer should contain our string afterwards
  curl = curl_easy_init();
  if(curl) {
    curl_easy_setopt(curl, CURLOPT_URL, url->c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, read_buffer);
    res = curl_easy_perform(curl);
    if(res!=CURLE_OK){
      errLog << "curl performance error " << res << ", at segment " << segment << std::endl;
    }
    curl_easy_cleanup(curl);
  }else{
    errLog << "curl init error " << curl << ", at segment " << segment << std::endl;
    return 1;
  }
  d.Parse<0>(read_buffer->c_str());
  std::cout << *read_buffer << std::endl;
  return 0;
}


int main(int argc, char **argv){

  return 0;
}
